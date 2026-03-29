"""Custom scraper for Burns Lake.

Source URL: https://www.burnslake.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class BurnsLakeScraper(BCMunicipalScraper):
    """Scraper for Burns Lake council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
