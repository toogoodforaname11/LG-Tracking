"""Base scraper with shared HTTP client logic."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

import httpx

from app.config import settings


@dataclass
class DiscoveredItem:
    """A single discovered meeting document (agenda, minutes, or video)."""

    municipality: str
    title: str
    item_type: str  # agenda, minutes, video
    url: str
    meeting_date: str | None = None  # YYYY-MM-DD
    meeting_type: str | None = None  # regular, public_hearing, committee, etc.
    pdf_url: str | None = None
    video_url: str | None = None
    content_hash: str | None = None
    raw_metadata: dict = field(default_factory=dict)
    discovered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class BaseScraper(ABC):
    """Abstract base for all platform scrapers."""

    def __init__(self, municipality: str, base_url: str):
        self.municipality = municipality
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            timeout=settings.scrape_timeout_seconds,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            },
            follow_redirects=True,
        )

    async def close(self):
        await self.client.aclose()

    async def fetch(self, url: str) -> str:
        """Fetch a URL with retries."""
        last_error = None
        for attempt in range(3):
            try:
                resp = await self.client.get(url)
                resp.raise_for_status()
                return resp.text
            except httpx.HTTPError as e:
                last_error = e
                if attempt < 2:
                    import asyncio
                    await asyncio.sleep(settings.request_delay_seconds * (attempt + 1))
        raise last_error

    @abstractmethod
    async def discover(self) -> list[DiscoveredItem]:
        """Discover new meeting items. Returns list of discovered items."""
        ...
