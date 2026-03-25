"""Custom scraper for Creston.

Source URL: https://www.creston.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class CrestonScraper(BCMunicipalScraper):
    """Scraper for Creston council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
