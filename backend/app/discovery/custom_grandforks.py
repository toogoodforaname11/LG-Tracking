"""Custom scraper for City of Grand Forks.

Source URL: https://www.grandforks.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class GrandForksScraper(BCMunicipalScraper):
    """Scraper for City of Grand Forks council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
