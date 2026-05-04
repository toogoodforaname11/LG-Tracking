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
from app.discovery.base import BaseScraper, DiscoveredItem
from app.discovery.civicweb import CivicWebScraper
from app.discovery.granicus import GranicusScraper
from app.discovery.escribe import EScribeScraper
from app.discovery.youtube import YouTubeScraper, resolve_channel_id, _CHANNEL_ID_RE
from app.discovery.custom_bc_municipal import make_generic_scraper, GENERIC_SCRAPER_KEYWORDS
# Substantive custom scrapers with real parsing logic (not just keyword configs)
from app.discovery.custom_saanich import SaanichScraper
from app.discovery.custom_sidney import SidneyScraper
from app.discovery.custom_esquimalt import EsquimaltScraper
from app.discovery.custom_viewroyal import ViewRoyalScraper
from app.discovery.custom_langford import LangfordScraper
from app.discovery.custom_highlands import HighlandsScraper
from app.discovery.custom_crd import CRDScraper
from app.config import settings
from app.services.instant_alerts import send_immediate_alerts_for_documents

logger = logging.getLogger(__name__)

# Number of consecutive poll failures before a source is marked BROKEN.
BROKEN_THRESHOLD = 5

# Maximum number of sources polled concurrently.  Keeps total outbound
# connections reasonable while dramatically reducing overall poll time
# compared to sequential execution.
MAX_CONCURRENT_POLLS = 8


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


# Substantive custom scrapers with municipality-specific parsing logic.
# These override discover() or _parse_page() beyond simple keyword config.
CUSTOM_SCRAPER_MAP: dict[str, type] = {
    "Saanich": SaanichScraper,
    "Sidney": SidneyScraper,
    "Esquimalt": EsquimaltScraper,
    "View Royal": ViewRoyalScraper,
    "Langford": LangfordScraper,
    "Highlands": HighlandsScraper,
    "CRD": CRDScraper,
}


def _get_custom_scraper(short_name: str, url: str) -> BaseScraper | None:
    """Look up and instantiate a custom scraper for a municipality.

    First checks the substantive scraper map (for municipalities with custom
    parsing logic), then falls back to the config-driven generic scraper
    factory (for municipalities that only need extra subpage keywords).
    """
    scraper_cls = CUSTOM_SCRAPER_MAP.get(short_name)
    if scraper_cls:
        return scraper_cls(short_name, url)
    return make_generic_scraper(short_name, url)


async def poll_source(source: Source, municipality: Municipality) -> list[DiscoveredItem]:
    """Poll a single source for new items."""
    scraper = None

    try:
        if source.platform == Platform.CIVICWEB:
            scraper = CivicWebScraper(municipality.short_name, source.url)
            return await scraper.discover()
        elif source.platform == Platform.YOUTUBE:
            channel_id = None
            config: dict = {}
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

            # If the cached id isn't a real UCxxx channel id (or is missing),
            # resolve it from the URL. The historical fallback of splitting
            # the URL on "/" produced a literal "@handle" which YouTube's RSS
            # endpoint rejects — that path is gone.
            if not channel_id or not _CHANNEL_ID_RE.match(channel_id):
                resolved = await resolve_channel_id(source.url)
                if not resolved:
                    logger.warning(
                        "YouTube source %d (%s/%s): could not resolve channel id from %s; skipping",
                        source.id, municipality.short_name, source.label, source.url,
                    )
                    return []
                channel_id = resolved
                # Cache the resolved id back into scrape_config so we only pay
                # the resolution cost once per source.
                config["channel_id"] = channel_id
                source.scrape_config = json.dumps(config)

            scraper = YouTubeScraper(municipality.short_name, channel_id)
            return await scraper.discover()
        elif source.platform == Platform.GRANICUS:
            scraper = GranicusScraper(municipality.short_name, source.url)
            return await scraper.discover()
        elif source.platform == Platform.ESCRIBE:
            scraper = EScribeScraper(municipality.short_name, source.url)
            return await scraper.discover()
        elif source.platform == Platform.CUSTOM:
            scraper = _get_custom_scraper(municipality.short_name, source.url)
            if scraper:
                return await scraper.discover()
            logger.error(
                "No custom scraper registered for %s (source %d: %s). "
                "Add an entry to CUSTOM_SCRAPER_MAP in poller.py.",
                municipality.short_name, source.id, source.label,
            )
            return []
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

        # Extract content fields early — needed for both hash and document creation.
        raw_text = None
        video_timestamps = None
        video_duration = None
        if item.item_type == "video" and item.raw_metadata:
            raw_text = item.raw_metadata.get("content_for_embedding")
            video_timestamps = item.raw_metadata.get("timestamps")
            video_duration = item.raw_metadata.get("duration")

        if existing_doc:
            stats["existing"] += 1
            existing_doc.last_checked_at = datetime.now(timezone.utc)

            # Detect content changes at the same URL (revised agendas/minutes).
            hash_source = raw_text or item.title or item.url
            new_hash = hashlib.sha256(hash_source.encode()).hexdigest()

            # Legacy migration: rows created before the content-hash fix
            # stored sha256(url).  If the existing hash matches the old URL-
            # based scheme, silently upgrade to the new content-based hash
            # without marking for reprocessing — the document content has not
            # actually changed, only the hashing strategy has.
            legacy_url_hash = hashlib.sha256(item.url.encode()).hexdigest()
            if existing_doc.content_hash == legacy_url_hash and new_hash != legacy_url_hash:
                existing_doc.content_hash = new_hash
                if raw_text:
                    existing_doc.raw_text = raw_text
                continue

            if existing_doc.content_hash and new_hash != existing_doc.content_hash:
                existing_doc.content_hash = new_hash
                existing_doc.is_processed = False
                existing_doc.is_new = True
                if raw_text:
                    existing_doc.raw_text = raw_text
                stats.setdefault("updated", 0)
                stats["updated"] += 1
            continue

        # Find or create meeting record
        meeting_id = None
        if item.meeting_date:
            meeting_type_enum = MEETING_TYPE_MAP.get(item.meeting_type or "regular")
            result = await db.execute(
                select(Meeting).where(
                    Meeting.municipality_id == municipality.id,
                    Meeting.meeting_date == item.meeting_date,
                    Meeting.meeting_type == meeting_type_enum,
                )
            )
            meeting = result.scalar_one_or_none()
            if not meeting:
                meeting = Meeting(
                    municipality_id=municipality.id,
                    title=item.title,
                    meeting_date=item.meeting_date,
                    meeting_type=meeting_type_enum,
                    source_url=item.url,
                )
                db.add(meeting)
                await db.flush()
            meeting_id = meeting.id

        # Hash from actual content, not URL — enables revision detection.
        hash_source = raw_text or item.title or item.url
        content_hash = hashlib.sha256(hash_source.encode()).hexdigest()

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


