"""Seed the sources registry with BC and Alberta municipalities and their known data sources."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.municipality import (
    Municipality,
    Source,
    GovType,
    Platform,
    SourceType,
    ScrapeStatus,
    PROVINCE_BC,
    PROVINCE_AB,
    PROVINCE_ON,
    TIER_UPPER,
    TIER_LOWER,
    TIER_SINGLE,
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
                "scrape_status": ScrapeStatus.ACTIVE,
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
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-victoria.escribemeetings.com",
                "label": "Victoria eScribe Agendas",
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
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://saanich.ca.granicus.com",
                "label": "Saanich Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
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
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://centralsaanich.ca.granicus.com",
                "label": "Central Saanich Granicus Agendas",
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
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://northsaanich.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "North Saanich CivicWeb Meeting List",
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
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://sidney.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Sidney CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://sidney.civicweb.net/filepro/documents/",
                "label": "Sidney CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
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
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://oakbay.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Oak Bay CivicWeb Meeting List",
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
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://esquimalt.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Esquimalt CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://esquimalt.civicweb.net/filepro/documents/",
                "label": "Esquimalt CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
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
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://viewroyal.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "View Royal CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://viewroyal.civicweb.net/filepro/documents/",
                "label": "View Royal CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
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
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://langford.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Langford CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://langford.civicweb.net/filepro/documents/",
                "label": "Langford CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
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
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://metchosin.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Metchosin CivicWeb Meeting List",
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
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://sooke.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Sooke CivicWeb Meeting List",
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
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://highlands.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Highlands CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://highlands.civicweb.net/filepro/documents/",
                "label": "Highlands CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
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
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 1 – 10 municipalities (Colwood already in CRD list above)
BC_MUNICIPALITIES_BATCH_1 = [
    {
        "name": "District of 100 Mile House",
        "short_name": "100 Mile House",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.100milehouse.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.100milehouse.com/council-meetings",
                "label": "100 Mile House Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Abbotsford",
        "short_name": "Abbotsford",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.abbotsford.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://abbotsford.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Abbotsford CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://abbotsford.civicweb.net/filepro/documents/",
                "label": "Abbotsford CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Armstrong",
        "short_name": "Armstrong",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.armstrong.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.armstrong.ca/council",
                "label": "Armstrong Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Burnaby",
        "short_name": "Burnaby",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.burnaby.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://burnaby.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Burnaby CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://burnaby.civicweb.net/filepro/documents/",
                "label": "Burnaby CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Campbell River",
        "short_name": "Campbell River",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.campbellriver.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://campbellriver.ca.granicus.com",
                "label": "Campbell River Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Castlegar",
        "short_name": "Castlegar",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.castlegar.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.castlegar.ca/council",
                "label": "Castlegar Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Chilliwack",
        "short_name": "Chilliwack",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.chilliwack.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@ChilliwackCity",
                "label": "Chilliwack YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    # Colwood – already present in CRD_MUNICIPALITIES, skipped.
    {
        "name": "City of Coquitlam",
        "short_name": "Coquitlam",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.coquitlam.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://coquitlam.ca.granicus.com",
                "label": "Coquitlam Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 2 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_2 = [
    {
        "name": "City of Duncan",
        "short_name": "Duncan",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.duncan.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://duncan.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Duncan CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://duncan.civicweb.net/filepro/documents/",
                "label": "Duncan CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Enderby",
        "short_name": "Enderby",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.enderby.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.enderby.ca/council",
                "label": "Enderby Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Fernie",
        "short_name": "Fernie",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.fernie.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.fernie.ca/council-meetings",
                "label": "Fernie Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Fort St. John",
        "short_name": "Fort St. John",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.fortstjohn.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://fortstjohn.ca.granicus.com",
                "label": "Fort St. John Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Grand Forks",
        "short_name": "Grand Forks",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.grandforks.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.grandforks.ca/council",
                "label": "Grand Forks Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Kamloops",
        "short_name": "Kamloops",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.kamloops.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofKamloops",
                "label": "Kamloops YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Kelowna",
        "short_name": "Kelowna",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.kelowna.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://kelowna.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Kelowna CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://kelowna.civicweb.net/filepro/documents/",
                "label": "Kelowna CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Langley City",
        "short_name": "Langley City",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.langleycity.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://langley.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Langley City CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://langley.civicweb.net/filepro/documents/",
                "label": "Langley City CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Township of Langley",
        "short_name": "Langley Township",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.tol.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@TownshipofLangley",
                "label": "Langley Township YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Maple Ridge",
        "short_name": "Maple Ridge",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.mapleridge.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://mapleridge.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Maple Ridge CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://mapleridge.civicweb.net/filepro/documents/",
                "label": "Maple Ridge CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 3 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_3 = [
    {
        "name": "City of Mission",
        "short_name": "Mission",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.mission.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://mission.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Mission CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://mission.civicweb.net/filepro/documents/",
                "label": "Mission CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Nanaimo",
        "short_name": "Nanaimo",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.nanaimo.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofNanaimo",
                "label": "Nanaimo YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Nelson",
        "short_name": "Nelson",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.nelson.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.nelson.ca/council",
                "label": "Nelson Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of New Westminster",
        "short_name": "New Westminster",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.newwestcity.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://newwestcity.ca.granicus.com",
                "label": "New Westminster Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of North Vancouver",
        "short_name": "North Vancouver City",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.cnv.org/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://northvancouver.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "North Vancouver City CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://northvancouver.civicweb.net/filepro/documents/",
                "label": "North Vancouver City CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of North Vancouver",
        "short_name": "North Vancouver District",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.dnv.org/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@DistrictofNorthVancouver",
                "label": "North Vancouver District YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Penticton",
        "short_name": "Penticton",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.penticton.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://penticton.ca.granicus.com",
                "label": "Penticton Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Port Coquitlam",
        "short_name": "Port Coquitlam",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.portcoquitlam.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://portcoquitlam.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Port Coquitlam CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://portcoquitlam.civicweb.net/filepro/documents/",
                "label": "Port Coquitlam CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Prince George",
        "short_name": "Prince George",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.princegeorge.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofPrinceGeorge",
                "label": "Prince George YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 4 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_4 = [
    {
        "name": "City of Prince Rupert",
        "short_name": "Prince Rupert",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.princerupert.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.princerupert.ca/council-meetings",
                "label": "Prince Rupert Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Quesnel",
        "short_name": "Quesnel",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.quesnel.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.quesnel.ca/council",
                "label": "Quesnel Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Richmond",
        "short_name": "Richmond",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.richmond.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofRichmondBC",
                "label": "Richmond YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Salmon Arm",
        "short_name": "Salmon Arm",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.salmonarm.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.salmonarm.ca/council",
                "label": "Salmon Arm Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://salmonarm.ca.granicus.com",
                "label": "Salmon Arm Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Surrey",
        "short_name": "Surrey",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.surrey.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.surrey.ca/council",
                "label": "Surrey Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Terrace",
        "short_name": "Terrace",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.terrace.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.terrace.ca/council",
                "label": "Terrace Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Trail",
        "short_name": "Trail",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.trail.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.trail.ca/council",
                "label": "Trail Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Vancouver",
        "short_name": "Vancouver",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.vancouver.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@VanCityClerk",
                "label": "Vancouver YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Vernon",
        "short_name": "Vernon",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.vernon.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://vernon.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Vernon CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://vernon.civicweb.net/filepro/documents/",
                "label": "Vernon CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 5 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_5 = [
    {
        "name": "City of West Kelowna",
        "short_name": "West Kelowna",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.westkelownacity.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://westkelowna.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "West Kelowna CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://westkelowna.civicweb.net/filepro/documents/",
                "label": "West Kelowna CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of West Vancouver",
        "short_name": "West Vancouver",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.westvancouver.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@WestVanDistrict",
                "label": "West Vancouver YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of White Rock",
        "short_name": "White Rock",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.whiterockcity.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://whiterock.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "White Rock CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://whiterock.civicweb.net/filepro/documents/",
                "label": "White Rock CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Williams Lake",
        "short_name": "Williams Lake",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.williamslake.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.williamslake.ca/council",
                "label": "Williams Lake Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 6 – remaining municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_6 = [
    {
        "name": "City of Courtenay",
        "short_name": "Courtenay",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.courtenay.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://courtenay.ca.granicus.com",
                "label": "Courtenay Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Comox",
        "short_name": "Comox",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.comox.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://comox.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Comox CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://comox.civicweb.net/filepro/documents/",
                "label": "Comox CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Cumberland",
        "short_name": "Cumberland",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.cumberland.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.cumberland.ca/council",
                "label": "Cumberland Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Port Alberni",
        "short_name": "Port Alberni",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.portalberni.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://portalberni.ca.granicus.com",
                "label": "Port Alberni Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Parksville",
        "short_name": "Parksville",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.parksville.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://parksville.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Parksville CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://parksville.civicweb.net/filepro/documents/",
                "label": "Parksville CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Qualicum Beach",
        "short_name": "Qualicum Beach",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.qualicumbeach.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://qualicumbeach.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Qualicum Beach CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://qualicumbeach.civicweb.net/filepro/documents/",
                "label": "Qualicum Beach CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Ladysmith",
        "short_name": "Ladysmith",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.ladysmith.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://ladysmith.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Ladysmith CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://ladysmith.civicweb.net/filepro/documents/",
                "label": "Ladysmith CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 7 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_7 = [
    {
        "name": "City of Powell River",
        "short_name": "Powell River",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.powellriver.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://powellriver.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Powell River CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://powellriver.civicweb.net/filepro/documents/",
                "label": "Powell River CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Squamish",
        "short_name": "Squamish",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.squamish.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://squamish.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Squamish CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://squamish.civicweb.net/filepro/documents/",
                "label": "Squamish CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Resort Municipality of Whistler",
        "short_name": "Whistler",
        "gov_type": GovType.MOUNTAIN_RESORT,
        "region": "BC",
        "website_url": "https://www.whistler.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://whistler.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Whistler CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://whistler.civicweb.net/filepro/documents/",
                "label": "Whistler CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Revelstoke",
        "short_name": "Revelstoke",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.revelstoke.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.revelstoke.ca/council",
                "label": "Revelstoke Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Golden",
        "short_name": "Golden",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.golden.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.golden.ca/council",
                "label": "Golden Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Cranbrook",
        "short_name": "Cranbrook",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.cranbrook.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.cranbrook.ca/council",
                "label": "Cranbrook Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Kimberley",
        "short_name": "Kimberley",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.kimberley.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.kimberley.ca/council",
                "label": "Kimberley Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Rossland",
        "short_name": "Rossland",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.rossland.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.rossland.ca/council",
                "label": "Rossland Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Sparwood",
        "short_name": "Sparwood",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.sparwood.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.sparwood.ca/council",
                "label": "Sparwood Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Elkford",
        "short_name": "Elkford",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.elkford.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.elkford.ca/council",
                "label": "Elkford Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 8 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_8 = [
    {
        "name": "City of Port Moody",
        "short_name": "Port Moody",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.portmoody.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://portmoody.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Port Moody CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://portmoody.civicweb.net/filepro/documents/",
                "label": "Port Moody CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Pitt Meadows",
        "short_name": "Pitt Meadows",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.pittmeadows.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://pittmeadows.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Pitt Meadows CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://pittmeadows.civicweb.net/filepro/documents/",
                "label": "Pitt Meadows CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Hope",
        "short_name": "Hope",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.hope.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.hope.ca/council",
                "label": "Hope Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Kent",
        "short_name": "Kent",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.kentbc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.kentbc.ca/council",
                "label": "Kent Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Harrison Hot Springs",
        "short_name": "Harrison Hot Springs",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.harrisonhotsprings.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.harrisonhotsprings.ca/council",
                "label": "Harrison Hot Springs Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Lions Bay",
        "short_name": "Lions Bay",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.lionsbay.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.lionsbay.ca/council",
                "label": "Lions Bay Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Bowen Island Municipality",
        "short_name": "Bowen Island",
        "gov_type": GovType.ISLAND_MUNICIPALITY,
        "region": "BC",
        "website_url": "https://www.bowenislandmunicipality.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://bowenisland.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Bowen Island CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://bowenisland.civicweb.net/filepro/documents/",
                "label": "Bowen Island CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Gibsons",
        "short_name": "Gibsons",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.gibsons.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.gibsons.ca/council",
                "label": "Gibsons Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Sechelt",
        "short_name": "Sechelt",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.sechelt.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://sechelt.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Sechelt CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://sechelt.civicweb.net/filepro/documents/",
                "label": "Sechelt CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Pemberton",
        "short_name": "Pemberton",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.pemberton.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.pemberton.ca/council",
                "label": "Pemberton Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 9 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_9 = [
    {
        "name": "District of Summerland",
        "short_name": "Summerland",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.summerland.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://summerland.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Summerland CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://summerland.civicweb.net/filepro/documents/",
                "label": "Summerland CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Peachland",
        "short_name": "Peachland",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.peachland.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://peachland.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Peachland CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://peachland.civicweb.net/filepro/documents/",
                "label": "Peachland CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Lake Country",
        "short_name": "Lake Country",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.lakecountry.bc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://lakecountry.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Lake Country CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://lakecountry.civicweb.net/filepro/documents/",
                "label": "Lake Country CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Township of Spallumcheen",
        "short_name": "Spallumcheen",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.spallumcheen.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.spallumcheen.ca/council",
                "label": "Spallumcheen Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Coldstream",
        "short_name": "Coldstream",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.coldstream.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.coldstream.ca/council",
                "label": "Coldstream Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Lumby",
        "short_name": "Lumby",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.lumby.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.lumby.ca/council",
                "label": "Lumby Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Sicamous",
        "short_name": "Sicamous",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.sicamous.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.sicamous.ca/council",
                "label": "Sicamous Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 10 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_10 = [
    {
        "name": "District of Kitimat",
        "short_name": "Kitimat",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.kitimat.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.kitimat.ca/council",
                "label": "Kitimat Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Smithers",
        "short_name": "Smithers",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.smithers.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.smithers.ca/council",
                "label": "Smithers Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Houston",
        "short_name": "Houston",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.houston.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.houston.ca/council",
                "label": "Houston Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Vanderhoof",
        "short_name": "Vanderhoof",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.vanderhoof.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.vanderhoof.ca/council",
                "label": "Vanderhoof Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Mackenzie",
        "short_name": "Mackenzie",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.mackenzie.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.mackenzie.ca/council",
                "label": "Mackenzie Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Fort St. James",
        "short_name": "Fort St. James",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.fortstjames.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.fortstjames.ca/council",
                "label": "Fort St. James Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Dawson Creek",
        "short_name": "Dawson Creek",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.dawsoncreek.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.GRANICUS,
                "source_type": SourceType.AGENDA,
                "url": "https://dawsoncreek.ca.granicus.com",
                "label": "Dawson Creek Granicus Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Chetwynd",
        "short_name": "Chetwynd",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.chetwynd.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.chetwynd.ca/council",
                "label": "Chetwynd Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Tumbler Ridge",
        "short_name": "Tumbler Ridge",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.tumblerridge.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.tumblerridge.ca/council",
                "label": "Tumbler Ridge Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Hudson's Hope",
        "short_name": "Hudson's Hope",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.hudsonshope.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.hudsonshope.ca/council",
                "label": "Hudson's Hope Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 11 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_11 = [
    {
        "name": "District of Lake Cowichan",
        "short_name": "Lake Cowichan",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.lakecowichan.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://lakecowichan.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Lake Cowichan CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://lakecowichan.civicweb.net/filepro/documents/",
                "label": "Lake Cowichan CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Port Hardy",
        "short_name": "Port Hardy",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.porthardy.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.porthardy.ca/council",
                "label": "Port Hardy Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Port McNeill",
        "short_name": "Port McNeill",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.portmcneill.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.portmcneill.ca/council",
                "label": "Port McNeill Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Alert Bay",
        "short_name": "Alert Bay",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.alertbay.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.alertbay.ca/council",
                "label": "Alert Bay Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Gold River",
        "short_name": "Gold River",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.goldriver.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.goldriver.ca/council",
                "label": "Gold River Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Tahsis",
        "short_name": "Tahsis",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.tahsis.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.tahsis.ca/council",
                "label": "Tahsis Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Zeballos",
        "short_name": "Zeballos",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.zeballos.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.zeballos.ca/council",
                "label": "Zeballos Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Ucluelet",
        "short_name": "Ucluelet",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.ucluelet.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://ucluelet.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Ucluelet CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://ucluelet.civicweb.net/filepro/documents/",
                "label": "Ucluelet CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Tofino",
        "short_name": "Tofino",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.tofino.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://tofino.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Tofino CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://tofino.civicweb.net/filepro/documents/",
                "label": "Tofino CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Lantzville",
        "short_name": "Lantzville",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.lantzville.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://lantzville.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Lantzville CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://lantzville.civicweb.net/filepro/documents/",
                "label": "Lantzville CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 12 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_12 = [
    {
        "name": "Village of Fruitvale",
        "short_name": "Fruitvale",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.fruitvale.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.fruitvale.ca/council",
                "label": "Fruitvale Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Warfield",
        "short_name": "Warfield",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.warfield.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.warfield.ca/council",
                "label": "Warfield Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Montrose",
        "short_name": "Montrose",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.montrose.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.montrose.ca/council",
                "label": "Montrose Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Greenwood",
        "short_name": "Greenwood",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.greenwoodbc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.greenwoodbc.ca/council",
                "label": "Greenwood Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Midway",
        "short_name": "Midway",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.midwaybc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.midwaybc.ca/council",
                "label": "Midway Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Osoyoos",
        "short_name": "Osoyoos",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.osoyoos.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://osoyoos.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Osoyoos CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://osoyoos.civicweb.net/filepro/documents/",
                "label": "Osoyoos CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Oliver",
        "short_name": "Oliver",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.oliver.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://oliver.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Oliver CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://oliver.civicweb.net/filepro/documents/",
                "label": "Oliver CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Princeton",
        "short_name": "Princeton",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.princeton.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.princeton.ca/council",
                "label": "Princeton Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Keremeos",
        "short_name": "Keremeos",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.keremeos.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.keremeos.ca/council",
                "label": "Keremeos Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of New Denver",
        "short_name": "New Denver",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.newdenver.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.newdenver.ca/council",
                "label": "New Denver Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 13 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_13 = [
    {
        "name": "Village of Silverton",
        "short_name": "Silverton",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.silverton.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.silverton.ca/council",
                "label": "Silverton Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Slocan",
        "short_name": "Slocan",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.slocan.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.slocan.ca/council",
                "label": "Slocan Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Kaslo",
        "short_name": "Kaslo",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.kaslo.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.kaslo.ca/council",
                "label": "Kaslo Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Nakusp",
        "short_name": "Nakusp",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.nakusp.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.nakusp.com/council",
                "label": "Nakusp Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Town of Creston",
        "short_name": "Creston",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.creston.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.creston.ca/council",
                "label": "Creston Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Salmo",
        "short_name": "Salmo",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.salmo.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.salmo.ca/council",
                "label": "Salmo Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Riondel",
        "short_name": "Riondel",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.riondel.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.riondel.ca/council",
                "label": "Riondel Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Ainsworth Hot Springs",
        "short_name": "Ainsworth Hot Springs",
        "gov_type": GovType.UNINCORPORATED,
        "region": "BC",
        "website_url": "https://www.rdkb.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.rdkb.com",
                "label": "Ainsworth Hot Springs RDKB Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Balfour",
        "short_name": "Balfour",
        "gov_type": GovType.UNINCORPORATED,
        "region": "BC",
        "website_url": "https://www.rdkb.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.rdkb.com",
                "label": "Balfour RDKB Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Christina Lake",
        "short_name": "Christina Lake",
        "gov_type": GovType.UNINCORPORATED,
        "region": "BC",
        "website_url": "https://www.rdkb.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.rdkb.com",
                "label": "Christina Lake RDKB Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 14 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_14 = [
    {
        "name": "District of Invermere",
        "short_name": "Invermere",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.invermere.net/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.invermere.net/council",
                "label": "Invermere Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Canal Flats",
        "short_name": "Canal Flats",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.canalflats.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.canalflats.com/council",
                "label": "Canal Flats Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Radium Hot Springs",
        "short_name": "Radium Hot Springs",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.radiumhotsprings.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.radiumhotsprings.com/council",
                "label": "Radium Hot Springs Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Ashcroft",
        "short_name": "Ashcroft",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.ashcroftbc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.ashcroftbc.ca/council",
                "label": "Ashcroft Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Cache Creek",
        "short_name": "Cache Creek",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.cachecreekbc.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.cachecreekbc.com/council",
                "label": "Cache Creek Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Clinton",
        "short_name": "Clinton",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.clintonbc.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.clintonbc.com/council",
                "label": "Clinton Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Lillooet",
        "short_name": "Lillooet",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.lillooetbc.com/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.lillooetbc.com/council",
                "label": "Lillooet Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Merritt",
        "short_name": "Merritt",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.merritt.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://merritt.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Merritt CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://merritt.civicweb.net/filepro/documents/",
                "label": "Merritt CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Logan Lake",
        "short_name": "Logan Lake",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.loganlake.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.loganlake.ca/council",
                "label": "Logan Lake Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Chase",
        "short_name": "Chase",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.chasebc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.chasebc.ca/council",
                "label": "Chase Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 15 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_15 = [
    {
        "name": "District of Clearwater",
        "short_name": "Clearwater",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.clearwaterbc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.clearwaterbc.ca/council",
                "label": "Clearwater Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Barriere",
        "short_name": "Barriere",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.barrierebc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.barrierebc.ca/council",
                "label": "Barriere Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Valemount",
        "short_name": "Valemount",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.valemount.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.valemount.ca/council",
                "label": "Valemount Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of McBride",
        "short_name": "McBride",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.mcbride.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.mcbride.ca/council",
                "label": "McBride Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Granisle",
        "short_name": "Granisle",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.granisle.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.granisle.ca/council",
                "label": "Granisle Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Telkwa",
        "short_name": "Telkwa",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.telkwa.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.telkwa.ca/council",
                "label": "Telkwa Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of New Hazelton",
        "short_name": "New Hazelton",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.newhazelton.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.newhazelton.ca/council",
                "label": "New Hazelton Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Hazelton",
        "short_name": "Hazelton",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.hazelton.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.hazelton.ca/council",
                "label": "Hazelton Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Stewart",
        "short_name": "Stewart",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.stewartbc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.stewartbc.ca/council",
                "label": "Stewart Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Port Edward",
        "short_name": "Port Edward",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.portedward.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.portedward.ca/council",
                "label": "Port Edward Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 16 – final 11 municipalities (completes all 161 BC municipalities)
# Batch 16 – unique entries only (duplicates from Batch 15 removed)
BC_MUNICIPALITIES_BATCH_16 = [
    {
        "name": "Town of Fort Nelson",
        "short_name": "Fort Nelson",
        "gov_type": GovType.TOWN,
        "region": "BC",
        "website_url": "https://www.fortnelson.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.fortnelson.ca/council",
                "label": "Fort Nelson Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Northern Rockies Regional Municipality",
        "short_name": "Northern Rockies",
        "gov_type": GovType.REGIONAL_MUNICIPALITY,
        "region": "BC",
        "website_url": "https://www.northernrockies.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.northernrockies.ca/council",
                "label": "Northern Rockies Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Wells",
        "short_name": "Wells",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.wellsbc.ca/",
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.wellsbc.ca/council",
                "label": "Wells Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 17 – 15 previously missing BC municipalities
BC_MUNICIPALITIES_BATCH_17 = [
    {
        "name": "Village of Anmore",
        "short_name": "Anmore",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://anmore.com/",
        "population": 2356,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://anmore.com/village-hall/mayor-council/agendas-minutes/",
                "label": "Anmore Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Belcarra",
        "short_name": "Belcarra",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.belcarra.ca/",
        "population": 687,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://belcarra.ca/municipal-hall/council-meetings/",
                "label": "Belcarra Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Burns Lake",
        "short_name": "Burns Lake",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.burnslake.ca/",
        "population": 1659,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.burnslake.ca/local-government/mayor-council/agendas-minutes",
                "label": "Burns Lake Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Delta",
        "short_name": "Delta",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.delta.ca/",
        "population": 108455,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-delta.escribemeetings.com",
                "label": "Delta eScribe Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Fraser Lake",
        "short_name": "Fraser Lake",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.fraserlake.ca/",
        "population": 965,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.fraserlake.ca/municipal-hall/council-meetings-0",
                "label": "Fraser Lake Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Lytton",
        "short_name": "Lytton",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.lytton.ca/",
        "population": 210,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://lyttonbc.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Lytton CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://lyttonbc.civicweb.net/filepro/documents/",
                "label": "Lytton CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Masset",
        "short_name": "Masset",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "http://massetbc.com/",
        "population": 838,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "http://massetbc.com/village-office/minutes/",
                "label": "Masset Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Municipality of North Cowichan",
        "short_name": "North Cowichan",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://www.northcowichan.ca/",
        "population": 31990,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-northcowichan.escribemeetings.com",
                "label": "North Cowichan eScribe Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Port Alice",
        "short_name": "Port Alice",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://portalice.ca/",
        "population": 739,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://portalice.ca/town-hall/minutes-agendas/",
                "label": "Port Alice Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Port Clements",
        "short_name": "Port Clements",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://portclements.ca/",
        "population": 340,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://portclements.ca/municipal-information/council-meetings/",
                "label": "Port Clements Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Pouce Coupe",
        "short_name": "Pouce Coupe",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://poucecoupe.ca/",
        "population": 739,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://poucecoupe.ca/government/administration/council-meetings/",
                "label": "Pouce Coupe Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Queen Charlotte",
        "short_name": "Queen Charlotte",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://daajinggiids.ca/",
        "population": 964,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://daajinggiids.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Queen Charlotte CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://daajinggiids.civicweb.net/filepro/documents/",
                "label": "Queen Charlotte CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Village of Sayward",
        "short_name": "Sayward",
        "gov_type": GovType.VILLAGE,
        "region": "BC",
        "website_url": "https://www.sayward.ca/",
        "population": 311,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://www.sayward.ca/government-bylaws/council-meetings",
                "label": "Sayward Council Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Sun Peaks Mountain Resort Municipality",
        "short_name": "Sun Peaks",
        "gov_type": GovType.MOUNTAIN_RESORT,
        "region": "BC",
        "website_url": "https://sunpeaksmunicipality.ca/",
        "population": 1404,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://sunpeaks.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Sun Peaks CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://sunpeaks.civicweb.net/filepro/documents/",
                "label": "Sun Peaks CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "District of Taylor",
        "short_name": "Taylor",
        "gov_type": GovType.DISTRICT,
        "region": "BC",
        "website_url": "https://districtoftaylor.com/",
        "population": 1469,
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://taylor.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Taylor CivicWeb Agendas",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.MINUTES,
                "url": "https://taylor.civicweb.net/filepro/documents/",
                "label": "Taylor CivicWeb Minutes",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]


# =============================================================================
# Alberta — Phase 1 (10 municipalities, fully configured for active scraping)
# =============================================================================
#
# These are the 10 largest / highest-priority Alberta municipalities. Each has
# a website + at least one structured source (CivicWeb / eSCRIBE / YouTube)
# and ships in ScrapeStatus.ACTIVE so the existing platform-aware scrapers
# pick them up without further code changes.
#
# Source URLs were chosen using the published meeting management portals
# referenced from each municipality's official council page; if a portal
# domain changes upstream the source row can be patched via the registry API
# without a redeploy.
ALBERTA_MUNICIPALITIES_PHASE_1 = [
    {
        "name": "City of Calgary",
        "short_name": "Calgary",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.calgary.ca/",
        "population": 1306784,
        "sources": [
            {
                # One eSCRIBE source per portal — the scraper finds both
                # agendas and minutes from the same portal listing, so
                # registering separate rows per source_type would just
                # duplicate-poll the same URL.
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-calgary.escribemeetings.com",
                "label": "Calgary eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                # Calgary's actual handle is @thecityofcalgary; the prior
                # @cityofcalgary handle 404s. URL preserved through resolver
                # cache in Source.scrape_config.
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@thecityofcalgary",
                "label": "Calgary YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Edmonton",
        "short_name": "Edmonton",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.edmonton.ca/",
        "population": 1010899,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-edmonton.escribemeetings.com",
                "label": "Edmonton eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofEdmonton",
                "label": "Edmonton YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        # Red Deer publishes meetings on eSCRIBE, not CivicWeb (the original
        # reddeer.civicweb.net subdomain doesn't exist). YouTube channel is
        # @TheCityofRedDeer (not @CityofRedDeer).
        "name": "City of Red Deer",
        "short_name": "Red Deer",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.reddeer.ca/",
        "population": 100844,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-reddeer.escribemeetings.com",
                "label": "Red Deer eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@TheCityofRedDeer",
                "label": "Red Deer YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Lethbridge",
        "short_name": "Lethbridge",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.lethbridge.ca/",
        "population": 98406,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-lethbridge.escribemeetings.com",
                "label": "Lethbridge eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofLethbridge",
                "label": "Lethbridge YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Medicine Hat",
        "short_name": "Medicine Hat",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.medicinehat.ca/",
        "population": 63271,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-medicinehat.escribemeetings.com",
                "label": "Medicine Hat eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                # Real handle is @CityMedicineHat (no "of"); the prior
                # @CityofMedicineHatAB handle 404s.
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityMedicineHat",
                "label": "Medicine Hat YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Airdrie",
        "short_name": "Airdrie",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.airdrie.ca/",
        "population": 80649,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-airdrie.escribemeetings.com",
                "label": "Airdrie eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                # Airdrie has no discoverable public council-meetings YouTube
                # channel; eSCRIBE is the source of truth. Demoted to PENDING
                # until/unless an official handle surfaces.
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofAirdrie",
                "label": "Airdrie YouTube Council Meetings",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    },
    {
        # Spruce Grove uses eSCRIBE, not CivicWeb. The original
        # sprucegrove.civicweb.net subdomain doesn't exist.
        "name": "City of Spruce Grove",
        "short_name": "Spruce Grove",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.sprucegrove.org/",
        "population": 39348,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-sprucegrove.escribemeetings.com",
                "label": "Spruce Grove eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@CityofSpruceGrove",
                "label": "Spruce Grove YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Grande Prairie",
        "short_name": "Grande Prairie",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.cityofgp.com/",
        "population": 64141,
        "sources": [
            {
                # Real eSCRIBE subdomain is pub-cityofgp; the prior
                # pub-grandeprairie subdomain doesn't exist.
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-cityofgp.escribemeetings.com",
                "label": "Grande Prairie eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                # YouTube channel published under /user/GrandePrairieCA.
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/user/GrandePrairieCA",
                "label": "Grande Prairie YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        # St. Albert publishes agendas/minutes via Legistar (stalbert.ca.legistar.com)
        # which we do not yet have a scraper for. The Legistar-platform sources
        # ship as CUSTOM/PENDING placeholders so they appear in the registry
        # and can be activated in a follow-up phase. YouTube remains ACTIVE
        # via the legacy /user/CityofStAlbert URL (it's a real channel).
        "name": "City of St. Albert",
        "short_name": "St. Albert",
        "gov_type": GovType.CITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://stalbert.ca/",
        "population": 68232,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://stalbert.ca.legistar.com/Calendar.aspx",
                "label": "St. Albert Legistar Portal (pending Legistar scraper)",
                "scrape_status": ScrapeStatus.PENDING,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/user/CityofStAlbert",
                "label": "St. Albert YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "Regional Municipality of Wood Buffalo (Fort McMurray)",
        "short_name": "Fort McMurray",
        "gov_type": GovType.REGIONAL_MUNICIPALITY,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": "https://www.rmwb.ca/",
        "population": 72326,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-rmwb.escribemeetings.com",
                "label": "Wood Buffalo eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                # Wood Buffalo's YouTube channel is published under
                # /user/rmwbwebmaster (legacy URL form, still active).
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/user/rmwbwebmaster",
                "label": "Wood Buffalo YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]


# =============================================================================
# Alberta — Remainder seed (~334 entries, PENDING placeholders)
# =============================================================================
#
# The remaining Alberta municipalities are seeded with a single CUSTOM /
# PENDING source pointing at the provincial directory. This makes them
# appear in the /municipalities?province=Alberta dropdown so subscribers can
# *choose* them today, while telling the poller to skip them until a real
# scraper config is configured for them in a follow-up phase.
#
# Names are taken verbatim from the spec the product team provided. Some
# entries are amalgamated/dissolved municipalities (e.g. "Grand Centre",
# "Turner Valley", "Lacombe (prior to city status)") — they are kept as-is
# but listed as PENDING so they have no live scraping side-effects.
_ALBERTA_DIRECTORY_URL = "https://www.alberta.ca/find-a-municipal-official"


def _ab_pending(
    *,
    name: str,
    short_name: str,
    gov_type: GovType,
    website_url: str | None = None,
    population: int | None = None,
) -> dict:
    """Build a placeholder Alberta municipality entry for Phase 1+ rollout.

    The single source is intentionally CUSTOM/PENDING: it satisfies the
    "every muni has at least one source" invariant without triggering the
    poller to make HTTP calls before a real scraper config is wired up.
    """
    return {
        "name": name,
        "short_name": short_name,
        "gov_type": gov_type,
        "region": "Alberta",
        "province": PROVINCE_AB,
        "website_url": website_url,
        "population": population,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": f"{_ALBERTA_DIRECTORY_URL}#{short_name.replace(' ', '-')}",
                "label": f"{short_name} council meetings (pending)",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    }


# Cities — the spec lists 17 cities. The first 10 are in Phase 1, so this
# block covers the remaining cities only.
_AB_REMAINDER_CITIES = [
    ("City of Brooks", "Brooks", GovType.CITY),
    ("City of Camrose", "Camrose", GovType.CITY),
    ("City of Cold Lake", "Cold Lake", GovType.CITY),
    ("City of Lacombe", "Lacombe", GovType.CITY),
    ("City of Leduc", "Leduc", GovType.CITY),
    ("City of Lloydminster", "Lloydminster", GovType.CITY),
    ("City of Wetaskiwin", "Wetaskiwin", GovType.CITY),
]

_AB_REMAINDER_TOWNS = [
    ("Town of Banff", "Banff", GovType.TOWN),
    ("Town of Barrhead", "Barrhead", GovType.TOWN),
    ("Town of Bassano", "Bassano", GovType.TOWN),
    ("Town of Beaumont", "Beaumont", GovType.TOWN),
    ("Town of Bentley", "Bentley", GovType.TOWN),
    ("Town of Blackfalds", "Blackfalds", GovType.TOWN),
    ("Town of Black Diamond", "Black Diamond", GovType.TOWN),
    ("Town of Bon Accord", "Bon Accord", GovType.TOWN),
    ("Town of Bonnyville", "Bonnyville", GovType.TOWN),
    ("Town of Bow Island", "Bow Island", GovType.TOWN),
    ("Town of Bowden", "Bowden", GovType.TOWN),
    ("Town of Bruderheim", "Bruderheim", GovType.TOWN),
    ("Town of Canmore", "Canmore", GovType.TOWN),
    ("Town of Cardston", "Cardston", GovType.TOWN),
    ("Town of Carstairs", "Carstairs", GovType.TOWN),
    ("Town of Castor", "Castor", GovType.TOWN),
    ("City of Chestermere", "Chestermere", GovType.TOWN),
    ("Town of Claresholm", "Claresholm", GovType.TOWN),
    ("Town of Coaldale", "Coaldale", GovType.TOWN),
    ("Town of Coalhurst", "Coalhurst", GovType.TOWN),
    ("Village of Coronation", "Coronation", GovType.TOWN),
    ("Town of Crossfield", "Crossfield", GovType.TOWN),
    ("Town of Daysland", "Daysland", GovType.TOWN),
    ("Town of Devon", "Devon", GovType.TOWN),
    ("Town of Didsbury", "Didsbury", GovType.TOWN),
    ("Village of Eckville", "Eckville", GovType.TOWN),
    ("Town of Edson", "Edson", GovType.TOWN),
    ("Town of Elk Point", "Elk Point", GovType.TOWN),
    ("Town of Fairview", "Fairview", GovType.TOWN),
    ("Village of Falher", "Falher", GovType.TOWN),
    ("Town of Fort Macleod", "Fort Macleod", GovType.TOWN),
    ("Town of Fox Creek", "Fox Creek", GovType.TOWN),
    ("Town of Gibbons", "Gibbons", GovType.TOWN),
    ("Town of Grand Centre", "Grand Centre", GovType.TOWN),
    ("Village of Granum", "Granum", GovType.TOWN),
    ("Town of Grimshaw", "Grimshaw", GovType.TOWN),
    ("Town of Hanna", "Hanna", GovType.TOWN),
    ("Town of Hardisty", "Hardisty", GovType.TOWN),
    ("Town of High Level", "High Level", GovType.TOWN),
    ("Town of High Prairie", "High Prairie", GovType.TOWN),
    ("Town of High River", "High River", GovType.TOWN),
    ("Town of Hinton", "Hinton", GovType.TOWN),
    ("Town of Innisfail", "Innisfail", GovType.TOWN),
    ("Town of Irricana", "Irricana", GovType.TOWN),
    ("Town of Killam", "Killam", GovType.TOWN),
    ("Lac La Biche County (Town of Lac La Biche)", "Lac La Biche", GovType.TOWN),
    ("Town of Lacombe (prior to city status)", "Lacombe (former town)", GovType.TOWN),
    ("Town of Lamont", "Lamont", GovType.TOWN),
    ("Village of Legal", "Legal", GovType.TOWN),
    ("Town of Magrath", "Magrath", GovType.TOWN),
    ("Town of Manning", "Manning", GovType.TOWN),
    ("Town of Mayerthorpe", "Mayerthorpe", GovType.TOWN),
    ("Town of Milk River", "Milk River", GovType.TOWN),
    ("Village of Millet", "Millet", GovType.TOWN),
    ("Town of Morinville", "Morinville", GovType.TOWN),
    ("Village of Mundare", "Mundare", GovType.TOWN),
    ("Town of Nanton", "Nanton", GovType.TOWN),
    ("Town of Olds", "Olds", GovType.TOWN),
    ("Village of Onoway", "Onoway", GovType.TOWN),
    ("Town of Oyen", "Oyen", GovType.TOWN),
    ("Town of Peace River", "Peace River", GovType.TOWN),
    ("Town of Penhold", "Penhold", GovType.TOWN),
    ("Town of Picture Butte", "Picture Butte", GovType.TOWN),
    ("Town of Pincher Creek", "Pincher Creek", GovType.TOWN),
    ("Town of Ponoka", "Ponoka", GovType.TOWN),
    ("Town of Provost", "Provost", GovType.TOWN),
    ("Town of Rainbow Lake", "Rainbow Lake", GovType.TOWN),
    ("Town of Raymond", "Raymond", GovType.TOWN),
    ("Town of Redcliff", "Redcliff", GovType.TOWN),
    ("Town of Rimbey", "Rimbey", GovType.TOWN),
    ("Town of Rocky Mountain House", "Rocky Mountain House", GovType.TOWN),
    ("Town of Sexsmith", "Sexsmith", GovType.TOWN),
    ("Town of Slave Lake", "Slave Lake", GovType.TOWN),
    ("Town of Smoky Lake", "Smoky Lake", GovType.TOWN),
    ("Town of Spirit River", "Spirit River", GovType.TOWN),
    ("Town of St. Paul", "St. Paul", GovType.TOWN),
    ("Village of Stavely", "Stavely", GovType.TOWN),
    ("Town of Stettler", "Stettler", GovType.TOWN),
    ("Town of Stony Plain", "Stony Plain", GovType.TOWN),
    ("Town of Strathmore", "Strathmore", GovType.TOWN),
    ("Town of Sundre", "Sundre", GovType.TOWN),
    ("Town of Swan Hills", "Swan Hills", GovType.TOWN),
    ("Town of Sylvan Lake", "Sylvan Lake", GovType.TOWN),
    ("Town of Taber", "Taber", GovType.TOWN),
    ("Village of Thorsby", "Thorsby", GovType.TOWN),
    ("Town of Three Hills", "Three Hills", GovType.TOWN),
    ("Town of Tofield", "Tofield", GovType.TOWN),
    ("Town of Turner Valley", "Turner Valley", GovType.TOWN),
    ("Town of Two Hills", "Two Hills", GovType.TOWN),
    ("Town of Vauxhall", "Vauxhall", GovType.TOWN),
    ("Town of Vegreville", "Vegreville", GovType.TOWN),
    ("Town of Vermilion", "Vermilion", GovType.TOWN),
    ("Town of Vulcan", "Vulcan", GovType.TOWN),
    ("Town of Wainwright", "Wainwright", GovType.TOWN),
    ("Town of Westlock", "Westlock", GovType.TOWN),
    ("Town of Whitecourt", "Whitecourt", GovType.TOWN),
]

_AB_REMAINDER_VILLAGES = [
    ("Village of Acme", "Acme"),
    ("Village of Alberta Beach", "Alberta Beach"),
    ("Village of Alix", "Alix"),
    ("Village of Alliance", "Alliance"),
    ("Village of Andrew", "Andrew"),
    ("Village of Arrowwood", "Arrowwood"),
    ("Village of Barnwell", "Barnwell"),
    ("Village of Barons", "Barons"),
    ("Village of Bawlf", "Bawlf"),
    ("Village of Berwyn", "Berwyn"),
    ("Village of Big Valley", "Big Valley"),
    ("Village of Bittern Lake", "Bittern Lake"),
    ("Village of Boyle", "Boyle"),
    ("Village of Carbon", "Carbon"),
    ("Village of Carmangay", "Carmangay"),
    ("Village of Caroline", "Caroline"),
    ("Village of Chauvin", "Chauvin"),
    ("Village of Chipman", "Chipman"),
    ("Village of Clive", "Clive"),
    ("Village of Clyde", "Clyde"),
    ("Village of Czar", "Czar"),
    ("Village of Delburne", "Delburne"),
    ("Village of Delia", "Delia"),
    ("Village of Dewberry", "Dewberry"),
    ("Village of Donalda", "Donalda"),
    ("Village of Duchess", "Duchess"),
    ("Village of Edgerton", "Edgerton"),
    ("Village of Elnora", "Elnora"),
    ("Village of Ferintosh", "Ferintosh"),
    ("Village of Foremost", "Foremost"),
    ("Village of Girouxville", "Girouxville"),
    ("Village of Glendon", "Glendon"),
    ("Village of Halkirk", "Halkirk"),
    ("Village of Hay Lakes", "Hay Lakes"),
    ("Village of Heisler", "Heisler"),
    ("Village of Hill Spring", "Hill Spring"),
    ("Village of Hines Creek", "Hines Creek"),
    ("Village of Hughenden", "Hughenden"),
    ("Village of Hussar", "Hussar"),
    ("Village of Hythe", "Hythe"),
    ("Village of Kitscoty", "Kitscoty"),
    ("Village of Linden", "Linden"),
    ("Village of Lomond", "Lomond"),
    ("Village of Longview", "Longview"),
    ("Village of Lougheed", "Lougheed"),
    ("Village of Mannville", "Mannville"),
    ("Village of Marwayne", "Marwayne"),
    ("Village of Milo", "Milo"),
    ("Village of Minburn", "Minburn"),
    ("Village of Morrin", "Morrin"),
    ("Village of Myrnam", "Myrnam"),
    ("Village of Nampa", "Nampa"),
    ("Village of Nobleford", "Nobleford"),
    ("Village of Paradise Valley", "Paradise Valley"),
    ("Village of Rockyford", "Rockyford"),
    ("Village of Rosalind", "Rosalind"),
    ("Village of Rycroft", "Rycroft"),
    ("Village of Ryley", "Ryley"),
    ("Village of Spring Lake", "Spring Lake"),
    ("Village of Standard", "Standard"),
    ("Village of Stirling", "Stirling"),
    ("Village of Valhalla Centre", "Valhalla Centre"),
    ("Village of Veteran", "Veteran"),
    ("Village of Vilna", "Vilna"),
    ("Village of Wabamun", "Wabamun"),
    ("Village of Warburg", "Warburg"),
    ("Village of Warner", "Warner"),
    ("Village of Willingdon", "Willingdon"),
    ("Village of Youngstown", "Youngstown"),
]

# Summer villages — the canonical Alberta Summer Villages list. The product
# spec quoted "96 of them" with abbreviated examples; the actual count of
# incorporated Alberta summer villages is in the low 50s (Alberta Municipal
# Affairs registry). We seed the full canonical list so the dropdown isn't
# missing entries the user listed verbatim. Use VILLAGE gov_type to keep
# the existing GovType enum unchanged.
_AB_REMAINDER_SUMMER_VILLAGES = [
    "Argentia Beach",
    "Betula Beach",
    "Birch Cove",
    "Birchcliff",
    "Bondiss",
    "Bonnyville Beach",
    "Brentwood",  # Brentwood-on-the-Lake summer village name
    "Burnstick Lake",
    "Castle Island",
    "Crystal Springs",
    "Ghost Lake",
    "Golden Days",
    "Grandview",
    "Gull Lake",
    "Half Moon Bay",
    "Horseshoe Bay",
    "Island Lake",
    "Island Lake South",
    "Itaska Beach",
    "Jarvis Bay",
    "Kapasiwin",
    "Lakeview",
    "Larkspur",
    "Ma-Me-O Beach",
    "Mewatha Beach",
    "Nakamun Park",
    "Norglenwold",
    "Norris Beach",
    "Parkland Beach",
    "Pelican Narrows",
    "Point Alison",
    "Poplar Bay",
    "Rochon Sands",
    "Ross Haven",
    "Seba Beach",
    "Silver Beach",
    "Silver Sands",
    "South Baptiste",
    "South View",
    "Sunbreaker Cove",
    "Sundance Beach",
    "Sunrise Beach",
    "Sunset Beach",
    "Sunset Point",
    "Sunridge",
    "Val Quentin",
    "Waiparous",
    "West Baptiste",
    "West Cove",
    "Whispering Hills",
    "White Sands",
    "Yellowstone",
]

_AB_REMAINDER_COUNTIES = [
    ("Athabasca County", "Athabasca County"),
    ("Beaver County", "Beaver County"),
    ("Big Lakes County", "Big Lakes County"),
    ("Birch Hills County", "Birch Hills County"),
    ("Brazeau County", "Brazeau County"),
    ("Camrose County", "Camrose County"),
    ("Cardston County", "Cardston County"),
    ("Clear Hills County", "Clear Hills County"),
    ("Clearwater County", "Clearwater County"),
    ("County of Barrhead", "County of Barrhead"),
    ("County of Grande Prairie No. 1", "County of Grande Prairie"),
    ("County of Minburn No. 27", "County of Minburn"),
    ("County of Newell", "County of Newell"),
    ("County of Northern Lights", "County of Northern Lights"),
    ("County of Stettler No. 6", "County of Stettler"),
    ("Cypress County", "Cypress County"),
    ("Flagstaff County", "Flagstaff County"),
    ("Foothills County", "Foothills County"),
    ("Kneehill County", "Kneehill County"),
    ("Lac Ste. Anne County", "Lac Ste. Anne County"),
    ("Lac La Biche County", "Lac La Biche County"),
    ("Lamont County", "Lamont County"),
    ("Leduc County", "Leduc County"),
    ("Mackenzie County", "Mackenzie County"),
    ("Mountain View County", "Mountain View County"),
    ("Northern Sunrise County", "Northern Sunrise County"),
    ("Parkland County", "Parkland County"),
    ("Ponoka County", "Ponoka County"),
    ("Red Deer County", "Red Deer County"),
    ("Rocky View County", "Rocky View County"),
    ("Saddle Hills County", "Saddle Hills County"),
    ("Smoky Lake County", "Smoky Lake County"),
    ("Starland County", "Starland County"),
    ("Sturgeon County", "Sturgeon County"),
    ("Thorhild County", "Thorhild County"),
    ("Two Hills County", "Two Hills County"),
    ("Vermilion River County", "Vermilion River County"),
    ("Vulcan County", "Vulcan County"),
    ("Westlock County", "Westlock County"),
    ("Wetaskiwin County No. 10", "Wetaskiwin County"),
    ("Wheatland County", "Wheatland County"),
    ("Yellowhead County", "Yellowhead County"),
]

_AB_REMAINDER_SPECIALIZED = [
    # Specialized municipalities: gov_type = REGIONAL_MUNICIPALITY (closest fit)
    ("Municipality of Crowsnest Pass", "Crowsnest Pass", GovType.REGIONAL_MUNICIPALITY),
    ("Municipality of Jasper", "Jasper", GovType.REGIONAL_MUNICIPALITY),
    ("Strathcona County", "Strathcona County", GovType.REGIONAL_MUNICIPALITY),
    # Improvement Districts and Special Areas — closest available gov_type
    # is UNINCORPORATED.
    ("Improvement District No. 9 (Banff)", "Improvement District No. 9", GovType.UNINCORPORATED),
    ("Special Area No. 2", "Special Area No. 2", GovType.UNINCORPORATED),
    ("Special Area No. 3", "Special Area No. 3", GovType.UNINCORPORATED),
    ("Special Area No. 4", "Special Area No. 4", GovType.UNINCORPORATED),
    # Métis settlements — use UNINCORPORATED (no METIS_SETTLEMENT enum value
    # today; introducing one would require a Postgres enum migration).
    ("Buffalo Lake Métis Settlement", "Buffalo Lake", GovType.UNINCORPORATED),
    ("East Prairie Métis Settlement", "East Prairie", GovType.UNINCORPORATED),
    ("Elizabeth Métis Settlement", "Elizabeth", GovType.UNINCORPORATED),
    ("Fishing Lake Métis Settlement", "Fishing Lake", GovType.UNINCORPORATED),
    ("Gift Lake Métis Settlement", "Gift Lake", GovType.UNINCORPORATED),
    ("Kikino Métis Settlement", "Kikino", GovType.UNINCORPORATED),
    ("Paddle Prairie Métis Settlement", "Paddle Prairie", GovType.UNINCORPORATED),
    ("Peavine Métis Settlement", "Peavine", GovType.UNINCORPORATED),
]


def _build_alberta_remainder() -> list[dict]:
    """Materialize the placeholder Alberta entries from the typed source lists."""
    out: list[dict] = []

    for name, short, gtype in _AB_REMAINDER_CITIES:
        out.append(_ab_pending(name=name, short_name=short, gov_type=gtype))

    for name, short, gtype in _AB_REMAINDER_TOWNS:
        out.append(_ab_pending(name=name, short_name=short, gov_type=gtype))

    for name, short in _AB_REMAINDER_VILLAGES:
        out.append(_ab_pending(name=name, short_name=short, gov_type=GovType.VILLAGE))

    for short in _AB_REMAINDER_SUMMER_VILLAGES:
        out.append(
            _ab_pending(
                name=f"Summer Village of {short}",
                short_name=f"SV {short}",
                gov_type=GovType.VILLAGE,
            )
        )

    for name, short in _AB_REMAINDER_COUNTIES:
        out.append(_ab_pending(name=name, short_name=short, gov_type=GovType.DISTRICT))

    for name, short, gtype in _AB_REMAINDER_SPECIALIZED:
        out.append(_ab_pending(name=name, short_name=short, gov_type=gtype))

    return out


def _apply_remainder_patches(entries: list[dict]) -> list[dict]:
    """Merge the auto-generated probe patches onto the placeholder roster.

    For every entry whose ``short_name`` appears in ``REMAINDER_PATCHES``:
    - replace ``website_url`` with the probe-discovered value
    - replace the placeholder source list with the probe-derived sources

    Entries with no patch keep their PENDING placeholder source.
    """
    try:
        from app.services._ab_remainder_patches import REMAINDER_PATCHES
    except ImportError:
        # Patches file not generated yet (e.g. fresh checkout before
        # ``scripts/apply_alberta_probe.py`` has been run). Stay placeholder-only.
        return entries

    # Resolve the string-form enum references used in the patches file.
    enum_lookup = {
        "Platform.CIVICWEB": Platform.CIVICWEB,
        "Platform.GRANICUS": Platform.GRANICUS,
        "Platform.ESCRIBE": Platform.ESCRIBE,
        "Platform.YOUTUBE": Platform.YOUTUBE,
        "Platform.CIVICPLUS": Platform.CIVICPLUS,
        "Platform.CUSTOM": Platform.CUSTOM,
        "Platform.UNKNOWN": Platform.UNKNOWN,
        "SourceType.AGENDA": SourceType.AGENDA,
        "SourceType.MINUTES": SourceType.MINUTES,
        "SourceType.VIDEO": SourceType.VIDEO,
        "SourceType.NOTICE": SourceType.NOTICE,
        "SourceType.BYLAW": SourceType.BYLAW,
        "ScrapeStatus.ACTIVE": ScrapeStatus.ACTIVE,
        "ScrapeStatus.PENDING": ScrapeStatus.PENDING,
        "ScrapeStatus.BROKEN": ScrapeStatus.BROKEN,
        "ScrapeStatus.DISABLED": ScrapeStatus.DISABLED,
    }

    def _resolve(source: dict) -> dict:
        return {
            "platform": enum_lookup[source["platform"]],
            "source_type": enum_lookup[source["source_type"]],
            "url": source["url"],
            "label": source["label"],
            "scrape_status": enum_lookup[source["scrape_status"]],
        }

    for entry in entries:
        patch = REMAINDER_PATCHES.get(entry["short_name"])
        if not patch:
            continue
        if patch.get("website_url"):
            entry["website_url"] = patch["website_url"]
        sources = [_resolve(s) for s in patch.get("sources", [])]
        if sources:
            # Drop the placeholder PENDING source — we now have real ones.
            entry["sources"] = sources

    return entries


ALBERTA_MUNICIPALITIES_REMAINDER: list[dict] = _apply_remainder_patches(
    _build_alberta_remainder()
)


# =============================================================================
# Ontario — Phase 1 (10 cities, fully configured for active scraping)
# =============================================================================
#
# Ontario's two dominant council-meeting platforms are eSCRIBE and CivicWeb.
# Toronto runs a bespoke portal at secure.toronto.ca/council that needs a
# new scraper (tracked as ON-001 in docs/ontario-rollout-tracker.md); the
# initial Toronto seed source ships PENDING. Other Phase 1 cities use
# eSCRIBE or CivicWeb directly and the existing platform scrapers handle
# them with no code changes.
#
# Each Phase 1 muni has 2 source rows:
#   - one platform/portal entry (eSCRIBE / CivicWeb / CUSTOM-pending)
#   - one YouTube entry
# That mirrors the Alberta Phase 1 shape so phase_runner.py / tracker
# tooling stays consistent across provinces.
ONTARIO_MUNICIPALITIES_PHASE_1 = [
    {
        # Toronto's own portal (secure.toronto.ca/council) needs a custom
        # scraper. Until ON-001 lands the portal source ships PENDING and
        # YouTube remains ACTIVE for video coverage.
        "name": "City of Toronto",
        "short_name": "Toronto",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_SINGLE,
        "website_url": "https://www.toronto.ca/",
        "population": 2794356,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": "https://secure.toronto.ca/council/",
                "label": "Toronto Council Portal (pending custom scraper)",
                "scrape_status": ScrapeStatus.PENDING,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityoftoronto",
                "label": "Toronto YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Ottawa",
        "short_name": "Ottawa",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_SINGLE,
        "website_url": "https://ottawa.ca/",
        "population": 1017449,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://app06.ottawa.ca/sirepub/meet.aspx",
                "label": "Ottawa eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofottawa",
                "label": "Ottawa YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Mississauga",
        "short_name": "Mississauga",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_LOWER,
        "website_url": "https://www.mississauga.ca/",
        "population": 717961,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-mississauga.escribemeetings.com",
                "label": "Mississauga eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofmississauga",
                "label": "Mississauga YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Brampton",
        "short_name": "Brampton",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_LOWER,
        "website_url": "https://www.brampton.ca/",
        "population": 656480,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-brampton.escribemeetings.com",
                "label": "Brampton eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofbrampton",
                "label": "Brampton YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Hamilton",
        "short_name": "Hamilton",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_SINGLE,
        "website_url": "https://www.hamilton.ca/",
        "population": 569353,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-hamilton.escribemeetings.com",
                "label": "Hamilton eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofhamilton",
                "label": "Hamilton YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of London",
        "short_name": "London",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_SINGLE,
        "website_url": "https://london.ca/",
        "population": 422324,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-london.escribemeetings.com",
                "label": "London eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityoflondonont",
                "label": "London YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Markham",
        "short_name": "Markham",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_LOWER,
        "website_url": "https://www.markham.ca/",
        "population": 338503,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-markham.escribemeetings.com",
                "label": "Markham eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofmarkham",
                "label": "Markham YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Vaughan",
        "short_name": "Vaughan",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_LOWER,
        "website_url": "https://www.vaughan.ca/",
        "population": 323103,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-vaughan.escribemeetings.com",
                "label": "Vaughan eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofvaughan",
                "label": "Vaughan YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Kitchener",
        "short_name": "Kitchener",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_LOWER,
        "website_url": "https://www.kitchener.ca/",
        "population": 256885,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-kitchener.escribemeetings.com",
                "label": "Kitchener eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofkitchener",
                "label": "Kitchener YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
    {
        "name": "City of Windsor",
        "short_name": "Windsor",
        "gov_type": GovType.CITY,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": TIER_SINGLE,
        "website_url": "https://www.citywindsor.ca/",
        "population": 229660,
        "sources": [
            {
                "platform": Platform.ESCRIBE,
                "source_type": SourceType.AGENDA,
                "url": "https://pub-windsor.escribemeetings.com",
                "label": "Windsor eScribe Portal",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
            {
                "platform": Platform.YOUTUBE,
                "source_type": SourceType.VIDEO,
                "url": "https://www.youtube.com/@cityofwindsor",
                "label": "Windsor YouTube Council Meetings",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]


# =============================================================================
# Ontario — Remainder seed (PENDING placeholders for the 30 upper-tier
# regions/counties + ~200 lower/single-tier munis from the public registry)
# =============================================================================
_ONTARIO_DIRECTORY_URL = "https://www.amo.on.ca/about-us/who-we-are/member-municipalities"


def _on_pending(
    *,
    name: str,
    short_name: str,
    gov_type: GovType,
    tier: str,
    website_url: str | None = None,
) -> dict:
    """Build a placeholder Ontario municipality entry for Phase 2+ rollout."""
    return {
        "name": name,
        "short_name": short_name,
        "gov_type": gov_type,
        "region": "Ontario",
        "province": PROVINCE_ON,
        "tier": tier,
        "website_url": website_url,
        "population": None,
        "sources": [
            {
                "platform": Platform.CUSTOM,
                "source_type": SourceType.AGENDA,
                "url": f"{_ONTARIO_DIRECTORY_URL}#{short_name.replace(' ', '-')}",
                "label": f"{short_name} council meetings (pending)",
                "scrape_status": ScrapeStatus.PENDING,
            },
        ],
    }


# 30 upper-tier municipalities (counties + regional municipalities). These
# all run their own councils that publish agendas/minutes via eSCRIBE or
# CivicWeb — Phases 2+ will patch in the real portal URLs.
_ON_UPPER_TIER = [
    # Regional Municipalities (8)
    ("Regional Municipality of Durham", "Durham Region"),
    ("Regional Municipality of Halton", "Halton Region"),
    ("Regional Municipality of Niagara", "Niagara Region"),
    ("Regional Municipality of Peel", "Peel Region"),
    ("Regional Municipality of Waterloo", "Waterloo Region"),
    ("Regional Municipality of York", "York Region"),
    ("County of Bruce", "Bruce County"),
    ("County of Dufferin", "Dufferin County"),
    # Counties (22)
    ("County of Elgin", "Elgin County"),
    ("County of Essex", "Essex County"),
    ("County of Frontenac", "Frontenac County"),
    ("County of Grey", "Grey County"),
    ("County of Haliburton", "Haliburton County"),
    ("Haldimand-Norfolk", "Haldimand-Norfolk"),
    ("County of Hastings", "Hastings County"),
    ("County of Huron", "Huron County"),
    ("County of Lambton", "Lambton County"),
    ("Counties of Leeds and Grenville", "Leeds and Grenville"),
    ("County of Lanark", "Lanark County"),
    ("County of Lennox and Addington", "Lennox and Addington"),
    ("County of Middlesex", "Middlesex County"),
    ("Muskoka District", "Muskoka"),
    ("County of Northumberland", "Northumberland County"),
    ("Oxford County", "Oxford County"),
    ("County of Perth", "Perth County"),
    ("County of Peterborough", "Peterborough County"),
    ("United Counties of Prescott and Russell", "Prescott and Russell"),
    ("United Counties of Stormont, Dundas and Glengarry", "SDG Counties"),
    ("County of Renfrew", "Renfrew County"),
    ("County of Simcoe", "Simcoe County"),
    ("County of Wellington", "Wellington County"),
]


# Lower / single-tier municipalities derived from Wikipedia's public list
# (List of municipalities in Ontario). This is not the full 444 — about
# ~210 entries — but covers all the cities/towns/townships with a public
# council page. Tier classification follows OMAFRA's official list:
#   - Single-tier: stand-alone (e.g. Toronto, Ottawa, Hamilton, Greater
#     Sudbury, Kawartha Lakes, Norfolk County, Prince Edward County)
#   - Lower-tier: located inside one of the 30 upper-tier regions/counties
#
# Phase 1 munis (Toronto..Windsor) are excluded so they aren't double-seeded.
_ON_PHASE_1_SHORT_NAMES = {m["short_name"] for m in ONTARIO_MUNICIPALITIES_PHASE_1}
_ON_REMAINDER_SINGLE = [
    # Stand-alone single-tier munis (all are Cities unless noted).
    ("City of Barrie", "Barrie"),
    ("City of Belleville", "Belleville"),
    ("City of Brant", "Brant"),
    ("City of Brantford", "Brantford"),
    ("City of Brockville", "Brockville"),
    ("City of Cornwall", "Cornwall"),
    ("City of Greater Sudbury", "Greater Sudbury"),
    ("City of Guelph", "Guelph"),
    ("City of Haldimand", "Haldimand County"),
    ("City of Kawartha Lakes", "Kawartha Lakes"),
    ("City of Kingston", "Kingston"),
    ("City of Norfolk", "Norfolk County"),
    ("County of Prince Edward", "Prince Edward County"),
    ("City of Orillia", "Orillia"),
    ("City of Pembroke", "Pembroke"),
    ("City of Peterborough", "Peterborough"),
    ("City of Prescott", "Prescott"),
    ("City of Quinte West", "Quinte West"),
    ("City of Sarnia", "Sarnia"),
    ("City of Sault Ste. Marie", "Sault Ste. Marie"),
    ("City of St. Thomas", "St. Thomas"),
    ("City of Stratford", "Stratford"),
    ("City of Temiskaming Shores", "Temiskaming Shores"),
    ("City of Thunder Bay", "Thunder Bay"),
    ("City of Timmins", "Timmins"),
    ("City of North Bay", "North Bay"),
    ("City of Oshawa", "Oshawa"),
]


_ON_REMAINDER_LOWER = [
    # Towns / townships / villages located inside an upper-tier county/region.
    ("Town of Ajax", "Ajax"),
    ("Town of Amherstburg", "Amherstburg"),
    ("Town of Aurora", "Aurora"),
    ("Town of Aylmer", "Aylmer"),
    ("Township of Adelaide Metcalfe", "Adelaide Metcalfe"),
    ("Township of Adjala-Tosorontio", "Adjala-Tosorontio"),
    ("Township of Alberton", "Alberton"),
    ("Township of Alfred and Plantagenet", "Alfred and Plantagenet"),
    ("Township of Algonquin Highlands", "Algonquin Highlands"),
    ("Township of Amaranth", "Amaranth"),
    ("Township of Armour", "Armour"),
    ("Township of Armstrong", "Armstrong"),
    ("Township of Asphodel-Norwood", "Asphodel-Norwood"),
    ("Township of Assiginack", "Assiginack"),
    ("Township of Athens", "Athens"),
    ("Township of Augusta", "Augusta"),
    ("Township of Baldwin", "Baldwin"),
    ("Town of Bancroft", "Bancroft"),
    ("Township of Beckwith", "Beckwith"),
    ("Township of Billings", "Billings"),
    ("Town of Blind River", "Blind River"),
    ("Municipality of Bluewater", "Bluewater"),
    ("Township of Bonfield", "Bonfield"),
    ("Town of Bracebridge", "Bracebridge"),
    ("Town of Bradford West Gwillimbury", "Bradford West Gwillimbury"),
    ("Municipality of Brighton", "Brighton"),
    ("Township of Brock", "Brock"),
    ("Municipality of Brockton", "Brockton"),
    ("Town of Burlington", "Burlington"),
    ("Town of Caledon", "Caledon"),
    ("Municipality of Callander", "Callander"),
    ("Township of Calvin", "Calvin"),
    ("City of Cambridge", "Cambridge"),
    ("Township of Carling", "Carling"),
    ("Township of Casey", "Casey"),
    ("Village of Casselman", "Casselman"),
    ("Township of Centre Hastings", "Centre Hastings"),
    ("Township of Centre Wellington", "Centre Wellington"),
    ("Township of Chamberlain", "Chamberlain"),
    ("Township of Champlain", "Champlain"),
    ("Township of Chapleau", "Chapleau"),
    ("Township of Chapple", "Chapple"),
    ("Township of Chatham-Kent", "Chatham-Kent"),
    ("Township of Chatsworth", "Chatsworth"),
    ("Township of Chisholm", "Chisholm"),
    ("Township of Clarence-Rockland", "Clarence-Rockland"),
    ("Municipality of Clarington", "Clarington"),
    ("Township of Clearview", "Clearview"),
    ("Town of Cobalt", "Cobalt"),
    ("Town of Cobourg", "Cobourg"),
    ("Town of Cochrane", "Cochrane"),
    ("Township of Coleman", "Coleman"),
    ("Town of Collingwood", "Collingwood"),
    ("Township of Conmee", "Conmee"),
    ("Township of Cramahe", "Cramahe"),
    ("Township of Dawson", "Dawson"),
    ("Town of Deep River", "Deep River"),
    ("Town of Deseronto", "Deseronto"),
    ("Township of Dorion", "Dorion"),
    ("Town of Dryden", "Dryden"),
    ("Township of Drummond/North Elmsley", "Drummond/North Elmsley"),
    ("Town of East Gwillimbury", "East Gwillimbury"),
    ("Township of East Hawkesbury", "East Hawkesbury"),
    ("Township of East Zorra-Tavistock", "East Zorra-Tavistock"),
    ("Township of Edwardsburgh/Cardinal", "Edwardsburgh/Cardinal"),
    ("Town of Elliot Lake", "Elliot Lake"),
    ("Township of Emo", "Emo"),
    ("Township of Enniskillen", "Enniskillen"),
    ("Town of Erin", "Erin"),
    ("Town of Espanola", "Espanola"),
    ("Township of Essa", "Essa"),
    ("Town of Essex", "Essex"),
    ("Township of Faraday", "Faraday"),
    ("Town of Fort Erie", "Fort Erie"),
    ("Town of Fort Frances", "Fort Frances"),
    ("Municipality of French River", "French River"),
    ("Town of Gananoque", "Gananoque"),
    ("Township of Gauthier", "Gauthier"),
    ("Town of Georgina", "Georgina"),
    ("Township of Georgian Bay", "Georgian Bay"),
    ("Township of Georgian Bluffs", "Georgian Bluffs"),
    ("Township of Gillies", "Gillies"),
    ("Town of Goderich", "Goderich"),
    ("Town of Gore Bay", "Gore Bay"),
    ("Town of Grand Valley", "Grand Valley"),
    ("Town of Gravenhurst", "Gravenhurst"),
    ("Municipality of Greenstone", "Greenstone"),
    ("Town of Greater Napanee", "Greater Napanee"),
    ("Town of Grimsby", "Grimsby"),
    ("Township of Hamilton", "Hamilton Township"),
    ("Town of Halton Hills", "Halton Hills"),
    ("Town of Hanover", "Hanover"),
    ("Township of Harley", "Harley"),
    ("Township of Harris", "Harris"),
    ("Town of Hawkesbury", "Hawkesbury"),
    ("Town of Hearst", "Hearst"),
    ("Municipality of Highlands East", "Highlands East"),
    ("Township of Hilliard", "Hilliard"),
    ("Township of Hilton", "Hilton"),
    ("Township of Horton", "Horton"),
    ("Township of Howick", "Howick"),
    ("Township of Hudson", "Hudson"),
    ("Town of Huntsville", "Huntsville"),
    ("Township of Huron East", "Huron East"),
    ("Township of Ignace", "Ignace"),
    ("Town of Ingersoll", "Ingersoll"),
    ("Township of Innisfil", "Innisfil"),
    ("Township of James", "James"),
    ("Town of Jocelyn", "Jocelyn"),
    ("Township of Johnson", "Johnson"),
    ("Township of Joly", "Joly"),
    ("Town of Kearney", "Kearney"),
    ("Township of Kerns", "Kerns"),
    ("Municipality of Killarney", "Killarney"),
    ("Town of Kincardine", "Kincardine"),
    ("Township of King", "King"),
    ("Town of Kingsville", "Kingsville"),
    ("Township of LaSalle", "LaSalle"),
    ("Township of Laird", "Laird"),
    ("Township of Lake of the Woods", "Lake of the Woods"),
    ("Township of Lakeshore", "Lakeshore"),
    ("Town of Larder Lake", "Larder Lake"),
    ("Town of Latchford", "Latchford"),
    ("Town of Leamington", "Leamington"),
    ("Township of Limerick", "Limerick"),
    ("Town of Lincoln", "Lincoln"),
    ("Township of Loyalist", "Loyalist"),
    ("Township of Machar", "Machar"),
    ("Township of Machin", "Machin"),
    ("Township of Madawaska Valley", "Madawaska Valley"),
    ("Township of Malahide", "Malahide"),
    ("Township of Mapleton", "Mapleton"),
    ("Town of Marathon", "Marathon"),
    ("Town of Mattawa", "Mattawa"),
    ("Township of Mattawan", "Mattawan"),
    ("Township of McDougall", "McDougall"),
    ("Township of McGarry", "McGarry"),
    ("Township of McKellar", "McKellar"),
    ("Town of Meaford", "Meaford"),
    ("Township of Melancthon", "Melancthon"),
    ("Town of Midland", "Midland"),
    ("Town of Milton", "Milton"),
    ("Town of Minto", "Minto"),
    ("Township of Mississippi Mills", "Mississippi Mills"),
    ("Township of Mono", "Mono"),
    ("Township of Montague", "Montague"),
    ("Town of Moonbeam", "Moonbeam"),
    ("Township of Morley", "Morley"),
    ("Town of Mulmur", "Mulmur"),
    ("Town of Newmarket", "Newmarket"),
    ("Town of Niagara Falls", "Niagara Falls"),
    ("Town of Niagara-on-the-Lake", "Niagara-on-the-Lake"),
    ("Township of Nipissing", "Nipissing"),
    ("Township of North Dundas", "North Dundas"),
    ("Township of North Glengarry", "North Glengarry"),
    ("Township of North Huron", "North Huron"),
    ("Township of North Middlesex", "North Middlesex"),
    ("Township of North Perth", "North Perth"),
    ("Township of Norwich", "Norwich"),
    ("Township of O'Connor", "O'Connor"),
    ("Town of Oakville", "Oakville"),
    ("Town of Oil Springs", "Oil Springs"),
    ("Town of Orangeville", "Orangeville"),
    ("Township of Otonabee-South Monaghan", "Otonabee-South Monaghan"),
    ("Town of Parry Sound", "Parry Sound"),
    ("Municipality of Pelee", "Pelee"),
    ("Town of Pelham", "Pelham"),
    ("Township of Perry", "Perry"),
    ("Town of Perth", "Perth"),
    ("Township of Perth East", "Perth East"),
    ("Township of Perth South", "Perth South"),
    ("Town of Petawawa", "Petawawa"),
    ("Town of Petrolia", "Petrolia"),
    ("City of Pickering", "Pickering"),
    ("Village of Point Edward", "Point Edward"),
    ("Town of Port Hope", "Port Hope"),
    ("Town of Powassan", "Powassan"),
    ("Township of Puslinch", "Puslinch"),
    ("Township of Rainy River", "Rainy River"),
    ("Town of Red Lake", "Red Lake"),
    ("Town of Red Rock", "Red Rock"),
    ("Town of Renfrew", "Renfrew"),
    ("Town of Richmond Hill", "Richmond Hill"),
    ("Township of Russell", "Russell"),
    ("Township of Ryerson", "Ryerson"),
    ("Township of Sables-Spanish Rivers", "Sables-Spanish Rivers"),
    ("Town of Saugeen Shores", "Saugeen Shores"),
    ("Town of Schreiber", "Schreiber"),
    ("Township of Seguin", "Seguin"),
    ("Township of Selwyn", "Selwyn"),
    ("Township of Severn", "Severn"),
    ("Town of Shelburne", "Shelburne"),
    ("Township of Sioux Lookout", "Sioux Lookout"),
    ("Town of Smiths Falls", "Smiths Falls"),
    ("Town of South Bruce", "South Bruce"),
    ("Township of South Dundas", "South Dundas"),
    ("Township of South Glengarry", "South Glengarry"),
    ("Town of South River", "South River"),
    ("Township of South Stormont", "South Stormont"),
    ("Township of South-West Oxford", "South-West Oxford"),
    ("Township of Southgate", "Southgate"),
    ("Township of Southwest Middlesex", "Southwest Middlesex"),
    ("Township of Southwold", "Southwold"),
    ("Town of Spanish", "Spanish"),
    ("Township of Springwater", "Springwater"),
    ("Township of St. Charles", "St. Charles"),
    ("Township of St. Clair", "St. Clair"),
    ("Township of St. Joseph", "St. Joseph"),
    ("Town of St. Marys", "St. Marys"),
    ("Township of Strathroy-Caradoc", "Strathroy-Caradoc"),
    ("Township of Strong", "Strong"),
    ("Village of Sundridge", "Sundridge"),
    ("Township of Tarbutt", "Tarbutt"),
    ("Township of Tay", "Tay"),
    ("Township of Tay Valley", "Tay Valley"),
    ("Town of Tecumseh", "Tecumseh"),
    ("Town of The Blue Mountains", "The Blue Mountains"),
    ("Municipality of The Nation", "The Nation"),
    ("Township of The North Shore", "The North Shore"),
    ("Town of Thessalon", "Thessalon"),
    ("Township of Tiny", "Tiny"),
    ("Town of Trent Hills", "Trent Hills"),
    ("Township of Trent Lakes", "Trent Lakes"),
    ("Municipality of Tweed", "Tweed"),
    ("Township of Tyendinaga", "Tyendinaga"),
    ("Town of Uxbridge", "Uxbridge"),
    ("Township of Wainfleet", "Wainfleet"),
    ("Town of Wasaga Beach", "Wasaga Beach"),
    ("Township of Warwick", "Warwick"),
    ("City of Waterloo", "Waterloo"),
    ("Town of Wawa", "Wawa"),
    ("Township of Wellesley", "Wellesley"),
    ("Township of Wellington North", "Wellington North"),
    ("Township of West Elgin", "West Elgin"),
    ("Township of West Lincoln", "West Lincoln"),
    ("Township of West Nipissing", "West Nipissing"),
    ("Township of West Perth", "West Perth"),
    ("Town of Whitby", "Whitby"),
    ("Town of Whitchurch-Stouffville", "Whitchurch-Stouffville"),
    ("Town of White River", "White River"),
    ("Township of Whitestone", "Whitestone"),
    ("Township of Whitewater Region", "Whitewater Region"),
    ("Township of Wilmot", "Wilmot"),
    ("Township of Wollaston", "Wollaston"),
    ("Township of Woodstock", "Woodstock"),
    ("Township of Woolwich", "Woolwich"),
    ("Town of Welland", "Welland"),
    ("Town of Newbury", "Newbury"),
    ("Town of Hudson", "Hudson"),
    ("Town of Westport", "Westport"),
    ("Township of Tudor and Cashel", "Tudor and Cashel"),
    ("Township of Frontenac Islands", "Frontenac Islands"),
    ("Township of Stone Mills", "Stone Mills"),
    ("Township of Greater Madawaska", "Greater Madawaska"),
    ("Township of Admaston/Bromley", "Admaston/Bromley"),
    ("Township of McNab/Braeside", "McNab/Braeside"),
    ("Township of North Frontenac", "North Frontenac"),
    ("Township of Central Frontenac", "Central Frontenac"),
    ("Township of South Frontenac", "South Frontenac"),
    ("Township of Brudenell, Lyndoch and Raglan", "Brudenell, Lyndoch and Raglan"),
    ("Township of Lanark Highlands", "Lanark Highlands"),
    ("Township of Carlow/Mayo", "Carlow/Mayo"),
    ("Township of Highlands of Cardiff", "Highlands of Cardiff"),
    ("Township of Bonnechere Valley", "Bonnechere Valley"),
    ("Township of Madoc", "Madoc"),
    ("Township of Stirling-Rawdon", "Stirling-Rawdon"),
    ("Township of Tweed (legacy)", "Tweed (legacy)"),
    ("Town of Mattice-Val Côté", "Mattice-Val Côté"),
    ("Town of Manitouwadge", "Manitouwadge"),
    ("Town of Atikokan", "Atikokan"),
    ("Town of Kapuskasing", "Kapuskasing"),
    ("Town of Iroquois Falls", "Iroquois Falls"),
    ("Town of Smooth Rock Falls", "Smooth Rock Falls"),
    ("Town of Black River-Matheson", "Black River-Matheson"),
    ("Town of Cochrane (legacy)", "Cochrane (legacy)"),
    ("Town of Opasatika", "Opasatika"),
    ("Town of Charlton and Dack", "Charlton and Dack"),
    ("Town of Englehart", "Englehart"),
    ("Town of Kirkland Lake", "Kirkland Lake"),
    ("Township of Larder Lake (legacy)", "Larder Lake (legacy)"),
    ("Township of Schreiber (legacy)", "Schreiber (legacy)"),
    ("Township of Manitouwadge (legacy)", "Manitouwadge (legacy)"),
]


def _build_ontario_remainder() -> list[dict]:
    """Materialize the placeholder Ontario entries from the typed source lists.

    The output skips short_names already in Phase 1 to avoid duplicate seeds.
    """
    out: list[dict] = []

    for name, short in _ON_UPPER_TIER:
        if short in _ON_PHASE_1_SHORT_NAMES:
            continue
        out.append(_on_pending(
            name=name, short_name=short,
            gov_type=GovType.REGIONAL_DISTRICT, tier=TIER_UPPER,
        ))

    for name, short in _ON_REMAINDER_SINGLE:
        if short in _ON_PHASE_1_SHORT_NAMES:
            continue
        # Most ON single-tier munis are cities; gov_type=CITY is closest fit.
        out.append(_on_pending(
            name=name, short_name=short,
            gov_type=GovType.CITY, tier=TIER_SINGLE,
        ))

    for name, short in _ON_REMAINDER_LOWER:
        if short in _ON_PHASE_1_SHORT_NAMES:
            continue
        out.append(_on_pending(
            name=name, short_name=short,
            gov_type=GovType.TOWN, tier=TIER_LOWER,
        ))

    # Dedupe by short_name (the lower-tier list may collide with single-tier).
    seen: set[str] = set()
    deduped: list[dict] = []
    for muni in out:
        if muni["short_name"] in seen:
            continue
        seen.add(muni["short_name"])
        deduped.append(muni)
    return deduped


def _apply_ontario_remainder_patches(entries: list[dict]) -> list[dict]:
    """Merge the auto-generated probe patches onto the ON placeholder roster.

    Mirrors ``_apply_remainder_patches`` (Alberta) — see its docstring for
    the full design discussion.
    """
    try:
        from app.services._on_remainder_patches import REMAINDER_PATCHES
    except ImportError:
        return entries

    enum_lookup = {
        "Platform.CIVICWEB": Platform.CIVICWEB,
        "Platform.GRANICUS": Platform.GRANICUS,
        "Platform.ESCRIBE": Platform.ESCRIBE,
        "Platform.YOUTUBE": Platform.YOUTUBE,
        "Platform.CIVICPLUS": Platform.CIVICPLUS,
        "Platform.CUSTOM": Platform.CUSTOM,
        "Platform.UNKNOWN": Platform.UNKNOWN,
        "SourceType.AGENDA": SourceType.AGENDA,
        "SourceType.MINUTES": SourceType.MINUTES,
        "SourceType.VIDEO": SourceType.VIDEO,
        "SourceType.NOTICE": SourceType.NOTICE,
        "SourceType.BYLAW": SourceType.BYLAW,
        "ScrapeStatus.ACTIVE": ScrapeStatus.ACTIVE,
        "ScrapeStatus.PENDING": ScrapeStatus.PENDING,
        "ScrapeStatus.BROKEN": ScrapeStatus.BROKEN,
        "ScrapeStatus.DISABLED": ScrapeStatus.DISABLED,
    }

    def _resolve(source: dict) -> dict:
        return {
            "platform": enum_lookup[source["platform"]],
            "source_type": enum_lookup[source["source_type"]],
            "url": source["url"],
            "label": source["label"],
            "scrape_status": enum_lookup[source["scrape_status"]],
        }

    for entry in entries:
        patch = REMAINDER_PATCHES.get(entry["short_name"])
        if not patch:
            continue
        if patch.get("website_url"):
            entry["website_url"] = patch["website_url"]
        sources = [_resolve(s) for s in patch.get("sources", [])]
        if sources:
            entry["sources"] = sources

    return entries


ONTARIO_MUNICIPALITIES_REMAINDER: list[dict] = _apply_ontario_remainder_patches(
    _build_ontario_remainder()
)


# All BC and AB batches concatenated — public for tests that want to
# walk the entire registry without poking private internals.
BC_BATCHES = [
    CRD_MUNICIPALITIES,
    BC_MUNICIPALITIES_BATCH_1,
    BC_MUNICIPALITIES_BATCH_2,
    BC_MUNICIPALITIES_BATCH_3,
    BC_MUNICIPALITIES_BATCH_4,
    BC_MUNICIPALITIES_BATCH_5,
    BC_MUNICIPALITIES_BATCH_6,
    BC_MUNICIPALITIES_BATCH_7,
    BC_MUNICIPALITIES_BATCH_8,
    BC_MUNICIPALITIES_BATCH_9,
    BC_MUNICIPALITIES_BATCH_10,
    BC_MUNICIPALITIES_BATCH_11,
    BC_MUNICIPALITIES_BATCH_12,
    BC_MUNICIPALITIES_BATCH_13,
    BC_MUNICIPALITIES_BATCH_14,
    BC_MUNICIPALITIES_BATCH_15,
    BC_MUNICIPALITIES_BATCH_16,
    BC_MUNICIPALITIES_BATCH_17,
]

AB_BATCHES = [
    ALBERTA_MUNICIPALITIES_PHASE_1,
    ALBERTA_MUNICIPALITIES_REMAINDER,
]

ON_BATCHES = [
    ONTARIO_MUNICIPALITIES_PHASE_1,
    ONTARIO_MUNICIPALITIES_REMAINDER,
]


def _normalize_province(muni: dict) -> dict:
    """Return a copy of muni with a ``province`` key.

    Existing BC seed dicts predate Alberta support and may omit the field;
    treat them as BC. Alberta dicts always include ``province=PROVINCE_AB``
    explicitly.
    """
    if "province" in muni:
        return muni
    out = dict(muni)
    out["province"] = PROVINCE_BC
    return out


async def seed_registry(db: AsyncSession) -> dict:
    """Seed the registry with BC + Alberta municipalities and sources.

    Returns a summary of what was created vs already existed. Idempotent:
    re-running adds new sources/munis without duplicating existing rows.
    """
    stats = {"municipalities_created": 0, "municipalities_existed": 0, "sources_created": 0}

    all_municipalities: list[dict] = []
    for batch in BC_BATCHES + AB_BATCHES + ON_BATCHES:
        all_municipalities.extend(batch)

    for muni_data in all_municipalities:
        muni_data = _normalize_province(muni_data)
        sources_data = muni_data.get("sources", [])
        muni_fields = {k: v for k, v in muni_data.items() if k != "sources"}

        # Match on (short_name, province) to support BC/AB short_name overlap
        # (e.g. "Lacombe" exists as both a BC place and an AB city).
        result = await db.execute(
            select(Municipality).where(
                Municipality.short_name == muni_fields["short_name"],
                Municipality.province == muni_fields["province"],
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            stats["municipalities_existed"] += 1
            muni = existing
        else:
            muni = Municipality(**muni_fields)
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

        # Demote any stale AB-directory PENDING placeholders to DISABLED once
        # this muni has at least one *real* (non-placeholder) source. Without
        # this, the poller wastes a request on the placeholder URL on every
        # cron tick. We don't delete the row to preserve scrape_run history.
        placeholder_substr = "alberta.ca/find-a-municipal-official"
        non_placeholder_seed_urls = {
            s["url"] for s in sources_data if placeholder_substr not in s["url"]
        }
        if non_placeholder_seed_urls:
            stale = await db.execute(
                select(Source).where(
                    Source.municipality_id == muni.id,
                    Source.url.like(f"%{placeholder_substr}%"),
                    Source.scrape_status != ScrapeStatus.DISABLED,
                )
            )
            for placeholder_source in stale.scalars().all():
                placeholder_source.scrape_status = ScrapeStatus.DISABLED

    await db.commit()
    return stats
