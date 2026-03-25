"""Custom scraper for Lillooet.

Source URL: https://www.lillooetbc.com/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class LillooetScraper(BCMunicipalScraper):
    """Scraper for Lillooet council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
