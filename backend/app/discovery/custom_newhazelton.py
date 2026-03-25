"""Custom scraper for New Hazelton.

Source URL: https://www.newhazelton.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class NewHazeltonScraper(BCMunicipalScraper):
    """Scraper for New Hazelton council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
