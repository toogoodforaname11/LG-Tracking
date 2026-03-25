"""Custom scraper for Ainsworth Hot Springs.

Source URL: https://www.rdkb.com
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class AinsworthHotSpringsScraper(BCMunicipalScraper):
    """Scraper for Ainsworth Hot Springs council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "rdkb",
    ]
