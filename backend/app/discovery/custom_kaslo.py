"""Custom scraper for Kaslo.

Source URL: https://www.kaslo.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class KasloScraper(BCMunicipalScraper):
    """Scraper for Kaslo council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
