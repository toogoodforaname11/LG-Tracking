"""Custom scraper for Gibsons.

Source URL: https://www.gibsons.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class GibsonsScraper(BCMunicipalScraper):
    """Scraper for Gibsons council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
