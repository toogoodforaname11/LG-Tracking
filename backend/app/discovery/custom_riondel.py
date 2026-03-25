"""Custom scraper for Riondel.

Source URL: https://www.riondel.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class RiondelScraper(BCMunicipalScraper):
    """Scraper for Riondel council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
