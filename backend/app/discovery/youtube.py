"""YouTube video discovery for council meetings.

Uses YouTube Data API v3 (or RSS feed fallback) to find new council meeting videos.
"""

import re
from datetime import datetime
from urllib.parse import urljoin
from xml.etree import ElementTree

from app.discovery.base import BaseScraper, DiscoveredItem


# YouTube RSS feed URL pattern (no API key needed)
YT_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

# Keywords that indicate a council meeting video
MEETING_KEYWORDS = [
    "council meeting",
    "public hearing",
    "committee of the whole",
    "regular meeting",
    "special meeting",
    "council session",
    "board meeting",
]


class YouTubeScraper(BaseScraper):
    """Discover council meeting videos via YouTube RSS feed (no API key required)."""

    def __init__(self, municipality: str, channel_id: str):
        # YouTube RSS doesn't need a base_url, but we set one for the feed
        super().__init__(municipality, f"https://www.youtube.com/channel/{channel_id}")
        self.channel_id = channel_id
        self.feed_url = YT_FEED_URL.format(channel_id=channel_id)

    async def discover(self) -> list[DiscoveredItem]:
        """Discover recent council meeting videos from YouTube RSS feed."""
        items = []

        try:
            xml_text = await self.fetch(self.feed_url)
            items = self._parse_feed(xml_text)
        except Exception as e:
            print(f"[YouTube] Feed fetch failed for {self.municipality}: {e}")

        return items

    def _parse_feed(self, xml_text: str) -> list[DiscoveredItem]:
        """Parse YouTube Atom feed XML for council meeting videos."""
        items = []
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "yt": "http://www.youtube.com/xml/schemas/2015",
            "media": "http://search.yahoo.com/mrss/",
        }

        try:
            root = ElementTree.fromstring(xml_text)
        except ElementTree.ParseError as e:
            print(f"[YouTube] XML parse error for {self.municipality}: {e}")
            return items

        for entry in root.findall("atom:entry", ns):
            title_el = entry.find("atom:title", ns)
            video_id_el = entry.find("yt:videoId", ns)
            published_el = entry.find("atom:published", ns)

            if title_el is None or video_id_el is None:
                continue

            title = title_el.text or ""
            video_id = video_id_el.text or ""
            published = published_el.text if published_el is not None else None

            # Filter: only include videos that look like council meetings
            if not self._is_meeting_video(title):
                continue

            # Parse the published date
            meeting_date = None
            if published:
                try:
                    dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    meeting_date = dt.strftime("%Y-%m-%d")
                except ValueError:
                    pass

            # Also try to extract meeting date from title
            title_date = self._extract_date_from_title(title)
            if title_date:
                meeting_date = title_date

            video_url = f"https://www.youtube.com/watch?v={video_id}"

            items.append(
                DiscoveredItem(
                    municipality=self.municipality,
                    title=title,
                    item_type="video",
                    url=video_url,
                    meeting_date=meeting_date,
                    meeting_type=self._classify_from_title(title),
                    video_url=video_url,
                    raw_metadata={
                        "video_id": video_id,
                        "channel_id": self.channel_id,
                        "published": published,
                    },
                )
            )

        return items

    @staticmethod
    def _is_meeting_video(title: str) -> bool:
        """Check if a video title indicates a council meeting."""
        title_lower = title.lower()
        return any(kw in title_lower for kw in MEETING_KEYWORDS)

    @staticmethod
    def _classify_from_title(title: str) -> str:
        """Classify meeting type from video title."""
        title_lower = title.lower()
        if "public hearing" in title_lower:
            return "public_hearing"
        if "special" in title_lower:
            return "special"
        if "committee" in title_lower:
            return "committee"
        return "regular"

    @staticmethod
    def _extract_date_from_title(title: str) -> str | None:
        """Try to extract a date from a video title like 'Council Meeting - March 9, 2026'."""
        patterns = [
            r"(\w+ \d{1,2},?\s*\d{4})",
            r"(\d{4}-\d{2}-\d{2})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
        ]
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                date_str = match.group(1)
                for fmt in ["%B %d, %Y", "%B %d %Y", "%b %d, %Y", "%Y-%m-%d", "%m/%d/%Y"]:
                    try:
                        return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                    except ValueError:
                        continue
        return None
