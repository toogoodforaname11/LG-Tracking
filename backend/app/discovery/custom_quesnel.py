"""Custom scraper for City of Quesnel.

Source URL: https://www.quesnel.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class QuesnelScraper(BCMunicipalScraper):
    """Scraper for City of Quesnel council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
