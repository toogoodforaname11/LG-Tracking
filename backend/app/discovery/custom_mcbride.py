"""Custom scraper for McBride.

Source URL: https://www.mcbride.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class McBrideScraper(BCMunicipalScraper):
    """Scraper for McBride council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
