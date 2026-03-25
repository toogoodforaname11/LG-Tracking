"""Custom scraper for Houston.

Source URL: https://www.houston.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class HoustonScraper(BCMunicipalScraper):
    """Scraper for Houston council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
