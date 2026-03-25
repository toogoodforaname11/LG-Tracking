"""Custom scraper for Princeton.

Source URL: https://www.princeton.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PrincetonScraper(BCMunicipalScraper):
    """Scraper for Princeton council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
