"""Custom scraper for Rossland.

Source URL: https://www.rossland.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class RosslandScraper(BCMunicipalScraper):
    """Scraper for Rossland council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
