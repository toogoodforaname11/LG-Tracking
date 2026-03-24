"""Seed the sources registry with CRD municipalities and their known data sources."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.municipality import (
    Municipality,
    Source,
    GovType,
    Platform,
    SourceType,
    ScrapeStatus,
)

# Complete CRD municipality registry with confirmed sources
CRD_MUNICIPALITIES = [
    {
        "name": "City of Colwood",
        "short_name": "Colwood",
        "gov_type": GovType.CITY,
        "region": "CRD",
        "website_url": "https://www.colwood.ca/",
        "population": 18961,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://colwood.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Colwood CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://colwood.civicweb.net/filepro/documents/",
                "label": "Colwood CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofColwood",
                "label": "Colwood YouTube Council Meetings",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        "name": "City of Victoria",
        "short_name": "Victoria",
        "gov_type": GovType.CITY,
        "region": "CRD",
        "website_url": "https://www.victoria.ca/",
        "population": 91867,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://victoria.civicweb.net/portal/",
                "label": "Victoria CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://victoria.civicweb.net/portal/",
                "label": "Victoria CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Saanich",
        "short_name": "Saanich",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.saanich.ca/",
        "population": 117735,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.saanich.ca/EN/main/local-government/mayor-council/schedule-agendas-minutes.html",
                "label": "Saanich Agendas & Minutes",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        "name": "District of Central Saanich",
        "short_name": "Central Saanich",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.centralsaanich.ca/",
        "population": 18576,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://centralsaanich.civicweb.net/portal/",
                "label": "Central Saanich CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://centralsaanich.civicweb.net/portal/",
                "label": "Central Saanich CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of North Saanich",
        "short_name": "North Saanich",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://northsaanich.ca/",
        "population": 12220,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://northsaanich.civicweb.net/portal/",
                "label": "North Saanich CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://northsaanich.civicweb.net/portal/",
                "label": "North Saanich CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Sidney",
        "short_name": "Sidney",
        "gov_type": GovType.TOWN,
        "region": "CRD",
        "website_url": "https://www.sidney.ca/",
        "population": 12405,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.sidney.ca/government/",
                "label": "Sidney Council Agendas",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        "name": "District of Oak Bay",
        "short_name": "Oak Bay",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.oakbay.ca/",
        "population": 18094,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://oakbay.civicweb.net/portal/",
                "label": "Oak Bay CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://oakbay.civicweb.net/portal/",
                "label": "Oak Bay CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Township of Esquimalt",
        "short_name": "Esquimalt",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.esquimalt.ca/",
        "population": 17655,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.esquimalt.ca/municipal-hall/council/agendas-minutes",
                "label": "Esquimalt Agendas & Minutes",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        "name": "Town of View Royal",
        "short_name": "View Royal",
        "gov_type": GovType.TOWN,
        "region": "CRD",
        "website_url": "https://www.viewroyal.ca/",
        "population": 11575,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.viewroyal.ca/EN/main/municipal.html",
                "label": "View Royal Council Agendas",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        "name": "City of Langford",
        "short_name": "Langford",
        "gov_type": GovType.CITY,
        "region": "CRD",
        "website_url": "https://langford.ca/",
        "population": 46584,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://langford.ca/city-hall/",
                "label": "Langford Council Agendas",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        "name": "District of Metchosin",
        "short_name": "Metchosin",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.metchosin.ca/",
        "population": 5169,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://metchosin.civicweb.net/portal/",
                "label": "Metchosin CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://metchosin.civicweb.net/portal/",
                "label": "Metchosin CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Sooke",
        "short_name": "Sooke",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.sooke.ca/",
        "population": 15054,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://sooke.civicweb.net/portal/",
                "label": "Sooke CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://sooke.civicweb.net/portal/",
                "label": "Sooke CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Highlands",
        "short_name": "Highlands",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.highlands.ca/",
        "population": 2373,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.highlands.ca/local-government/council",
                "label": "Highlands Council Agendas",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        "name": "Capital Regional District",
        "short_name": "CRD",
        "gov_type": GovType.REGIONAL_DISTRICT,
        "region": "CRD",
        "website_url": "https://www.crd.bc.ca/",
        "population": 430800,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.crd.bc.ca/about/board-committees/board-committee-meetings",
                "label": "CRD Board Agendas",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
]


async def seed_registry(db: AsyncSession) -> dict:
    """Seed the registry with CRD municipalities and sources.

    Returns a summary of what was created vs already existed.
    """
    stats = {"municipalities_created": 0, "municipalities_existed": 0, "sources_created": 0}

    for muni_data in CRD_MUNICIPALITIES:
        sources_data = muni_data.pop("sources")

        # Check if municipality already exists
        result = await db.execute(
            select(Municipality).where(Municipality.short_name == muni_data["short_name"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            stats["municipalities_existed"] += 1
            muni = existing
        else:
            muni = Municipality(**muni_data)
            db.add(muni)
            await db.flush()  # Get the ID
            stats["municipalities_created"] += 1

        # Add sources that don't exist yet
        for source_data in sources_data:
            result = await db.execute(
                select(Source).where(
                    Source.municipality_id == muni.id,
                    Source.url == source_data["url"],
                )
            )
            if not result.scalar_one_or_none():
                source = Source(municipality_id=muni.id, **source_data)
                db.add(source)
                stats["sources_created"] += 1

        # Restore sources_data for potential re-runs
        muni_data["sources"] = sources_data

    await db.commit()
    return stats
