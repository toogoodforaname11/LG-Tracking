"""Custom scraper for Smithers.

Source URL: https://www.smithers.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SmithersScraper(BCMunicipalScraper):
    """Scraper for Smithers council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
