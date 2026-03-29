"""Custom scraper for Belcarra.

Source URL: https://www.belcarra.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class BelcarraScraper(BCMunicipalScraper):
    """Scraper for Belcarra council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
