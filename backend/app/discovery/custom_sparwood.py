"""Custom scraper for Sparwood.

Source URL: https://www.sparwood.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SparwoodScraper(BCMunicipalScraper):
    """Scraper for Sparwood council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
