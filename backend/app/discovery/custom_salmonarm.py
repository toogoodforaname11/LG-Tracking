"""Custom scraper for City of Salmon Arm.

Source URL: https://www.salmonarm.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SalmonArmScraper(BCMunicipalScraper):
    """Scraper for City of Salmon Arm council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
