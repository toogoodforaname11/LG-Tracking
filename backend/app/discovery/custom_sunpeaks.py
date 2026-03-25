"""Custom scraper for Sun Peaks.

Source URL: https://www.sunpeaksmunicipality.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class SunPeaksScraper(BCMunicipalScraper):
    """Scraper for Sun Peaks council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
