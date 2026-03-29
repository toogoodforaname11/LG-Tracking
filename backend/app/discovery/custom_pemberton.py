"""Custom scraper for Pemberton.

Source URL: https://www.pemberton.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PembertonScraper(BCMunicipalScraper):
    """Scraper for Pemberton council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
