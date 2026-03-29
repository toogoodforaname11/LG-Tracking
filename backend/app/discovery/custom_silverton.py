"""Custom scraper for Silverton.

Source URL: https://www.silverton.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SilvertonScraper(BCMunicipalScraper):
    """Scraper for Silverton council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
