"""Custom scraper for Zeballos.

Source URL: https://www.zeballos.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ZeballosScraper(BCMunicipalScraper):
    """Scraper for Zeballos council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
