"""Custom scraper for City of Fernie.

Source URL: https://www.fernie.ca/council-meetings
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class FernieScraper(BCMunicipalScraper):
    """Scraper for City of Fernie council meetings."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council-meetings", "council meetings",
    ]
