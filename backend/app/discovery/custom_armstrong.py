"""Custom scraper for City of Armstrong.

Source URL: https://www.armstrong.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ArmstrongScraper(BCMunicipalScraper):
    """Scraper for City of Armstrong council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
