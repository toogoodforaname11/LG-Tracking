"""Custom scraper for Hope.

Source URL: https://www.hope.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class HopeScraper(BCMunicipalScraper):
    """Scraper for Hope council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
