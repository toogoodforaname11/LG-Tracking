"""Custom scraper for Montrose.

Source URL: https://www.montrose.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class MontroseScraper(BCMunicipalScraper):
    """Scraper for Montrose council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
