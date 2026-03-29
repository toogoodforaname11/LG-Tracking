"""Granicus platform scraper.

Granicus is used by many BC municipalities for meeting management.
Portal structure:
  - Main page lists meeting types or recent meetings
  - Individual meeting pages contain agenda/minutes PDF links
  - Some portals use /ViewPublisher.php or similar endpoints
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

# Granicus meeting landing page patterns
GRANICUS_PATHS = [
    "/ViewPublisher.php",
    "/ViewPublisher.php?view_id=1",
    "/ViewPublisher.php?view_id=2",
    "/GeneratedAgendaViewer.php",
    "/MetaViewer.php",
    "",  # Root page itself
]

# Broader date regex
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
    # Granicus-specific: MetaViewer and GeneratedAgendaViewer links
    if "metaviewer" in href_lower:
        if "minute" in text:
            return "minutes"
        return "agenda"
    if "generatedagendaviewer" in href_lower:
        return "agenda"
    return None


class GranicusScraper(BaseScraper):
    """Generic scraper for Granicus municipal portals.

    Uses a multi-strategy approach:
    1. Try ViewPublisher.php pages (meeting lists)
    2. Parse table/list layouts for agenda/minutes links
    3. Fall back to generic PDF link scanning
    """

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meetings from a Granicus portal."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        parsed = urlparse(self.base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        # Try each known Granicus path
        for path in GRANICUS_PATHS:
            url = urljoin(base, path) if path else self.base_url
            try:
                html = await self.fetch(url)
                soup = BeautifulSoup(html, "lxml")
                page_items = self._parse_page(soup, url)
                for item in page_items:
                    if item.url not in seen_urls:
                        seen_urls.add(item.url)
                        items.append(item)

                # Follow links to individual meeting pages
                meeting_links = self._extract_meeting_links(soup, url)
                for meeting_url in meeting_links[:12]:
                    try:
                        await asyncio.sleep(settings.request_delay_seconds * 0.5)
                        m_html = await self.fetch(meeting_url)
                        m_soup = BeautifulSoup(m_html, "lxml")
                        m_items = self._parse_page(m_soup, meeting_url)
                        for item in m_items:
                            if item.url not in seen_urls:
                                seen_urls.add(item.url)
                                items.append(item)
                    except Exception:
                        continue

                if items:
                    break  # Found items, no need to try more paths

            except Exception as e:
                logger.debug("Granicus path %s failed for %s: %s", path, self.municipality, e)
                continue

        logger.info("Granicus discovery for %s: %d items found", self.municipality, len(items))
        return items

    def _extract_meeting_links(self, soup: BeautifulSoup, source_url: str) -> list[str]:
        """Extract links to individual meeting detail pages."""
        links: list[str] = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            href_lower = href.lower()
            if any(k in href_lower for k in [
                "generatedagendaviewer", "metaviewer", "meetingdetail",
                "viewpublisher", "clip_id=",
            ]):
                full = urljoin(source_url, href)
                if full not in links:
                    links.append(full)
        return links

    def _parse_page(self, soup: BeautifulSoup, source_url: str) -> list[DiscoveredItem]:
        """Parse a Granicus page for meeting document links."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        # Pattern 1: Table rows
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

                if full_url in seen_urls:
                    continue

                item_type = _classify_link(link_text, href)
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

        # Pattern 2: List items and divs
        for container in soup.find_all(["li", "div", "article", "section"]):
            text = container.get_text(" ", strip=True)
            if len(text) > 500:
                continue
            meeting_date = _extract_date(text)

            for link in container.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)

                if full_url in seen_urls:
                    continue

                item_type = _classify_link(link_text, href)
                if item_type:
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text or text[:100],
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        # Pattern 3: Generic PDF/document link scan
        if not items:
            for link in soup.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True)
                full_url = urljoin(source_url, href)
                href_lower = href.lower()

                if full_url in seen_urls:
                    continue

                if not (
                    href_lower.endswith(".pdf")
                    or "metaviewer" in href_lower
                    or "generatedagendaviewer" in href_lower
                    or "document" in href_lower
                ):
                    continue

                item_type = _classify_link(link_text, href)
                if item_type:
                    parent_text = link.parent.get_text(" ", strip=True) if link.parent else ""
                    meeting_date = _extract_date(parent_text)
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link_text or "Meeting Document",
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": source_url},
                        )
                    )

        return items
