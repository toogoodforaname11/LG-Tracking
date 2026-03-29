"""Custom scraper for Radium Hot Springs.

Source URL: https://www.radiumhotsprings.com/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class RadiumHotSpringsScraper(BCMunicipalScraper):
    """Scraper for Radium Hot Springs council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
