"""Custom scraper for City of Enderby.

Source URL: https://www.enderby.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class EnderbyScraper(BCMunicipalScraper):
    """Scraper for City of Enderby council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
