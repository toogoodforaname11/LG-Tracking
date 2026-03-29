"""Custom scraper for Wells.

Source URL: https://www.wellsbc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class WellsScraper(BCMunicipalScraper):
    """Scraper for Wells council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
