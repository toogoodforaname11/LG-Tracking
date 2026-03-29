"""Custom scraper for Sicamous.

Source URL: https://www.sicamous.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SicamousScraper(BCMunicipalScraper):
    """Scraper for Sicamous council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
