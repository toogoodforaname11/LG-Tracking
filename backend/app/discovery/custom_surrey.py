"""Custom scraper for City of Surrey.

Source URL: https://www.surrey.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SurreyScraper(BCMunicipalScraper):
    """Scraper for City of Surrey council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws", "public-hearing",
    ]
