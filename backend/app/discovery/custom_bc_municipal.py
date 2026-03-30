"""Shared base class for small BC municipal website scrapers.

Most small BC municipalities use WordPress or similar CMS platforms with
a consistent pattern: a council/meetings landing page with links to
agenda/minutes subpages or direct PDF links. This base class provides
the shared parsing logic so individual scrapers only need to define
municipality-specific URL patterns or fallback strategies.
"""

import logging
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper, DiscoveredItem
from app.discovery.civicweb import parse_civicweb_date, classify_meeting_type

logger = logging.getLogger(__name__)

# Date regex
DATE_RE = re.compile(
    r"(?:(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s*)?"
    r"(\w+ \d{1,2},?\s*\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})"
)


def extract_date(text: str) -> str | None:
    """Extract and parse the first date found in text."""
    match = DATE_RE.search(text)
    return parse_civicweb_date(match.group(1)) if match else None


def classify_link(link_text: str, href: str) -> str | None:
    """Classify a link as agenda, minutes, or video."""
    text = link_text.lower()
    href_lower = href.lower()

    if "agenda" in text or "agenda" in href_lower:
        return "agenda"
    if "minute" in text or "minute" in href_lower:
        return "minutes"
    if any(k in text for k in ["video", "watch", "recording", "webcast"]):
        return "video"
    if any(k in href_lower for k in ["youtube.com", "youtu.be", "vimeo.com"]):
        return "video"
    # Catch bare PDF links near meeting content
    if href_lower.endswith(".pdf") and any(
        k in text for k in ["council", "meeting", "regular", "special", "hearing"]
    ):
        return "agenda"
    return None


