"""YouTube video discovery for council meetings.

Uses YouTube RSS feed for discovery + oEmbed/page scrape for timestamps.
Timestamps are extracted from video descriptions (chapter markers like "0:15:30 Public Hearing").
"""

import re
from datetime import datetime
from xml.etree import ElementTree

import httpx

from app.discovery.base import BaseScraper, DiscoveredItem


# YouTube RSS feed URL pattern (no API key needed)
YT_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

# oEmbed endpoint for getting video metadata
YT_OEMBED_URL = "https://www.youtube.com/oembed?url={video_url}&format=json"

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

# Regex for timestamp patterns in video descriptions
# Matches: "0:15:30 Public Hearing", "1:02:15 - Rezoning Application", "15:30 Budget Discussion"
TIMESTAMP_PATTERN = re.compile(
    r"(?:^|\n)\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–—]?\s*(.+?)(?:\n|$)",
    re.MULTILINE,
)


def parse_timestamps(text: str) -> list[dict]:
    """Extract timestamp chapters from video description text.

    Returns list of {"t": "0:15:30", "seconds": 930, "label": "Public Hearing - OCP Amendment"}.
    """
    timestamps = []
    for match in TIMESTAMP_PATTERN.finditer(text):
        time_str = match.group(1).strip()
        label = match.group(2).strip()

        # Skip very short labels (likely not real chapters)
        if len(label) < 3:
            continue

        # Convert to seconds for deep-link generation
        parts = time_str.split(":")
        if len(parts) == 3:
            seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            seconds = int(parts[0]) * 60 + int(parts[1])
        else:
            continue

        timestamps.append({
            "t": time_str,
            "seconds": seconds,
            "label": label,
        })

    return timestamps


def format_timestamps_for_embedding(timestamps: list[dict], video_url: str) -> str:
    """Format timestamps into text suitable for embedding/indexing.

    Produces text like:
    "At 0:15:30 (https://youtube.com/watch?v=X&t=930): Public Hearing - OCP Amendment"
    """
    if not timestamps:
        return ""

    lines = ["VIDEO CHAPTERS/TIMESTAMPS:"]
    for ts in timestamps:
        deep_link = f"{video_url}&t={ts['seconds']}"
        lines.append(f"  [{ts['t']}] {ts['label']} ({deep_link})")
    return "\n".join(lines)


async def fetch_video_description(video_id: str) -> str | None:
    """Fetch video description by scraping the watch page.

    YouTube doesn't expose descriptions via oEmbed, so we fetch the watch page
    and extract from the meta tag or JSON-LD.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        async with httpx.AsyncClient(
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            },
            follow_redirects=True,
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            html = resp.text

            # Strategy 1: Extract from meta description tag
            meta_match = re.search(
                r'<meta\s+name="description"\s+content="([^"]*)"', html
            )
            meta_desc = meta_match.group(1) if meta_match else ""

            # Strategy 2: Extract from ytInitialData JSON (has full description)
            json_match = re.search(
                r'"description":\s*\{"simpleText":\s*"([^"]*?)"\}', html
            )
            if json_match:
                # Unescape JSON string
                full_desc = json_match.group(1).replace("\\n", "\n").replace('\\"', '"')
                return full_desc

            # Strategy 3: Try shortDescription from ytInitialPlayerResponse
            short_match = re.search(
                r'"shortDescription":\s*"(.*?)(?<!\\)"', html, re.DOTALL
            )
            if short_match:
                full_desc = short_match.group(1).replace("\\n", "\n").replace('\\"', '"')
                return full_desc

            return meta_desc or None

    except Exception:
        return None


async def fetch_video_duration(video_id: str) -> str | None:
    """Try to extract video duration from the watch page."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            resp = await client.get(url)
            html = resp.text

            # Look for duration in ISO 8601 format from JSON-LD
            dur_match = re.search(r'"lengthSeconds":\s*"(\d+)"', html)
            if dur_match:
                total_seconds = int(dur_match.group(1))
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                if hours > 0:
                    return f"{hours}:{minutes:02d}:{seconds:02d}"
                return f"{minutes}:{seconds:02d}"
    except Exception:
        pass
    return None


class YouTubeScraper(BaseScraper):
    """Discover council meeting videos via YouTube RSS feed + timestamp extraction."""

    def __init__(self, municipality: str, channel_id: str):
        super().__init__(municipality, f"https://www.youtube.com/channel/{channel_id}")
        self.channel_id = channel_id
        self.feed_url = YT_FEED_URL.format(channel_id=channel_id)

    async def discover(self) -> list[DiscoveredItem]:
        """Discover recent council meeting videos from YouTube RSS feed.

        For each video found, also fetches the description to extract
        timestamp chapters (e.g., "0:15:30 Public Hearing - OCP Amendment").
        """
        items = []

        try:
            xml_text = await self.fetch(self.feed_url)
            items = await self._parse_feed(xml_text)
        except Exception as e:
            print(f"[YouTube] Feed fetch failed for {self.municipality}: {e}")

        return items

    async def _parse_feed(self, xml_text: str) -> list[DiscoveredItem]:
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

            # Fetch description and extract timestamps
            description = await fetch_video_description(video_id)
            timestamps = parse_timestamps(description) if description else []
            duration = await fetch_video_duration(video_id)

            # Build text content from description + timestamps for matching/embedding
            content_parts = [title]
            if description:
                content_parts.append(description)
            if timestamps:
                content_parts.append(
                    format_timestamps_for_embedding(timestamps, video_url)
                )

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
                        "description": description,
                        "timestamps": timestamps,
                        "duration": duration,
                        "content_for_embedding": "\n".join(content_parts),
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
