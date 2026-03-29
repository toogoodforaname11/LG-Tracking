"""Custom scraper for Capital Regional District (CRD) Board.

Source URL: https://www.crd.bc.ca/about/board-committees/board-committee-meetings
CRD publishes board and committee meeting agendas and minutes on their website.
"""

import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper, DiscoveredItem
from app.discovery.civicweb import parse_civicweb_date, classify_meeting_type

logger = logging.getLogger(__name__)

# CRD-specific meeting type keywords
CRD_MEETING_TYPES = [
    ("board", "regular"),
    ("committee of the whole", "committee_of_the_whole"),
    ("planning", "committee"),
    ("finance", "committee"),
    ("governance", "committee"),
    ("environment", "committee"),
    ("transportation", "committee"),
    ("regional water", "committee"),
    ("hospital", "committee"),
    ("public hearing", "public_hearing"),
    ("special", "special"),
]


def classify_crd_meeting_type(title: str) -> str:
    """Classify CRD meeting type from title."""
    title_lower = title.lower()
    for keyword, mtype in CRD_MEETING_TYPES:
        if keyword in title_lower:
            return mtype
    return classify_meeting_type(title)


class CRDScraper(BaseScraper):
    """Scraper for Capital Regional District board and committee meetings."""

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meeting documents from the CRD board meetings page."""
        items: list[DiscoveredItem] = []

        try:
            html = await self.fetch(self.base_url)
            soup = BeautifulSoup(html, "lxml")

            # Parse the main meetings page
            items = self._parse_page(soup, self.base_url)

            # Follow links to specific committee or year pages
            sub_links = self._find_meeting_subpages(soup)
            seen = {i.url for i in items}
            for link_url in sub_links[:10]:
                try:
                    sub_html = await self.fetch(link_url)
                    sub_soup = BeautifulSoup(sub_html, "lxml")
                    sub_items = self._parse_page(sub_soup, link_url)
                    for item in sub_items:
                        if item.url not in seen:
                            seen.add(item.url)
                            items.append(item)
                except Exception:
                    continue

        except Exception as e:
            logger.error("CRD scrape failed: %s", e)

        logger.info("CRD discovery: %d items found", len(items))
        return items

    def _find_meeting_subpages(self, soup: BeautifulSoup) -> list[str]:
        """Find links to committee-specific or archive meeting pages."""
        links: list[str] = []
        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True).lower()
            href = link["href"]
            if any(k in text for k in [
                "agenda", "minutes", "meeting", "committee",
                "board", "schedule", "202",
            ]):
                full = urljoin(self.base_url, href)
                # Stay within the CRD domain
                if "crd.bc.ca" in full and full not in links and full != self.base_url:
                    links.append(full)
        return links

    def _parse_page(
        self, soup: BeautifulSoup, source_url: str
    ) -> list[DiscoveredItem]:
        """Parse a CRD page for meeting document links."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        # Scan tables (CRD often uses table-based layouts)
        for row in soup.find_all("tr"):
            row_text = row.get_text(" ", strip=True)
            meeting_date = self._extract_date(row_text)

            for link in row.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                if full_url in seen_urls:
                    continue

                item_type = self._classify_link(link_text, href)
                if item_type:
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text or row_text[:100],
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_crd_meeting_type(row_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        # Scan list items, divs, etc.
        for container in soup.find_all(["li", "div", "article", "section"]):
            text = container.get_text(" ", strip=True)
            # Skip very large containers to avoid duplicating entire page
            if len(text) > 500:
                continue
            meeting_date = self._extract_date(text)

            for link in container.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                if full_url in seen_urls:
                    continue

                item_type = self._classify_link(link_text, href)
                if item_type:
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text or text[:100],
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_crd_meeting_type(text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        return items

    @staticmethod
    def _extract_date(text: str) -> str | None:
        patterns = [
            r"(\w+ \d{1,2},?\s*\d{4})",
            r"(\d{4}-\d{2}-\d{2})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return parse_civicweb_date(match.group(1))
        return None

    @staticmethod
    def _classify_link(link_text: str, href: str) -> str | None:
        text = link_text.lower()
        href_lower = href.lower()
        if "agenda" in text or "agenda" in href_lower:
            return "agenda"
        if "minute" in text or "minute" in href_lower:
            return "minutes"
        if any(k in text for k in ["video", "watch", "recording", "webcast"]):
            return "video"
        if any(k in href_lower for k in ["youtube.com", "youtu.be"]):
            return "video"
        if href_lower.endswith(".pdf") and any(
            k in text for k in ["board", "committee", "meeting", "regular", "special"]
        ):
            return "agenda"
        return None
