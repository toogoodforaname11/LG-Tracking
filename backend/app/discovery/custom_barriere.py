"""Custom scraper for Barriere.

Source URL: https://www.barrierebc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class BarriereScraper(BCMunicipalScraper):
    """Scraper for Barriere council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
