"""Custom scraper for Canal Flats.

Source URL: https://www.canalflats.com/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class CanalFlatsScraper(BCMunicipalScraper):
    """Scraper for Canal Flats council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
