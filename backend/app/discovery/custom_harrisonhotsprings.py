"""Custom scraper for Harrison Hot Springs.

Source URL: https://www.harrisonhotsprings.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class HarrisonHotSpringsScraper(BCMunicipalScraper):
    """Scraper for Harrison Hot Springs council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
