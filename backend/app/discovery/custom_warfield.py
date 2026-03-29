"""Custom scraper for Warfield.

Source URL: https://www.warfield.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class WarfieldScraper(BCMunicipalScraper):
    """Scraper for Warfield council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
