"""Custom scraper for Mackenzie.

Source URL: https://www.mackenzie.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class MackenzieScraper(BCMunicipalScraper):
    """Scraper for Mackenzie council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
