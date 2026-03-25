"""CivicWeb platform scraper.

CivicWeb (by Diligent) is used by many BC municipalities.
Portal structure:
  - /Portal/MeetingTypeList.aspx — lists meeting types (Regular Council, etc.)
  - /Portal/MeetingSchedule.aspx — upcoming/past meetings
  - /Portal/MeetingInformation.aspx?Id=XXXX — individual meeting with agenda/minutes links
  - /filepro/documents/ — document search
"""

import asyncio
import logging
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper, DiscoveredItem
from app.config import settings

logger = logging.getLogger(__name__)


# CivicWeb meeting type keywords for classification
# Ordered longest-first so "committee of the whole" matches before "committee"
MEETING_TYPE_MAP = [
    ("committee of the whole", "committee_of_the_whole"),
    ("public hearing", "public_hearing"),
    ("special", "special"),
    ("committee", "committee"),
    ("regular", "regular"),
    ("council", "regular"),
    ("board", "regular"),
]

# Broader date regex — covers most CivicWeb date formats in one pass
DATE_REGEX = re.compile(
    r"(?:(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s*)?"
    r"(\w+ \d{1,2},?\s*\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\w{3}-\d{4})"
)


def classify_meeting_type(title: str) -> str:
    title_lower = title.lower()
    for keyword, mtype in MEETING_TYPE_MAP:
        if keyword in title_lower:
            return mtype
    return "regular"


def parse_civicweb_date(date_str: str) -> str | None:
    """Parse various CivicWeb date formats to YYYY-MM-DD."""
    date_str = date_str.strip().rstrip(",")
    for fmt in [
        "%B %d, %Y",      # March 9, 2026
        "%B %d %Y",       # March 9 2026
        "%b %d, %Y",      # Mar 9, 2026
        "%b %d %Y",       # Mar 9 2026
        "%m/%d/%Y",        # 03/09/2026
        "%Y-%m-%d",        # 2026-03-09
        "%d-%b-%Y",        # 09-Mar-2026
        "%d-%B-%Y",        # 09-March-2026
        "%A, %B %d, %Y",  # Monday, March 9, 2026
    ]:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _extract_date(text: str) -> str | None:
    """Extract and parse the first date found in text."""
    match = DATE_REGEX.search(text)
    return parse_civicweb_date(match.group(1)) if match else None


def _classify_link(link_text: str, href: str) -> str | None:
    """Classify a link as agenda, minutes, or video based on text and href."""
    text = link_text.lower()
    href_lower = href.lower()

    if any(k in text for k in ["agenda", "agenda package"]) or "agenda" in href_lower:
        return "agenda"
    if any(k in text for k in ["minute", "minutes"]) or "minute" in href_lower:
        return "minutes"
    if any(k in text for k in ["video", "watch", "recording", "webcast"]):
        return "video"
    if any(k in href_lower for k in ["youtube.com", "youtu.be", "vimeo.com"]):
        return "video"
    return None


def _is_document_link(href: str) -> bool:
    """Check if a link points to a document or meeting information page."""
    href_lower = href.lower()
    return (
        href_lower.endswith(".pdf")
        or "document" in href_lower
        or "filepro" in href_lower
        or "filestream" in href_lower
        or "meetinginformation" in href_lower.replace(" ", "")
    )


