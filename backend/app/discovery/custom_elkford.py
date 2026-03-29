"""Custom scraper for Elkford.

Source URL: https://www.elkford.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ElkfordScraper(BCMunicipalScraper):
    """Scraper for Elkford council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
