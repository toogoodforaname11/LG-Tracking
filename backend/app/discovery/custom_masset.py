"""Custom scraper for Masset.

Source URL: https://www.masset.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class MassetScraper(BCMunicipalScraper):
    """Scraper for Masset council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
