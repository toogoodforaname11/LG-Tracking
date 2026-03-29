"""Custom scraper for Port Clements.

Source URL: https://www.portclements.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PortClementsScraper(BCMunicipalScraper):
    """Scraper for Port Clements council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
