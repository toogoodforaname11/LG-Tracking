"""Custom scraper for City of Prince Rupert.

Source URL: https://www.princerupert.ca/council-meetings
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PrinceRupertScraper(BCMunicipalScraper):
    """Scraper for City of Prince Rupert council meetings."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council-meetings", "council meetings",
    ]