class CivicWebScraper(BaseScraper):
    """Scraper for CivicWeb (Diligent) municipal portals.

    Uses a multi-strategy approach:
    1. MeetingSchedule.aspx — flat list of all meetings
    2. MeetingTypeList.aspx — follow links to per-type schedules
    3. MeetingInformation.aspx — drill into individual meeting pages
    4. Generic PDF link scan — last resort
    """

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meetings from CivicWeb portal."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        # Strategy 1: Try MeetingSchedule.aspx (lists all meetings with dates)
        schedule_items = await self._scrape_meeting_schedule()
        for item in schedule_items:
            if item.url not in seen_urls:
                seen_urls.add(item.url)
                items.append(item)

        # Strategy 2: Try MeetingTypeList.aspx — may find meetings schedule missed
        type_items = await self._scrape_meeting_type_list()
        for item in type_items:
            if item.url not in seen_urls:
                seen_urls.add(item.url)
                items.append(item)

        # Strategy 3: If both failed, try the base URL itself
        if not items:
            try:
                html = await self.fetch(self.base_url)
                soup = BeautifulSoup(html, "lxml")
                base_items = self._parse_meeting_list(soup, self.base_url)
                for item in base_items:
                    if item.url not in seen_urls:
                        seen_urls.add(item.url)
                        items.append(item)
            except Exception as e:
                logger.warning("Base URL scrape failed for %s: %s", self.municipality, e)

        logger.info(
            "CivicWeb discovery for %s: %d items found", self.municipality, len(items)
        )
        return items

    async def _scrape_meeting_schedule(self) -> list[DiscoveredItem]:
        """Scrape the meeting schedule page for upcoming/recent meetings."""
        parsed = urlparse(self.base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        url = urljoin(base, "/Portal/MeetingSchedule.aspx")
        items: list[DiscoveredItem] = []

        try:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "lxml")
            items = self._parse_meeting_list(soup, url)

            # Drill into individual MeetingInformation pages for more docs
            meeting_links = self._extract_meeting_info_links(soup, url)
            if meeting_links:
                detail_items = await self._scrape_meeting_detail_pages(meeting_links)
                items.extend(detail_items)

        except Exception as e:
            logger.warning("MeetingSchedule failed for %s: %s", self.municipality, e)

        return items

    async def _scrape_meeting_type_list(self) -> list[DiscoveredItem]:
        """Scrape the meeting type list and follow links to individual types."""
        parsed = urlparse(self.base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        url = urljoin(base, "/Portal/MeetingTypeList.aspx")
        items: list[DiscoveredItem] = []

        try:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "lxml")

            # Find all meeting type links
            type_links: list[str] = []
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "MeetingInformation" in href or "MeetingSchedule" in href:
                    full = urljoin(url, href)
                    if full not in type_links:
                        type_links.append(full)

            # Follow each meeting type link
            for type_url in type_links[:12]:  # Cap at 12 types
                try:
                    await asyncio.sleep(settings.request_delay_seconds * 0.5)
                    type_html = await self.fetch(type_url)
                    type_soup = BeautifulSoup(type_html, "lxml")
                    type_items = self._parse_meeting_list(type_soup, type_url)
                    items.extend(type_items)

                    # Also grab MeetingInformation links from the type page
                    detail_links = self._extract_meeting_info_links(type_soup, type_url)
                    if detail_links:
                        detail_items = await self._scrape_meeting_detail_pages(
                            detail_links[:8]
                        )
                        items.extend(detail_items)
                except Exception:
                    continue

        except Exception as e:
            logger.warning("MeetingTypeList failed for %s: %s", self.municipality, e)

        return items

    def _extract_meeting_info_links(
        self, soup: BeautifulSoup, source_url: str
    ) -> list[str]:
        """Extract links to individual MeetingInformation.aspx pages."""
        links: list[str] = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "MeetingInformation" in href and "Id=" in href:
                full = urljoin(source_url, href)
                if full not in links:
                    links.append(full)
        return links

    async def _scrape_meeting_detail_pages(
        self, urls: list[str]
    ) -> list[DiscoveredItem]:
        """Scrape individual MeetingInformation pages for agenda/minutes PDFs."""
        items: list[DiscoveredItem] = []
        for url in urls[:12]:
            try:
                await asyncio.sleep(settings.request_delay_seconds * 0.5)
                html = await self.fetch(url)
                soup = BeautifulSoup(html, "lxml")
                page_items = self._parse_meeting_list(soup, url)
                items.extend(page_items)
            except Exception as e:
                logger.debug("MeetingInformation page failed %s: %s", url, e)
                continue
        return items

    def _parse_meeting_list(
        self, soup: BeautifulSoup, source_url: str
    ) -> list[DiscoveredItem]:
        """Parse a CivicWeb page for meeting entries with agenda/minutes links."""
        items: list[DiscoveredItem] = []

        # Pattern 1: Table rows with meeting info
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 2:
                continue

            row_text = row.get_text(" ", strip=True)
            meeting_date = _extract_date(row_text)

            for link in row.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                item_type = _classify_link(link_text, href)
                if item_type:
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

        # Pattern 2: Div-based layout (newer CivicWeb versions)
        for div in soup.find_all(
            "div", class_=re.compile(r"meeting|agenda|schedule|document", re.I)
        ):
            div_text = div.get_text(" ", strip=True)
            meeting_date = _extract_date(div_text)

            for link in div.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                item_type = _classify_link(link_text, href)
                if item_type:
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text,
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(div_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        # Pattern 3: Generic link scan — find any PDF/document links
        if not items:
            for link in soup.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                if not _is_document_link(href):
                    continue

                item_type = _classify_link(link_text, href)
                if item_type:
                    parent_text = (
                        link.parent.get_text(" ", strip=True) if link.parent else ""
                    )
                    meeting_date = _extract_date(parent_text)

                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text,
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        return items

    async def scrape_meeting_page(self, meeting_url: str) -> list[DiscoveredItem]:
        """Scrape an individual meeting information page for all documents."""
        try:
            html = await self.fetch(meeting_url)
            soup = BeautifulSoup(html, "lxml")
            return self._parse_meeting_list(soup, meeting_url)
        except Exception as e:
            logger.error("Failed to scrape meeting page %s: %s", meeting_url, e)
            return []
