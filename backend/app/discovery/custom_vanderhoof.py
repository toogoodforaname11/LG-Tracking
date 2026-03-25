"""Custom scraper for Vanderhoof.

Source URL: https://www.vanderhoof.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class VanderhoofScraper(BCMunicipalScraper):
    """Scraper for Vanderhoof council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
