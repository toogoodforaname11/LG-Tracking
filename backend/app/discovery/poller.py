"""Discovery poller — orchestrates scraping across all active sources."""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.municipality import Municipality, Source, ScrapeStatus, Platform, ScrapeRun
from app.models.document import Document, Meeting, DocType, MeetingType
from app.discovery.base import DiscoveredItem
from app.discovery.civicweb import CivicWebScraper
from app.discovery.youtube import YouTubeScraper
from app.config import settings
from app.services.instant_alerts import send_immediate_alerts_for_documents

logger = logging.getLogger(__name__)


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
            channel_id = None
            if source.scrape_config:
                try:
                    config = json.loads(source.scrape_config)
                    channel_id = config.get("channel_id")
                except json.JSONDecodeError as e:
                    logger.error(
                        "Invalid JSON in scrape_config for source %d (%s): %s",
                        source.id, source.label, e,
                    )
                    return []

            if not channel_id:
                # Fall back to extracting from URL like youtube.com/@CityofColwood
                channel_id = source.url.rstrip("/").split("/")[-1]

            scraper = YouTubeScraper(municipality.short_name, channel_id)
            return await scraper.discover()
        else:
            logger.warning(
                "Unsupported platform %s for source %d (%s/%s)",
                source.platform, source.id, municipality.short_name, source.label,
            )
            return []
    except Exception as e:
        logger.error(
            "Error polling source %d (%s/%s): %s",
            source.id, municipality.short_name, source.label, e,
        )
        return []
    finally:
        if scraper:
            await scraper.close()


async def store_discovered_items(
    db: AsyncSession, items: list[DiscoveredItem], source: Source, municipality: Municipality
) -> tuple[dict, list[Document]]:
    """Store discovered items in the database. Returns (stats, new_docs)."""
    stats = {"total": len(items), "new": 0, "existing": 0}
    new_docs: list[Document] = []

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
            existing_doc.last_checked_at = datetime.now(timezone.utc)
            continue

        # Find or create meeting record
        meeting_id = None
        if item.meeting_date:
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

        content_hash = hashlib.sha256(item.url.encode()).hexdigest()

        raw_text = None
        video_timestamps = None
        video_duration = None
        if item.item_type == "video" and item.raw_metadata:
            raw_text = item.raw_metadata.get("content_for_embedding")
            video_timestamps = item.raw_metadata.get("timestamps")
            video_duration = item.raw_metadata.get("duration")

        doc = Document(
            meeting_id=meeting_id,
            municipality_id=municipality.id,
            source_id=source.id,
            doc_type=DOC_TYPE_MAP.get(item.item_type, DocType.AGENDA),
            title=item.title,
            url=item.url,
            content_hash=content_hash,
            raw_text=raw_text,
            video_timestamps=video_timestamps,
            video_duration=video_duration,
            is_new=True,
            is_processed=False,
            first_seen_at=datetime.now(timezone.utc),
        )
        db.add(doc)
        new_docs.append(doc)
        stats["new"] += 1

    await db.commit()
    return stats, new_docs


async def run_discovery(db: AsyncSession, municipality_filter: str | None = None) -> dict:
    """Run discovery across all active sources.

    After polling, sends immediate alerts for any new documents to subscribers
    who have immediate_alerts enabled.

    Args:
        db: Database session
        municipality_filter: Optional short_name to only poll a specific municipality

    Returns:
        Summary dict with results per municipality.
    """
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
    all_new_docs: list[Document] = []

    for source, municipality in source_munis:
        muni_name = municipality.short_name
        logger.info("Polling %s / %s", muni_name, source.label)

        scrape_run = ScrapeRun(source_id=source.id)
        db.add(scrape_run)
        await db.flush()

        try:
            items = await poll_source(source, municipality)
            stats, new_docs = await store_discovered_items(db, items, source, municipality)
            all_new_docs.extend(new_docs)

            scrape_run.finished_at = datetime.now(timezone.utc)
            scrape_run.status = "success"
            scrape_run.documents_found = stats["total"]
            scrape_run.new_documents = stats["new"]

            source.scrape_status = ScrapeStatus.ACTIVE
            source.last_scraped_at = datetime.now(timezone.utc)
            source.last_error = None

            results[f"{muni_name}/{source.label}"] = stats
            logger.info("  %s/%s: %d items (%d new)", muni_name, source.label, stats["total"], stats["new"])

        except Exception as e:
            logger.error("Error during poll of %s/%s: %s", muni_name, source.label, e)
            scrape_run.finished_at = datetime.now(timezone.utc)
            scrape_run.status = "error"
            scrape_run.error_message = str(e)

            source.last_error = str(e)
            source.scrape_status = ScrapeStatus.BROKEN

            results[f"{muni_name}/{source.label}"] = {"error": str(e)}

        await db.commit()

        # Rate limiting between sources
        await asyncio.sleep(settings.request_delay_seconds)

    # Send immediate alerts for all new documents discovered in this run
    if all_new_docs:
        try:
            alert_stats = await send_immediate_alerts_for_documents(db, all_new_docs)
            results["_immediate_alerts"] = alert_stats
            logger.info("Immediate alerts: %d sent", alert_stats["alerts_sent"])
        except Exception as e:
            logger.error("Error sending immediate alerts: %s", e)
            results["_immediate_alerts"] = {"error": str(e)}

    return results
