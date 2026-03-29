"""Custom scraper for Cache Creek.

Source URL: https://www.cachecreekbc.com/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class CacheCreekScraper(BCMunicipalScraper):
    """Scraper for Cache Creek council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
