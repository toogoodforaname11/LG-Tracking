"""Custom scraper for Logan Lake.

Source URL: https://www.loganlake.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class LoganLakeScraper(BCMunicipalScraper):
    """Scraper for Logan Lake council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
