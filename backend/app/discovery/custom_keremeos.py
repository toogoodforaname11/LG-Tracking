"""Custom scraper for Keremeos.

Source URL: https://www.keremeos.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class KeremeosScraper(BCMunicipalScraper):
    """Scraper for Keremeos council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
