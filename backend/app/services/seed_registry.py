"""Seed the sources registry with BC municipalities and their known data sources."""

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
        "name": "District of Central Saanich",
        "short_name": "Central Saanich",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.centralsaanich.ca/",
        "population": 18576,
        # Also in CRD list above (CivicWeb); Granicus source added here.
        "sources": [
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
        "name": "District of Oak Bay",
        "short_name": "Oak Bay",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.oakbay.ca/",
        "population": 18094,
        # Already in CRD list (portal URLs); adding specific meeting-list pages.
        "sources": [
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
        "name": "District of Saanich",
        "short_name": "Saanich",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.saanich.ca/",
        "population": 117735,
        # Already in CRD list (custom); Granicus source added here.
        "sources": [
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
        "name": "City of Victoria",
        "short_name": "Victoria",
        "gov_type": GovType.CITY,
        "region": "CRD",
        "website_url": "https://www.victoria.ca/",
        "population": 91867,
        # Already in CRD list (CivicWeb); eScribe source added here.
        "sources": [
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
    {
        "name": "Town of View Royal",
        "short_name": "View Royal",
        "gov_type": GovType.TOWN,
        "region": "CRD",
        "website_url": "https://www.viewroyal.ca/",
        "population": 11575,
        # Already in CRD list (custom); CivicWeb source added here.
        "sources": [
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
        "name": "District of Sooke",
        "short_name": "Sooke",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.sooke.ca/",
        "population": 15054,
        # Already in CRD list; adding specific meeting-list pages.
        "sources": [
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
        "name": "Town of Sidney",
        "short_name": "Sidney",
        "gov_type": GovType.TOWN,
        "region": "CRD",
        "website_url": "https://www.sidney.ca/",
        "population": 12405,
        # Already in CRD list (custom); CivicWeb source added here.
        "sources": [
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
        "name": "District of North Saanich",
        "short_name": "North Saanich",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://northsaanich.ca/",
        "population": 12220,
        # Already in CRD list; adding specific meeting-list pages.
        "sources": [
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
        "name": "District of Metchosin",
        "short_name": "Metchosin",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.metchosin.ca/",
        "population": 5169,
        # Already in CRD list; adding specific meeting-list pages.
        "sources": [
            {
                "platform": Platform.CIVICWEB,
                "source_type": SourceType.AGENDA,
                "url": "https://metchosin.civicweb.net/Portal/MeetingTypeList.aspx",
                "label": "Metchosin CivicWeb Meeting List",
                "scrape_status": ScrapeStatus.ACTIVE,
            },
        ],
    },
]

# Batch 6 – 10 municipalities with correct specific meeting pages
BC_MUNICIPALITIES_BATCH_6 = [
    {
        "name": "City of Langford",
        "short_name": "Langford",
        "gov_type": GovType.CITY,
        "region": "CRD",
        "website_url": "https://langford.ca/",
        "population": 46584,
        # Already in CRD list (custom); CivicWeb source added here.
        "sources": [
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
        "name": "Township of Esquimalt",
        "short_name": "Esquimalt",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.esquimalt.ca/",
        "population": 17655,
        # Already in CRD list (custom); CivicWeb source added here.
        "sources": [
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
        "name": "District of Highlands",
        "short_name": "Highlands",
        "gov_type": GovType.DISTRICT,
        "region": "CRD",
        "website_url": "https://www.highlands.ca/",
        "population": 2373,
        # Already in CRD list (custom); CivicWeb source added here.
        "sources": [
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
        "name": "City of Salmon Arm",
        "short_name": "Salmon Arm",
        "gov_type": GovType.CITY,
        "region": "BC",
        "website_url": "https://www.salmonarm.ca/",
        "population": None,
        "sources": [
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
# Note: some entries overlap with Batch 15; duplicates are handled by seed_registry's
# existing-check logic (skipped if short_name already exists).
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
]


async def seed_registry(db: AsyncSession) -> dict:
    """Seed the registry with BC municipalities and sources.

    Returns a summary of what was created vs already existed.
    """
    stats = {"municipalities_created": 0, "municipalities_existed": 0, "sources_created": 0}

    all_municipalities = (
        CRD_MUNICIPALITIES
        + BC_MUNICIPALITIES_BATCH_1
        + BC_MUNICIPALITIES_BATCH_2
        + BC_MUNICIPALITIES_BATCH_3
        + BC_MUNICIPALITIES_BATCH_4
        + BC_MUNICIPALITIES_BATCH_5
        + BC_MUNICIPALITIES_BATCH_6
        + BC_MUNICIPALITIES_BATCH_7
        + BC_MUNICIPALITIES_BATCH_8
        + BC_MUNICIPALITIES_BATCH_9
        + BC_MUNICIPALITIES_BATCH_10
        + BC_MUNICIPALITIES_BATCH_11
        + BC_MUNICIPALITIES_BATCH_12
        + BC_MUNICIPALITIES_BATCH_13
        + BC_MUNICIPALITIES_BATCH_14
        + BC_MUNICIPALITIES_BATCH_15
        + BC_MUNICIPALITIES_BATCH_16
    )
    for muni_data in all_municipalities:
        sources_data = muni_data.get("sources", [])
        muni_fields = {k: v for k, v in muni_data.items() if k != "sources"}

        # Check if municipality already exists
        result = await db.execute(
            select(Municipality).where(Municipality.short_name == muni_fields["short_name"])
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

        # Restore sources_data for potential re-runs
        muni_data["sources"] = sources_data

    await db.commit()
    return stats