class BCMunicipalScraper(BaseScraper):
    """Base scraper for small BC municipal websites.

    Subclasses can override `_extra_subpage_keywords` to add
    municipality-specific terms for finding agenda/minutes subpages.
    """

    # Subclasses can extend this list
    _subpage_keywords: list[str] = [
        "agenda", "minutes", "council meeting", "schedule",
        "regular council", "public hearing", "council schedule",
        "meetings", "agendas and minutes",
    ]

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meeting documents from a municipal website."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        try:
            html = await self.fetch(self.base_url)
            soup = BeautifulSoup(html, "lxml")

            # Parse the landing page
            for item in self._parse_page(soup, self.base_url):
                if item.url not in seen_urls:
                    seen_urls.add(item.url)
                    items.append(item)

            # Find and follow subpages
            sub_links = self._find_subpage_links(soup)
            for link_url in sub_links[:8]:
                try:
                    sub_html = await self.fetch(link_url)
                    sub_soup = BeautifulSoup(sub_html, "lxml")
                    for item in self._parse_page(sub_soup, link_url):
                        if item.url not in seen_urls:
                            seen_urls.add(item.url)
                            items.append(item)
                except Exception:
                    continue

        except Exception as e:
            logger.error("%s scrape failed: %s", self.municipality, e)

        logger.info("%s discovery: %d items found", self.municipality, len(items))
        return items

    def _find_subpage_links(self, soup: BeautifulSoup) -> list[str]:
        """Find links to agenda/minutes subpages from the landing page."""
        links: list[str] = []
        base_domain = urlparse(self.base_url).netloc

        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True).lower()
            href = link["href"]
            full = urljoin(self.base_url, href)

            # Stay on the same domain
            if urlparse(full).netloc != base_domain:
                continue

            if any(k in text for k in self._subpage_keywords):
                if full not in links and full != self.base_url:
                    links.append(full)

            # Also follow year/archive links
            if any(k in text for k in ["202", "archive", "previous", "past"]):
                if full not in links and full != self.base_url:
                    links.append(full)

        return links

    def _parse_page(
        self, soup: BeautifulSoup, source_url: str
    ) -> list[DiscoveredItem]:
        """Parse a page for meeting document links."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        # Scan tables
        for row in soup.find_all("tr"):
            row_text = row.get_text(" ", strip=True)
            meeting_date = extract_date(row_text)

            for link in row.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                if full_url in seen_urls:
                    continue

                item_type = classify_link(link_text, href)
                if item_type:
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text or row_text[:100],
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(row_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        # Scan list items and content containers
        for el in soup.find_all(["li", "div", "article", "section", "p"]):
            el_text = el.get_text(" ", strip=True)
            if len(el_text) > 500:
                continue
            meeting_date = extract_date(el_text)

            for link in el.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                if full_url in seen_urls:
                    continue

                item_type = classify_link(link_text, href)
                if item_type:
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text or el_text[:100],
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(el_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        return items


# ---------------------------------------------------------------------------
# Config-driven generic scraper registry
# ---------------------------------------------------------------------------
# Maps municipality short_name -> extra subpage keywords beyond the base set.
# Municipalities not listed here get just the base keywords.

GENERIC_SCRAPER_KEYWORDS: dict[str, list[str]] = {
    "100 Mile House": ["council-meetings", "council meetings"],
    "Ainsworth Hot Springs": ["rdkb"],
    "Alert Bay": ["council"],
    "Anmore": ["council", "agendas-minutes"],
    "Armstrong": ["council", "bylaws"],
    "Ashcroft": ["council"],
    "Balfour": ["rdkb"],
    "Barriere": ["council"],
    "Belcarra": ["council"],
    "Burns Lake": ["council"],
    "Cache Creek": ["council"],
    "Canal Flats": ["council"],
    "Castlegar": ["council", "bylaws"],
    "Chase": ["council"],
    "Chetwynd": ["council"],
    "Christina Lake": ["rdkb"],
    "Clearwater": ["council"],
    "Clinton": ["council"],
    "Coldstream": ["council"],
    "Cranbrook": ["council"],
    "Creston": ["council"],
    "Cumberland": ["council"],
    "Elkford": ["council"],
    "Enderby": ["council", "bylaws"],
    "Fernie": ["council-meetings", "council meetings"],
    "Fort Nelson": ["council"],
    "Fort St. James": ["council"],
    "Fraser Lake": ["council"],
    "Fruitvale": ["council"],
    "Gibsons": ["council"],
    "Gold River": ["council"],
    "Golden": ["council"],
    "Grand Forks": ["council", "bylaws"],
    "Granisle": ["council"],
    "Greenwood": ["council"],
    "Harrison Hot Springs": ["council"],
    "Hazelton": ["council"],
    "Hope": ["council"],
    "Houston": ["council"],
    "Hudson's Hope": ["council"],
    "Invermere": ["council"],
    "Kaslo": ["council"],
    "Kent": ["council"],
    "Keremeos": ["council"],
    "Kimberley": ["council"],
    "Kitimat": ["council"],
    "Lillooet": ["council"],
    "Lions Bay": ["council"],
    "Logan Lake": ["council"],
    "Lumby": ["council"],
    "Mackenzie": ["council"],
    "Masset": ["council"],
    "McBride": ["council"],
    "Midway": ["council"],
    "Montrose": ["council"],
    "Nakusp": ["council"],
    "Nelson": ["council", "bylaws"],
    "New Denver": ["council"],
    "New Hazelton": ["council"],
    "Northern Rockies": ["council"],
    "Pemberton": ["council"],
    "Port Alice": ["council"],
    "Port Clements": ["council"],
    "Port Edward": ["council"],
    "Port Hardy": ["council"],
    "Port McNeill": ["council"],
    "Pouce Coupe": ["council"],
    "Prince Rupert": ["council-meetings", "council meetings"],
    "Princeton": ["council"],
    "Quesnel": ["council", "bylaws"],
    "Radium Hot Springs": ["council"],
    "Revelstoke": ["council"],
    "Riondel": ["council"],
    "Rossland": ["council"],
    "Salmo": ["council"],
    "Salmon Arm": ["council", "bylaws"],
    "Sayward": ["council"],
    "Sicamous": ["council"],
    "Silverton": ["council"],
    "Slocan": ["council"],
    "Smithers": ["council"],
    "Spallumcheen": ["council"],
    "Sparwood": ["council"],
    "Stewart": ["council"],
    "Surrey": ["council", "bylaws", "public-hearing"],
    "Tahsis": ["council"],
    "Telkwa": ["council"],
    "Terrace": ["council", "bylaws"],
    "Trail": ["council", "bylaws"],
    "Tumbler Ridge": ["council"],
    "Valemount": ["council"],
    "Vanderhoof": ["council"],
    "Warfield": ["council"],
    "Wells": ["council"],
    "Williams Lake": ["council", "bylaws"],
    "Zeballos": ["council"],
}


def make_generic_scraper(short_name: str, url: str) -> BCMunicipalScraper | None:
    """Create a BCMunicipalScraper with config-driven keywords for a municipality.

    Returns None if the municipality has no entry in GENERIC_SCRAPER_KEYWORDS.
    """
    extra_keywords = GENERIC_SCRAPER_KEYWORDS.get(short_name)
    if extra_keywords is None:
        return None

    scraper = BCMunicipalScraper(short_name, url)
    scraper._subpage_keywords = [*BCMunicipalScraper._subpage_keywords, *extra_keywords]
    return scraper
