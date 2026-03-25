"""Custom scraper for Sayward.

Source URL: https://www.sayward.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SaywardScraper(BCMunicipalScraper):
    """Scraper for Sayward council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
