"""Custom scraper for Lytton.

Source URL: https://www.lytton.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class LyttonScraper(BCMunicipalScraper):
    """Scraper for Lytton council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
