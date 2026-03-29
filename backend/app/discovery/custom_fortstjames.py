"""Custom scraper for Fort St. James.

Source URL: https://www.fortstjames.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class FortStJamesScraper(BCMunicipalScraper):
    """Scraper for Fort St. James council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
