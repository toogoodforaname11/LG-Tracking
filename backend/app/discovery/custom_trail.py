"""Custom scraper for City of Trail.

Source URL: https://www.trail.ca/council
"""

from app.discovery.custom_bc_municipal import BCMunicipalScraper


class TrailScraper(BCMunicipalScraper):
    """Scraper for City of Trail council agendas and minutes."""

    _subpage_keywords = [
        *BCMunicipalScraper._subpage_keywords,
        "council", "bylaws",
    ]
