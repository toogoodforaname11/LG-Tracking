"""Custom scraper for Spallumcheen.

Source URL: https://www.spallumcheen.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SpallumcheenScraper(BCMunicipalScraper):
    """Scraper for Spallumcheen council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
