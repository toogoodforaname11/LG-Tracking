"""Custom scraper for District of 100 Mile House.

Source URL: https://www.100milehouse.com/council-meetings
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class HundredMileHouseScraper(BCMunicipalScraper):
    """Scraper for District of 100 Mile House council meetings."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council-meetings", "council meetings",
    ]
