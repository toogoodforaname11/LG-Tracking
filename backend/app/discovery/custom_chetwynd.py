"""Custom scraper for Chetwynd.

Source URL: https://www.chetwynd.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ChetwyndScraper(BCMunicipalScraper):
    """Scraper for Chetwynd council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
