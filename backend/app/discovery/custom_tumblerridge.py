"""Custom scraper for Tumbler Ridge.

Source URL: https://www.tumblerridge.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class TumblerRidgeScraper(BCMunicipalScraper):
    """Scraper for Tumbler Ridge council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
