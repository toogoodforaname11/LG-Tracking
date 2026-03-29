"""Custom scraper for Granisle.

Source URL: https://www.granisle.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class GranisleScraper(BCMunicipalScraper):
    """Scraper for Granisle council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
