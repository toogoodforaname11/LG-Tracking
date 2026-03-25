"""Custom scraper for Gold River.

Source URL: https://www.goldriver.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class GoldRiverScraper(BCMunicipalScraper):
    """Scraper for Gold River council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
