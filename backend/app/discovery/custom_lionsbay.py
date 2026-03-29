"""Custom scraper for Lions Bay.

Source URL: https://www.lionsbay.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class LionsBayScraper(BCMunicipalScraper):
    """Scraper for Lions Bay council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
