"""Custom scraper for Balfour.

Source URL: https://www.rdkb.com
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class BalfourScraper(BCMunicipalScraper):
    """Scraper for Balfour council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "rdkb",
    ]
