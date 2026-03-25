"""Custom scraper for Kitimat.

Source URL: https://www.kitimat.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class KitimatScraper(BCMunicipalScraper):
    """Scraper for Kitimat council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
