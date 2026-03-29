"""Custom scraper for New Denver.

Source URL: https://www.newdenver.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class NewDenverScraper(BCMunicipalScraper):
    """Scraper for New Denver council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
