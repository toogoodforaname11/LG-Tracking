"""Custom scraper for Port McNeill.

Source URL: https://www.portmcneill.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PortMcNeillScraper(BCMunicipalScraper):
    """Scraper for Port McNeill council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
