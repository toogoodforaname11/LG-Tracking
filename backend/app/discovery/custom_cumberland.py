"""Custom scraper for Cumberland.

Source URL: https://www.cumberland.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class CumberlandScraper(BCMunicipalScraper):
    """Scraper for Cumberland council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
