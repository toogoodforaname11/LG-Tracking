"""Custom scraper for Anmore.

Source URL: https://anmore.com/village-hall/mayor-council/agendas-minutes/
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class AnmoreScraper(BCMunicipalScraper):
    """Scraper for Anmore council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "agendas-minutes",
    ]
