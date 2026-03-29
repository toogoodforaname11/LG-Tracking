"""Custom scraper for City of Williams Lake.

Source URL: https://www.williamslake.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class WilliamsLakeScraper(BCMunicipalScraper):
    """Scraper for City of Williams Lake council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
