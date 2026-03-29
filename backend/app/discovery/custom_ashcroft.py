"""Custom scraper for Ashcroft.

Source URL: https://www.ashcroftbc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class AshcroftScraper(BCMunicipalScraper):
    """Scraper for Ashcroft council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
