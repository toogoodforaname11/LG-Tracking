"""Custom scraper for Greenwood.

Source URL: https://www.greenwoodbc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class GreenwoodScraper(BCMunicipalScraper):
    """Scraper for Greenwood council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
