"""Custom scraper for Kent.

Source URL: https://www.kentbc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class KentScraper(BCMunicipalScraper):
    """Scraper for Kent council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
