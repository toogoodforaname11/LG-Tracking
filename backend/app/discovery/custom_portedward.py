"""Custom scraper for Port Edward.

Source URL: https://www.portedward.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PortEdwardScraper(BCMunicipalScraper):
    """Scraper for Port Edward council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
