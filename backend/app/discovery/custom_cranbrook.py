"""Custom scraper for Cranbrook.

Source URL: https://www.cranbrook.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class CranbrookScraper(BCMunicipalScraper):
    """Scraper for Cranbrook council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
