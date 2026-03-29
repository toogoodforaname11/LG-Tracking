"""Custom scraper for Nakusp.

Source URL: https://www.nakusp.com/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class NakuspScraper(BCMunicipalScraper):
    """Scraper for Nakusp council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
