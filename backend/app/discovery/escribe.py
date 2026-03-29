"""eScribe platform scraper.

eScribe is used by some BC municipalities for meeting management.
Portal structure:
  - Main page at pub-{city}.escribemeetings.com lists upcoming/past meetings
  - Meeting detail pages contain agenda/minutes PDF links
  - Common URL patterns: /Meeting.aspx?Id=GUID, /FileStream.ashx
"""

import asyncio
import logging
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper, DiscoveredItem
from app.discovery.civicweb import parse_civicweb_date, classify_meeting_type
from app.config import settings

logger = logging.getLogger(__name__)

# eScribe meeting listing paths to try
ESCRIBE_PATHS = [
    "/SearchMeetings.aspx",
    "/Ede.aspx",
    "/Meeting.aspx",
    "",  # Root page itself
]

# Date regex for eScribe pages
DATE_RE = re.compile(
    r"(?:(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s*)?"
    r"(\w+ \d{1,2},?\s*\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})"
)


def _extract_date(text: str) -> str | None:
    """Extract and parse the first date found in text."""
    match = DATE_RE.search(text)
    return parse_civicweb_date(match.group(1)) if match else None


def _classify_link(link_text: str, href: str) -> str | None:
    """Classify a link as agenda, minutes, or video."""
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
    # eScribe-specific: FileStream links are usually PDFs
    if "filestream" in href_lower:
        return "agenda"
    return None


def _is_meeting_link(href: str) -> bool:
    """Check if a link points to an eScribe meeting detail page."""
    href_lower = href.lower()
    return any(k in href_lower for k in [
        "meeting.aspx", "meetingdetail", "filestream.ashx",
        ".pdf", "agenda", "minute",
    ])


class EScribeScraper(BaseScraper):
    """Generic scraper for eScribe meeting portals."""

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meeting documents from an eScribe portal."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        for path in ESCRIBE_PATHS:
            url = self.base_url.rstrip("/") + path
            try:
                resp = await self.client.get(url, follow_redirects=True)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                page_items = self._parse_meeting_list(soup, url)

                for item in page_items:
                    if item.url not in seen_urls:
                        seen_urls.add(item.url)
                        items.append(item)

                if items:
                    logger.info(
                        "%s: found %d items via %s",
                        self.municipality, len(items), path or "/",
                    )

            except Exception as e:
                logger.debug(
                    "%s: error fetching %s: %s",
                    self.municipality, url, e,
                )
                continue

            if items:
                break

            await asyncio.sleep(settings.request_delay_seconds)

        # If listing pages found meeting detail links, follow them
        if not items:
            items = await self._try_detail_pages(seen_urls)

        return items

    def _parse_meeting_list(
        self, soup: BeautifulSoup, source_url: str,
    ) -> list[DiscoveredItem]:
        """Parse a meeting listing page for document links."""
        items: list[DiscoveredItem] = []

        # Strategy 1: Look for table rows with meeting info
        for row in soup.find_all("tr"):
            row_text = row.get_text(" ", strip=True)
            date = _extract_date(row_text)
            meeting_type = classify_meeting_type(row_text)

            for link in row.find_all("a", href=True):
                href = link["href"]
                if not href or href.startswith("#") or href.startswith("javascript"):
                    continue

                abs_url = urljoin(source_url, href)
                link_text = link.get_text(strip=True)
                doc_type = _classify_link(link_text, abs_url)

                if doc_type:
                    title_parts = [self.municipality]
                    if meeting_type:
                        title_parts.append(meeting_type.replace("_", " ").title())
                    title_parts.append(doc_type.title())
                    if date:
                        title_parts.append(date)

                    items.append(DiscoveredItem(
                        municipality=self.municipality,
                        title=" - ".join(title_parts),
                        item_type=doc_type,
                        url=abs_url,
                        meeting_date=date,
                        meeting_type=meeting_type,
                    ))

        # Strategy 2: Look for any document links on the page
        if not items:
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if not href or href.startswith("#") or href.startswith("javascript"):
                    continue

                abs_url = urljoin(source_url, href)
                link_text = link.get_text(strip=True)
                doc_type = _classify_link(link_text, abs_url)

                if not doc_type:
                    continue

                # Try to find a date near this link
                parent = link.find_parent(["div", "li", "td", "section"])
                parent_text = parent.get_text(" ", strip=True) if parent else ""
                date = _extract_date(parent_text) or _extract_date(link_text)
                meeting_type = classify_meeting_type(parent_text or link_text)

                title_parts = [self.municipality]
                if meeting_type:
                    title_parts.append(meeting_type.replace("_", " ").title())
                title_parts.append(doc_type.title())
                if date:
                    title_parts.append(date)

                items.append(DiscoveredItem(
                    municipality=self.municipality,
                    title=" - ".join(title_parts),
                    item_type=doc_type,
                    url=abs_url,
                    meeting_date=date,
                    meeting_type=meeting_type,
                ))

        return items

    async def _try_detail_pages(
        self, seen_urls: set[str],
    ) -> list[DiscoveredItem]:
        """Follow meeting detail page links from the root page."""
        items: list[DiscoveredItem] = []
        root_url = self.base_url.rstrip("/") + "/"

        try:
            resp = await self.client.get(root_url, follow_redirects=True)
            if resp.status_code != 200:
                return items

            soup = BeautifulSoup(resp.text, "html.parser")

            # Collect meeting detail links
            detail_links: list[str] = []
            for link in soup.find_all("a", href=True):
                href = link["href"]
                abs_url = urljoin(root_url, href)
                if _is_meeting_link(href) and abs_url not in seen_urls:
                    # Only follow links within the same domain
                    if urlparse(abs_url).netloc == urlparse(root_url).netloc:
                        detail_links.append(abs_url)
                        seen_urls.add(abs_url)

            # Visit up to 20 detail pages
            for detail_url in detail_links[:20]:
                try:
                    detail_resp = await self.client.get(
                        detail_url, follow_redirects=True,
                    )
                    if detail_resp.status_code != 200:
                        continue

                    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
                    page_items = self._parse_meeting_list(detail_soup, detail_url)
                    for item in page_items:
                        if item.url not in seen_urls:
                            seen_urls.add(item.url)
                            items.append(item)

                    await asyncio.sleep(settings.request_delay_seconds)
                except Exception as e:
                    logger.debug(
                        "%s: error fetching detail %s: %s",
                        self.municipality, detail_url, e,
                    )

        except Exception as e:
            logger.debug("%s: error in detail pages: %s", self.municipality, e)

        return items
