"""Custom scraper for Fort Nelson.

Source URL: https://www.fortnelson.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class FortNelsonScraper(BCMunicipalScraper):
    """Scraper for Fort Nelson council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
