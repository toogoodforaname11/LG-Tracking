"""CivicWeb platform scraper.

CivicWeb (by Diligent) is used by many BC municipalities.
Portal structure:
  - /Portal/MeetingTypeList.aspx — lists meeting types (Regular Council, etc.)
  - /Portal/MeetingSchedule.aspx — upcoming/past meetings
  - /Portal/MeetingInformation.aspx?Id=XXXX — individual meeting with agenda/minutes links
  - /filepro/documents/ — document search
"""

import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper, DiscoveredItem


# CivicWeb meeting type keywords for classification
MEETING_TYPE_MAP = {
    "regular": "regular",
    "special": "special",
    "public hearing": "public_hearing",
    "committee": "committee",
    "committee of the whole": "committee_of_the_whole",
    "council": "regular",
    "board": "regular",
}


def classify_meeting_type(title: str) -> str:
    title_lower = title.lower()
    for keyword, mtype in MEETING_TYPE_MAP.items():
        if keyword in title_lower:
            return mtype
    return "regular"


def parse_civicweb_date(date_str: str) -> str | None:
    """Parse various CivicWeb date formats to YYYY-MM-DD."""
    date_str = date_str.strip()
    for fmt in [
        "%B %d, %Y",      # March 9, 2026
        "%b %d, %Y",      # Mar 9, 2026
        "%m/%d/%Y",        # 03/09/2026
        "%Y-%m-%d",        # 2026-03-09
        "%d-%b-%Y",        # 09-Mar-2026
        "%A, %B %d, %Y",  # Monday, March 9, 2026
    ]:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


class CivicWebScraper(BaseScraper):
    """Scraper for CivicWeb (Diligent) municipal portals."""

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meetings from CivicWeb portal."""
        items = []

        # Strategy 1: Try MeetingSchedule.aspx (lists all meetings with dates)
        schedule_items = await self._scrape_meeting_schedule()
        items.extend(schedule_items)

        # Strategy 2: If schedule didn't work, try MeetingTypeList.aspx
        if not items:
            items = await self._scrape_meeting_type_list()

        return items

    async def _scrape_meeting_schedule(self) -> list[DiscoveredItem]:
        """Scrape the meeting schedule page for upcoming/recent meetings."""
        url = urljoin(self.base_url, "/Portal/MeetingSchedule.aspx")
        items = []

        try:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "lxml")
            items = self._parse_meeting_list(soup, url)
        except Exception as e:
            # Log and try alternative URL patterns
            print(f"[CivicWeb] MeetingSchedule failed for {self.municipality}: {e}")

        return items

    async def _scrape_meeting_type_list(self) -> list[DiscoveredItem]:
        """Scrape the meeting type list and follow links to individual types."""
        url = urljoin(self.base_url, "/Portal/MeetingTypeList.aspx")
        items = []

        try:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "lxml")

            # Find all meeting type links
            type_links = []
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "MeetingInformation" in href or "MeetingSchedule" in href:
                    type_links.append(urljoin(url, href))

            # Follow each meeting type link
            for type_url in type_links[:10]:  # Cap at 10 types
                try:
                    type_html = await self.fetch(type_url)
                    type_soup = BeautifulSoup(type_html, "lxml")
                    type_items = self._parse_meeting_list(type_soup, type_url)
                    items.extend(type_items)
                except Exception:
                    continue

        except Exception as e:
            print(f"[CivicWeb] MeetingTypeList failed for {self.municipality}: {e}")

        return items

    def _parse_meeting_list(self, soup: BeautifulSoup, source_url: str) -> list[DiscoveredItem]:
        """Parse a CivicWeb page for meeting entries with agenda/minutes links."""
        items = []

        # CivicWeb uses tables and divs — try multiple selectors
        # Pattern 1: Table rows with meeting info
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 2:
                continue

            # Look for date + meeting title pattern
            row_text = row.get_text(" ", strip=True)
            date_match = re.search(
                r"(\w+ \d{1,2},\s*\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})",
                row_text,
            )
            meeting_date = parse_civicweb_date(date_match.group(1)) if date_match else None

            # Find document links (agenda, minutes PDFs)
            for link in row.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True).lower()
                full_url = urljoin(source_url, href)

                item_type = None
                if any(k in link_text for k in ["agenda", "agenda package"]):
                    item_type = "agenda"
                elif any(k in link_text for k in ["minute", "minutes"]):
                    item_type = "minutes"
                elif "video" in link_text or "watch" in link_text:
                    item_type = "video"

                if item_type:
                    title_text = link.get_text(strip=True) or row_text[:100]
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=title_text,
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(row_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        # Pattern 2: Div-based layout (newer CivicWeb versions)
        for div in soup.find_all("div", class_=re.compile(r"meeting|agenda|schedule", re.I)):
            div_text = div.get_text(" ", strip=True)
            date_match = re.search(
                r"(\w+ \d{1,2},\s*\d{4}|\d{4}-\d{2}-\d{2})",
                div_text,
            )
            meeting_date = parse_civicweb_date(date_match.group(1)) if date_match else None

            for link in div.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True).lower()
                full_url = urljoin(source_url, href)

                item_type = None
                if "agenda" in link_text:
                    item_type = "agenda"
                elif "minute" in link_text:
                    item_type = "minutes"

                if item_type:
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link.get_text(strip=True),
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(div_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        # Pattern 3: Generic link scan — find any PDF links with agenda/minutes keywords
        if not items:
            for link in soup.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True).lower()
                full_url = urljoin(source_url, href)

                if not (href.lower().endswith(".pdf") or "document" in href.lower()):
                    continue

                item_type = None
                if "agenda" in link_text or "agenda" in href.lower():
                    item_type = "agenda"
                elif "minute" in link_text or "minute" in href.lower():
                    item_type = "minutes"

                if item_type:
                    # Try to extract date from surrounding text
                    parent_text = link.parent.get_text(" ", strip=True) if link.parent else ""
                    date_match = re.search(
                        r"(\w+ \d{1,2},\s*\d{4}|\d{4}-\d{2}-\d{2})",
                        parent_text,
                    )
                    meeting_date = (
                        parse_civicweb_date(date_match.group(1)) if date_match else None
                    )

                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link.get_text(strip=True),
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
            print(f"[CivicWeb] Failed to scrape meeting page {meeting_url}: {e}")
            return []
