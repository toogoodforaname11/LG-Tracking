"""Custom scraper for Stewart.

Source URL: https://www.stewartbc.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class StewartScraper(BCMunicipalScraper):
    """Scraper for Stewart council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
