"""Custom scraper for Christina Lake.

Source URL: https://www.rdkb.com
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ChristinaLakeScraper(BCMunicipalScraper):
    """Scraper for Christina Lake council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "rdkb",
    ]
