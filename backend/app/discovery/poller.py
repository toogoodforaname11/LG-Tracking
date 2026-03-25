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
from app.discovery.youtube import YouTubeScraper
from app.discovery.custom_saanich import SaanichScraper
from app.discovery.custom_sidney import SidneyScraper
from app.discovery.custom_esquimalt import EsquimaltScraper
from app.discovery.custom_viewroyal import ViewRoyalScraper
from app.discovery.custom_langford import LangfordScraper
from app.discovery.custom_highlands import HighlandsScraper
from app.discovery.custom_crd import CRDScraper
from app.discovery.custom_100milehouse import HundredMileHouseScraper
from app.discovery.custom_armstrong import ArmstrongScraper
from app.discovery.custom_castlegar import CastlegarScraper
from app.discovery.custom_enderby import EnderbyScraper
from app.discovery.custom_fernie import FernieScraper
from app.discovery.custom_grandforks import GrandForksScraper
from app.discovery.custom_nelson import NelsonScraper
from app.discovery.custom_princerupert import PrinceRupertScraper
from app.discovery.custom_quesnel import QuesnelScraper
from app.discovery.custom_salmonarm import SalmonArmScraper
from app.discovery.custom_surrey import SurreyScraper
from app.discovery.custom_terrace import TerraceScraper
from app.discovery.custom_trail import TrailScraper
from app.discovery.custom_williamslake import WilliamsLakeScraper
from app.discovery.custom_ainsworthhotsprings import AinsworthHotSpringsScraper
from app.discovery.custom_alertbay import AlertBayScraper
from app.discovery.custom_ashcroft import AshcroftScraper
from app.discovery.custom_balfour import BalfourScraper
from app.discovery.custom_barriere import BarriereScraper
from app.discovery.custom_cachecreek import CacheCreekScraper
from app.discovery.custom_canalflats import CanalFlatsScraper
from app.discovery.custom_chase import ChaseScraper
from app.discovery.custom_chetwynd import ChetwyndScraper
from app.discovery.custom_christinalake import ChristinaLakeScraper
from app.discovery.custom_clearwater import ClearwaterScraper
from app.discovery.custom_clinton import ClintonScraper
from app.discovery.custom_coldstream import ColdstreamScraper
from app.discovery.custom_cranbrook import CranbrookScraper
from app.discovery.custom_creston import CrestonScraper
from app.discovery.custom_cumberland import CumberlandScraper
from app.discovery.custom_elkford import ElkfordScraper
from app.discovery.custom_fortnelson import FortNelsonScraper
from app.discovery.custom_fortstjames import FortStJamesScraper
from app.discovery.custom_fruitvale import FruitvaleScraper
from app.discovery.custom_gibsons import GibsonsScraper
from app.discovery.custom_goldriver import GoldRiverScraper
from app.discovery.custom_golden import GoldenScraper
from app.discovery.custom_granisle import GranisleScraper
from app.discovery.custom_greenwood import GreenwoodScraper
from app.discovery.custom_harrisonhotsprings import HarrisonHotSpringsScraper
from app.discovery.custom_hazelton import HazeltonScraper
from app.discovery.custom_hope import HopeScraper
from app.discovery.custom_houston import HoustonScraper
from app.discovery.custom_hudsonshope import HudsonsHopeScraper
from app.discovery.custom_invermere import InvermereScraper
from app.discovery.custom_kaslo import KasloScraper
from app.discovery.custom_kent import KentScraper
from app.discovery.custom_keremeos import KeremeosScraper
from app.discovery.custom_kimberley import KimberleyScraper
from app.discovery.custom_kitimat import KitimatScraper
from app.discovery.custom_lillooet import LillooetScraper
from app.discovery.custom_lionsbay import LionsBayScraper
from app.discovery.custom_loganlake import LoganLakeScraper
from app.discovery.custom_lumby import LumbyScraper
from app.discovery.custom_mackenzie import MackenzieScraper
from app.discovery.custom_mcbride import McBrideScraper
from app.discovery.custom_midway import MidwayScraper
from app.discovery.custom_montrose import MontroseScraper
from app.discovery.custom_nakusp import NakuspScraper
from app.discovery.custom_newdenver import NewDenverScraper
from app.discovery.custom_newhazelton import NewHazeltonScraper
from app.discovery.custom_northernrockies import NorthernRockiesScraper
from app.discovery.custom_pemberton import PembertonScraper
from app.discovery.custom_portedward import PortEdwardScraper
from app.discovery.custom_porthardy import PortHardyScraper
from app.discovery.custom_portmcneill import PortMcNeillScraper
from app.discovery.custom_princeton import PrincetonScraper
from app.discovery.custom_radiumhotsprings import RadiumHotSpringsScraper
from app.discovery.custom_revelstoke import RevelstokeScraper
from app.discovery.custom_riondel import RiondelScraper
from app.discovery.custom_rossland import RosslandScraper
from app.discovery.custom_salmo import SalmoScraper
from app.discovery.custom_sicamous import SicamousScraper
from app.discovery.custom_silverton import SilvertonScraper
from app.discovery.custom_slocan import SlocanScraper
from app.discovery.custom_smithers import SmithersScraper
from app.discovery.custom_spallumcheen import SpallumcheenScraper
from app.discovery.custom_sparwood import SparwoodScraper
from app.discovery.custom_stewart import StewartScraper
from app.discovery.custom_tahsis import TahsisScraper
from app.discovery.custom_telkwa import TelkwaScraper
from app.discovery.custom_tumblerridge import TumblerRidgeScraper
from app.discovery.custom_valemount import ValemountScraper
from app.discovery.custom_vanderhoof import VanderhoofScraper
from app.discovery.custom_warfield import WarfieldScraper
from app.discovery.custom_wells import WellsScraper
from app.discovery.custom_zeballos import ZeballosScraper
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


