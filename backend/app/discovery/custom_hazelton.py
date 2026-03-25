"""Custom scraper for Hazelton.

Source URL: https://www.hazelton.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class HazeltonScraper(BCMunicipalScraper):
    """Scraper for Hazelton council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
