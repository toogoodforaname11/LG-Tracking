"""Custom scraper for Telkwa.

Source URL: https://www.telkwa.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class TelkwaScraper(BCMunicipalScraper):
    """Scraper for Telkwa council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
