"""Custom scraper for Salmo.

Source URL: https://www.salmo.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SalmoScraper(BCMunicipalScraper):
    """Scraper for Salmo council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
