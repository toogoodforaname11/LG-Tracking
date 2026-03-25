"""Custom scraper for Tahsis.

Source URL: https://www.tahsis.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class TahsisScraper(BCMunicipalScraper):
    """Scraper for Tahsis council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
