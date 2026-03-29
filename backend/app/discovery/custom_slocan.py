"""Custom scraper for Slocan.

Source URL: https://www.slocan.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SlocanScraper(BCMunicipalScraper):
    """Scraper for Slocan council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
