"""Custom scraper for Clearwater.

Source URL: https://www.clearwaterbc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ClearwaterScraper(BCMunicipalScraper):
    """Scraper for Clearwater council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
