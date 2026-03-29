"""Custom scraper for Lumby.

Source URL: https://www.lumby.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class LumbyScraper(BCMunicipalScraper):
    """Scraper for Lumby council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
