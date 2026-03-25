"""Custom scraper for Hudson's Hope.

Source URL: https://www.hudsonshope.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class HudsonsHopeScraper(BCMunicipalScraper):
    """Scraper for Hudson's Hope council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council",
    ]
