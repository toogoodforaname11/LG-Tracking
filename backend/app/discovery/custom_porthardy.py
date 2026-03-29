"""Custom scraper for Port Hardy.

Source URL: https://www.porthardy.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PortHardyScraper(BCMunicipalScraper):
    """Scraper for Port Hardy council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
