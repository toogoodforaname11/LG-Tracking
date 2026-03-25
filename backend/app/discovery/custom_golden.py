"""Custom scraper for Golden.

Source URL: https://www.golden.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class GoldenScraper(BCMunicipalScraper):
    """Scraper for Golden council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
