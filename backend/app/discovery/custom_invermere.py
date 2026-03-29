"""Custom scraper for Invermere.

Source URL: https://www.invermere.net/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class InvermereScraper(BCMunicipalScraper):
    """Scraper for Invermere council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
