"""Custom scraper for City of Terrace.

Source URL: https://www.terrace.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class TerraceScraper(BCMunicipalScraper):
    """Scraper for City of Terrace council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