# Registry of custom scrapers keyed by municipality short_name
CUSTOM_SCRAPER_MAP: dict[str, type] = {
    # CRD municipalities
    "Saanich": SaanichScraper,
    "Sidney": SidneyScraper,
    "Esquimalt": EsquimaltScraper,
    "View Royal": ViewRoyalScraper,
    "Langford": LangfordScraper,
    "Highlands": HighlandsScraper,
    "CRD": CRDScraper,
    # BC municipalities — Batch 1+2
    "100 Mile House": HundredMileHouseScraper,
    "Armstrong": ArmstrongScraper,
    "Castlegar": CastlegarScraper,
    "Enderby": EnderbyScraper,
    # BC municipalities — Phase 3
    "Fernie": FernieScraper,
    "Grand Forks": GrandForksScraper,
    "Nelson": NelsonScraper,
    # BC municipalities — Phase 4
    "Prince Rupert": PrinceRupertScraper,
    "Quesnel": QuesnelScraper,
    "Salmon Arm": SalmonArmScraper,
    "Surrey": SurreyScraper,
    "Terrace": TerraceScraper,
    "Trail": TrailScraper,
    "Williams Lake": WilliamsLakeScraper,
    # BC municipalities — Phases 7-11
    "Ainsworth Hot Springs": AinsworthHotSpringsScraper,
    "Alert Bay": AlertBayScraper,
    "Ashcroft": AshcroftScraper,
    "Balfour": BalfourScraper,
    "Barriere": BarriereScraper,
    "Cache Creek": CacheCreekScraper,
    "Canal Flats": CanalFlatsScraper,
    "Chase": ChaseScraper,
    "Chetwynd": ChetwyndScraper,
    "Christina Lake": ChristinaLakeScraper,
    "Clearwater": ClearwaterScraper,
    "Clinton": ClintonScraper,
    "Coldstream": ColdstreamScraper,
    "Cranbrook": CranbrookScraper,
    "Creston": CrestonScraper,
    "Cumberland": CumberlandScraper,
    "Elkford": ElkfordScraper,
    "Fort Nelson": FortNelsonScraper,
    "Fort St. James": FortStJamesScraper,
    "Fruitvale": FruitvaleScraper,
    "Gibsons": GibsonsScraper,
    "Gold River": GoldRiverScraper,
    "Golden": GoldenScraper,
    "Granisle": GranisleScraper,
    "Greenwood": GreenwoodScraper,
    "Harrison Hot Springs": HarrisonHotSpringsScraper,
    "Hazelton": HazeltonScraper,
    "Hope": HopeScraper,
    "Houston": HoustonScraper,
    "Hudson's Hope": HudsonsHopeScraper,
    "Invermere": InvermereScraper,
    "Kaslo": KasloScraper,
    "Kent": KentScraper,
    "Keremeos": KeremeosScraper,
    "Kimberley": KimberleyScraper,
    "Kitimat": KitimatScraper,
    "Lillooet": LillooetScraper,
    "Lions Bay": LionsBayScraper,
    "Logan Lake": LoganLakeScraper,
    "Lumby": LumbyScraper,
    "Mackenzie": MackenzieScraper,
    "McBride": McBrideScraper,
    "Midway": MidwayScraper,
    "Montrose": MontroseScraper,
    "Nakusp": NakuspScraper,
    "New Denver": NewDenverScraper,
    "New Hazelton": NewHazeltonScraper,
    "Northern Rockies": NorthernRockiesScraper,
    "Pemberton": PembertonScraper,
    "Port Edward": PortEdwardScraper,
    "Port Hardy": PortHardyScraper,
    "Port McNeill": PortMcNeillScraper,
    "Princeton": PrincetonScraper,
    "Radium Hot Springs": RadiumHotSpringsScraper,
    "Revelstoke": RevelstokeScraper,
    "Riondel": RiondelScraper,
    "Rossland": RosslandScraper,
    "Salmo": SalmoScraper,
    "Sicamous": SicamousScraper,
    "Silverton": SilvertonScraper,
    "Slocan": SlocanScraper,
    "Smithers": SmithersScraper,
    "Spallumcheen": SpallumcheenScraper,
    "Sparwood": SparwoodScraper,
    "Stewart": StewartScraper,
    "Tahsis": TahsisScraper,
    "Telkwa": TelkwaScraper,
    "Tumbler Ridge": TumblerRidgeScraper,
    "Valemount": ValemountScraper,
    "Vanderhoof": VanderhoofScraper,
    "Warfield": WarfieldScraper,
    "Wells": WellsScraper,
    "Zeballos": ZeballosScraper,
}


def _get_custom_scraper(short_name: str, url: str) -> BaseScraper | None:
    """Look up and instantiate a custom scraper for a municipality."""
    scraper_cls = CUSTOM_SCRAPER_MAP.get(short_name)
    if scraper_cls:
        return scraper_cls(short_name, url)
    return None


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
        elif source.platform == Platform.GRANICUS:
            scraper = GranicusScraper(municipality.short_name, source.url)
            return await scraper.discover()
        elif source.platform == Platform.CUSTOM:
            scraper = _get_custom_scraper(municipality.short_name, source.url)
            if scraper:
                return await scraper.discover()
            logger.warning(
                "No custom scraper for %s (source %d: %s)",
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
