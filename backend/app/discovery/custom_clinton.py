"""Custom scraper for Clinton.

Source URL: https://www.clintonbc.com/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class ClintonScraper(BCMunicipalScraper):
    """Scraper for Clinton council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
