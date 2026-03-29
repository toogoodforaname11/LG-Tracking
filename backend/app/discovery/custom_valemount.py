"""Custom scraper for Valemount.

Source URL: https://www.valemount.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ValemountScraper(BCMunicipalScraper):
    """Scraper for Valemount council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
