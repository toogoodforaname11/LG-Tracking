"""Custom scraper for Kimberley.

Source URL: https://www.kimberley.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class KimberleyScraper(BCMunicipalScraper):
    """Scraper for Kimberley council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
