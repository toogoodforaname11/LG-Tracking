"""Discovery poller — orchestrates scraping across all active sources."""

import asyncio
import hashlib
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.municipality import Municipality, Source, ScrapeStatus, Platform, ScrapeRun
from app.models.document import Document, Meeting, DocType, MeetingType
from app.discovery.base import DiscoveredItem
from app.discovery.civicweb import CivicWebScraper
from app.discovery.youtube import YouTubeScraper
from app.config import settings


# Map item_type strings to DocType enum
DOC_TYPE_MAP = {
    "agenda": DocType.AGENDA,
    "minutes": DocType.MINUTES,
    "video": DocType.VIDEO,
}

# Map meeting_type strings to MeetingType enum
MEETING_TYPE_MAP = {
    "regular": MeetingType.REGULAR,
    "special": MeetingType.SPECIAL,
    "public_hearing": MeetingType.PUBLIC_HEARING,
    "committee": MeetingType.COMMITTEE,
    "committee_of_the_whole": MeetingType.COW,
}


async def poll_source(source: Source, municipality: Municipality) -> list[DiscoveredItem]:
    """Poll a single source for new items."""
    scraper = None

    try:
        if source.platform == Platform.CIVICWEB:
            scraper = CivicWebScraper(municipality.short_name, source.url)
            return await scraper.discover()
        elif source.platform == Platform.YOUTUBE:
            # Extract channel ID from URL or scrape_config
            channel_id = None
            if source.scrape_config:
                import json
                config = json.loads(source.scrape_config)
                channel_id = config.get("channel_id")
            if not channel_id:
                # Try to extract from URL like youtube.com/@CityofColwood
                channel_id = source.url.split("/")[-1]

            scraper = YouTubeScraper(municipality.short_name, channel_id)
            return await scraper.discover()
        else:
            print(f"[Poller] Unsupported platform {source.platform} for {municipality.short_name}")
            return []
    except Exception as e:
        print(f"[Poller] Error polling {source.label}: {e}")
        return []
    finally:
        if scraper:
            await scraper.close()


async def store_discovered_items(
    db: AsyncSession, items: list[DiscoveredItem], source: Source, municipality: Municipality
) -> dict:
    """Store discovered items in the database. Returns stats."""
    stats = {"total": len(items), "new": 0, "existing": 0}

    for item in items:
        # Check if document already exists (by URL)
        result = await db.execute(
            select(Document).where(
                Document.municipality_id == municipality.id,
                Document.url == item.url,
            )
        )
        existing_doc = result.scalar_one_or_none()

        if existing_doc:
            stats["existing"] += 1
            # Update last_checked timestamp
            existing_doc.last_checked_at = datetime.utcnow()
            continue

        # Find or create meeting record
        meeting_id = None
        if item.meeting_date:
            meeting_title = f"{item.meeting_type or 'regular'} - {item.meeting_date}"
            result = await db.execute(
                select(Meeting).where(
                    Meeting.municipality_id == municipality.id,
                    Meeting.meeting_date == item.meeting_date,
                )
            )
            meeting = result.scalar_one_or_none()
            if not meeting:
                meeting = Meeting(
                    municipality_id=municipality.id,
                    title=item.title,
                    meeting_date=item.meeting_date,
                    meeting_type=MEETING_TYPE_MAP.get(item.meeting_type or "regular"),
                    source_url=item.url,
                )
                db.add(meeting)
                await db.flush()
            meeting_id = meeting.id

        # Compute content hash from URL (will be updated with actual content later)
        content_hash = hashlib.sha256(item.url.encode()).hexdigest()

        doc = Document(
            meeting_id=meeting_id,
            municipality_id=municipality.id,
            source_id=source.id,
            doc_type=DOC_TYPE_MAP.get(item.item_type, DocType.AGENDA),
            title=item.title,
            url=item.url,
            content_hash=content_hash,
            is_new=True,
            is_processed=False,
            first_seen_at=datetime.utcnow(),
        )
        db.add(doc)
        stats["new"] += 1

    await db.commit()
    return stats


async def run_discovery(db: AsyncSession, municipality_filter: str | None = None) -> dict:
    """Run discovery across all active sources.

    Args:
        db: Database session
        municipality_filter: Optional short_name to only poll a specific municipality

    Returns:
        Summary dict with results per municipality.
    """
    # Get all active sources with their municipalities
    query = (
        select(Source, Municipality)
        .join(Municipality, Source.municipality_id == Municipality.id)
        .where(Source.scrape_status.in_([ScrapeStatus.ACTIVE, ScrapeStatus.PENDING]))
        .where(Municipality.is_active.is_(True))
    )
    if municipality_filter:
        query = query.where(Municipality.short_name == municipality_filter)

    result = await db.execute(query)
    source_munis = result.all()

    results = {}

    for source, municipality in source_munis:
        muni_name = municipality.short_name
        print(f"[Poller] Polling {source.label}...")

        # Create scrape run record
        scrape_run = ScrapeRun(source_id=source.id)
        db.add(scrape_run)
        await db.flush()

        try:
            items = await poll_source(source, municipality)

            # Store items
            stats = await store_discovered_items(db, items, source, municipality)

            # Update scrape run
            scrape_run.finished_at = datetime.utcnow()
            scrape_run.status = "success"
            scrape_run.documents_found = stats["total"]
            scrape_run.new_documents = stats["new"]

            # Update source status
            source.scrape_status = ScrapeStatus.ACTIVE
            source.last_scraped_at = datetime.utcnow()
            source.last_error = None

            results[f"{muni_name}/{source.label}"] = stats
            print(f"  Found {stats['total']} items ({stats['new']} new)")

        except Exception as e:
            scrape_run.finished_at = datetime.utcnow()
            scrape_run.status = "error"
            scrape_run.error_message = str(e)

            source.last_error = str(e)
            source.scrape_status = ScrapeStatus.BROKEN

            results[f"{muni_name}/{source.label}"] = {"error": str(e)}
            print(f"  Error: {e}")

        await db.commit()

        # Rate limiting between sources
        await asyncio.sleep(settings.request_delay_seconds)

    return results
