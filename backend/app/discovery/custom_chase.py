"""Custom scraper for Chase.

Source URL: https://www.chasebc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ChaseScraper(BCMunicipalScraper):
    """Scraper for Chase council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
