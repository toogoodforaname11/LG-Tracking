"""Custom scraper for Port Alice.

Source URL: https://www.portalice.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PortAliceScraper(BCMunicipalScraper):
    """Scraper for Port Alice council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
