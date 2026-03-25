"""Custom scraper for Fraser Lake.

Source URL: https://www.fraserlake.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class FraserLakeScraper(BCMunicipalScraper):
    """Scraper for Fraser Lake council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
