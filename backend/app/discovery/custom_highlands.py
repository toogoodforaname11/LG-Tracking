"""Custom scraper for District of Highlands.

Source URL: https://www.highlands.ca/local-government/council
Highlands publishes council agendas and minutes on their local government page.
"""

import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.discovery.base import BaseScraper, DiscoveredItem
from app.discovery.civicweb import parse_civicweb_date, classify_meeting_type

logger = logging.getLogger(__name__)


class HighlandsScraper(BaseScraper):
    """Scraper for District of Highlands council agendas and minutes."""

    async def discover(self) -> list[DiscoveredItem]:
        """Discover meeting documents from the Highlands council page."""
        items: list[DiscoveredItem] = []

        try:
            html = await self.fetch(self.base_url)
            soup = BeautifulSoup(html, "lxml")

            # Find links to agenda/minutes subpages
            sub_links = self._find_meeting_links(soup)
            if sub_links:
                for link_url in sub_links[:8]:
                    try:
                        sub_html = await self.fetch(link_url)
                        sub_soup = BeautifulSoup(sub_html, "lxml")
                        sub_items = self._parse_page(sub_soup, link_url)
                        seen = {i.url for i in items}
                        for item in sub_items:
                            if item.url not in seen:
                                items.append(item)
                    except Exception:
                        continue

            # Also parse the main page
            main_items = self._parse_page(soup, self.base_url)
            seen = {i.url for i in items}
            for item in main_items:
                if item.url not in seen:
                    items.append(item)

        except Exception as e:
            logger.error("Highlands scrape failed: %s", e)

        logger.info("Highlands discovery: %d items found", len(items))
        return items

    def _find_meeting_links(self, soup: BeautifulSoup) -> list[str]:
        """Find links to agenda/minutes pages."""
        links: list[str] = []
        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True).lower()
            href = link["href"]
            if any(k in text for k in [
                "agenda", "minutes", "council meeting", "schedule",
            ]):
                full = urljoin(self.base_url, href)
                if full not in links and full != self.base_url:
                    links.append(full)
        return links

    def _parse_page(
        self, soup: BeautifulSoup, source_url: str
    ) -> list[DiscoveredItem]:
        """Parse a page for meeting document links."""
        items: list[DiscoveredItem] = []
        seen_urls: set[str] = set()

        for container in soup.find_all(["tr", "li", "div", "article", "section", "p"]):
            text = container.get_text(" ", strip=True)
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
                            meeting_type=classify_meeting_type(text),
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
        if any(k in text for k in ["video", "watch", "recording"]):
            return "video"
        if any(k in href_lower for k in ["youtube.com", "youtu.be"]):
            return "video"
        if href_lower.endswith(".pdf") and any(
            k in text for k in ["council", "meeting", "regular", "special"]
        ):
            return "agenda"
        return None
