"""Custom scraper for Northern Rockies.

Source URL: https://www.northernrockies.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class NorthernRockiesScraper(BCMunicipalScraper):
    """Scraper for Northern Rockies council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
