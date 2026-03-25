"""Custom scraper for Alert Bay.

Source URL: https://www.alertbay.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class AlertBayScraper(BCMunicipalScraper):
    """Scraper for Alert Bay council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
