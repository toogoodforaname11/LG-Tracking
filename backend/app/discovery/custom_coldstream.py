"""Custom scraper for Coldstream.

Source URL: https://www.coldstream.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ColdstreamScraper(BCMunicipalScraper):
    """Scraper for Coldstream council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
