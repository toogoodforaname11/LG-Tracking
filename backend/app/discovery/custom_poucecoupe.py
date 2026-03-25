"""Custom scraper for Pouce Coupe.

Source URL: https://poucecoupe.ca/government/administration/council-meetings/
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class PouceCoupeScraper(BCMunicipalScraper):
    """Scraper for Pouce Coupe council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
