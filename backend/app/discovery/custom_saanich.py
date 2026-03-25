"""Custom scraper for District of Saanich.

Source URL: https://www.saanich.ca/EN/main/local-government/mayor-council/schedule-agendas-minutes.html
Saanich publishes agendas and minutes on their municipal website with links to PDF documents.
"""

import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper, DiscoveredItem
from app.discovery.civicweb import parse_civicweb_date, classify_meeting_type

logger = logging.getLogger(__name__)


class SaanichScraper(BaseScraper):
    """Scraper for District of Saanich council agendas and minutes."""

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meeting documents from the Saanich agendas/minutes page."""
        items: list[DiscoveredItem] = []

        try:
            html = await self.fetch(self.base_url)
            soup = BeautifulSoup(html, "lxml")
            items = self._parse_page(soup)
        except Exception as e:
            logger.error("Saanich scrape failed: %s", e)

        # Also try to find sub-pages linked from the main page
        if not items:
            items = await self._try_subpages()

        logger.info("Saanich discovery: %d items found", len(items))
        return items

    def _parse_page(self, soup: BeautifulSoup) -> list[DiscoveredItem]:
        """Parse the Saanich agendas/minutes page for meeting documents."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        # Saanich uses a table/list layout with links to agenda and minutes PDFs
        # Look for tables first
        for row in soup.find_all("tr"):
            row_text = row.get_text(" ", strip=True)
            meeting_date = self._extract_date(row_text)

            for link in row.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True).lower()
                full_url = urljoin(self.base_url, href)

                if full_url in seen_urls:
                    continue

                item_type = self._classify_link(link_text, href)
                if item_type:
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link.get_text(strip=True) or row_text[:100],
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(row_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": self.base_url},
                        )
                    )

        # Also scan for any list items or div sections with agenda/minutes links
        for container in soup.find_all(["li", "div", "section", "article"]):
            container_text = container.get_text(" ", strip=True)
            meeting_date = self._extract_date(container_text)

            for link in container.find_all("a", href=True):
                href = link["href"]
                link_text = link.get_text(strip=True).lower()
                full_url = urljoin(self.base_url, href)

                if full_url in seen_urls:
                    continue

                item_type = self._classify_link(link_text, href)
                if item_type:
                    seen_urls.add(full_url)
                    items.append(
                        DiscoveredItem(
                            municipality=self.municipality,
                            title=link.get_text(strip=True),
                            item_type=item_type,
                            url=full_url,
                            meeting_date=meeting_date,
                            meeting_type=classify_meeting_type(container_text),
                            pdf_url=full_url if full_url.lower().endswith(".pdf") else None,
                            raw_metadata={"source_page": self.base_url},
                        )
                    )

        return items

    async def _try_subpages(self) -> list[DiscoveredItem]:
        """Follow links from the main page that might contain meeting lists."""
        items: list[DiscoveredItem] = []
        try:
            html = await self.fetch(self.base_url)
            soup = BeautifulSoup(html, "lxml")

            subpage_links: list[str] = []
            for link in soup.find_all("a", href=True):
                href = link["href"]
                text = link.get_text(strip=True).lower()
                if any(k in text for k in ["agenda", "minutes", "schedule", "meeting"]):
                    full = urljoin(self.base_url, href)
                    if full != self.base_url and full not in subpage_links:
                        subpage_links.append(full)

            for sub_url in subpage_links[:6]:
                try:
                    sub_html = await self.fetch(sub_url)
                    sub_soup = BeautifulSoup(sub_html, "lxml")
                    sub_items = self._parse_page(sub_soup)
                    items.extend(sub_items)
                except Exception:
                    continue
        except Exception as e:
            logger.debug("Saanich subpage scan failed: %s", e)
        return items

    @staticmethod
    def _extract_date(text: str) -> str | None:
        """Extract date from text."""
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
        """Classify a link as agenda, minutes, or video."""
        text = link_text.lower()
        href_lower = href.lower()
        if "agenda" in text or "agenda" in href_lower:
            return "agenda"
        if "minute" in text or "minute" in href_lower:
            return "minutes"
        if any(k in text for k in ["video", "watch", "recording"]):
            return "video"
        if any(k in href_lower for k in ["youtube.com", "youtu.be"]):
            return "video"
        # Catch bare PDF links near meeting content
        if href_lower.endswith(".pdf") and any(
            k in text for k in ["council", "meeting", "regular", "special", "hearing"]
        ):
            return "agenda"
        return None
