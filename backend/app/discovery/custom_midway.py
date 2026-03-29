"""Custom scraper for Midway.

Source URL: https://www.midwaybc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class MidwayScraper(BCMunicipalScraper):
    """Scraper for Midway council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
