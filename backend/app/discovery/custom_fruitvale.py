"""Custom scraper for Fruitvale.

Source URL: https://www.fruitvale.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class FruitvaleScraper(BCMunicipalScraper):
    """Scraper for Fruitvale council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