async def _poll_one(
    sem: asyncio.Semaphore,
    source: Source,
    municipality: Municipality,
) -> tuple[Source, Municipality, list[DiscoveredItem] | None, Exception | None]:
    """Poll a single source with semaphore-bounded concurrency.

    Returns (source, municipality, items_or_None, error_or_None).
    HTTP fetching happens concurrently; DB writes are done by the caller.
    """
    async with sem:
        try:
            items = await poll_source(source, municipality)
            return source, municipality, items, None
        except Exception as e:
            return source, municipality, None, e


async def run_discovery(db: AsyncSession, municipality_filter: str | None = None) -> dict:
    """Run discovery across all active sources.

    Sources are polled concurrently (bounded by MAX_CONCURRENT_POLLS) for
    speed, then results are stored sequentially through the shared DB
    session to avoid concurrency issues with SQLAlchemy.

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
        .where(Source.scrape_status.in_([ScrapeStatus.ACTIVE, ScrapeStatus.PENDING, ScrapeStatus.BROKEN]))
        .where(Municipality.is_active.is_(True))
    )
    if municipality_filter:
        query = query.where(Municipality.short_name == municipality_filter)

    result = await db.execute(query)
    source_munis = result.all()

    if not source_munis:
        return {}

    # Phase 1: Poll all sources concurrently (HTTP only, no DB writes).
    sem = asyncio.Semaphore(MAX_CONCURRENT_POLLS)
    tasks = [
        _poll_one(sem, source, municipality)
        for source, municipality in source_munis
    ]
    poll_results = await asyncio.gather(*tasks)

    # Phase 2: Store results sequentially through the shared DB session.
    results = {}
    all_new_docs: list[Document] = []

    for source, municipality, items, error in poll_results:
        muni_name = municipality.short_name

        scrape_run = ScrapeRun(source_id=source.id)
        db.add(scrape_run)
        await db.flush()

        if error is None and items is not None:
            try:
                stats, new_docs = await store_discovered_items(db, items, source, municipality)
                all_new_docs.extend(new_docs)

                scrape_run.finished_at = datetime.now(timezone.utc)
                scrape_run.status = "success"
                scrape_run.documents_found = stats["total"]
                scrape_run.new_documents = stats["new"]

                source.scrape_status = ScrapeStatus.ACTIVE
                source.last_scraped_at = datetime.now(timezone.utc)
                source.last_error = None
                source.consecutive_failures = 0

                results[f"{muni_name}/{source.label}"] = stats
                logger.info("  %s/%s: %d items (%d new)", muni_name, source.label, stats["total"], stats["new"])
            except Exception as e:
                # store_discovered_items failed — treat as poll error
                error = e

        if error is not None:
            logger.error("Error during poll of %s/%s: %s", muni_name, source.label, error)
            scrape_run.finished_at = datetime.now(timezone.utc)
            scrape_run.status = "error"
            scrape_run.error_message = str(error)

            source.last_error = str(error)
            source.consecutive_failures = (source.consecutive_failures or 0) + 1
            if source.consecutive_failures >= BROKEN_THRESHOLD:
                source.scrape_status = ScrapeStatus.BROKEN
                logger.warning(
                    "%s/%s marked BROKEN after %d consecutive failures",
                    muni_name, source.label, source.consecutive_failures,
                )

            results[f"{muni_name}/{source.label}"] = {"error": str(error)}

        await db.commit()

    # Phase 3: Send immediate alerts for all new documents discovered in this run.
    if all_new_docs:
        try:
            alert_stats = await send_immediate_alerts_for_documents(db, all_new_docs)
            results["_immediate_alerts"] = alert_stats
            logger.info("Immediate alerts: %d sent", alert_stats["alerts_sent"])
        except Exception as e:
            logger.error("Error sending immediate alerts: %s", e)
            results["_immediate_alerts"] = {"error": str(e)}

    return results
