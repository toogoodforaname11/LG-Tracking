"""Custom scraper for City of Nelson.

Source URL: https://www.nelson.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class NelsonScraper(BCMunicipalScraper):
    """Scraper for City of Nelson council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
