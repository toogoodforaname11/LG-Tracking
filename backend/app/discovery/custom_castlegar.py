"""Custom scraper for City of Castlegar.

Source URL: https://www.castlegar.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class CastlegarScraper(BCMunicipalScraper):
    """Scraper for City of Castlegar council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
