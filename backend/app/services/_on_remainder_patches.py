"""Auto-generated from docs/alberta-probe-report.json by
``scripts/apply_alberta_probe.py``. Do not edit by hand —
re-run the script if the probe report changes."""

# Strings reference Platform / SourceType / ScrapeStatus enum values
# defined in app.models.municipality. seed_registry resolves them at
# import time so this module stays free of model-side dependencies.

REMAINDER_PATCHES: dict = {
    'Ajax': {
        "website_url": 'https://www.ajax.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@yourvoice4ajax',
                "label": 'Ajax YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Alberton': {
        "website_url": 'https://www.alberton.ca/',
        "sources": [
        ],
    },
    'Algonquin Highlands': {
        "website_url": 'https://www.algonquinhighlands.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://algonquinhighlands.civicweb.net',
                "label": 'Algonquin Highlands Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townshipofalgonquinhighlan7249',
                "label": 'Algonquin Highlands YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Amaranth': {
        "website_url": 'https://www.amaranth.ca/',
        "sources": [
        ],
    },
    'Amherstburg': {
        "website_url": 'https://www.amherstburg.ca/',
        "sources": [
        ],
    },
    'Armour': {
        "website_url": 'https://www.armour.ca/',
        "sources": [
        ],
    },
    'Armstrong': {
        "website_url": 'https://www.armstrong.ca/',
        "sources": [
        ],
    },
    'Assiginack': {
        "website_url": 'https://www.assiginack.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townshipofassiginack7612',
                "label": 'Assiginack YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Atikokan': {
        "website_url": 'https://www.atikokan.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://atikokan.civicweb.net',
                "label": 'Atikokan Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Augusta': {
        "website_url": 'https://www.augusta.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-augusta.escribemeetings.com',
                "label": 'Augusta Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townshipofaugusta',
                "label": 'Augusta YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Aurora': {
        "website_url": 'https://www.aurora.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-auroraon.escribemeetings.com?FillWidth=1',
                "label": 'Aurora Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TownofAurora',
                "label": 'Aurora YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Aylmer': {
        "website_url": 'https://www.aylmer.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://aylmer.civicweb.net',
                "label": 'Aylmer Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TownOfAylmer',
                "label": 'Aylmer YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Baldwin': {
        "website_url": 'https://www.baldwin.ca/',
        "sources": [
        ],
    },
    'Bancroft': {
        "website_url": 'https://www.bancroft.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'http://bancroft.civicweb.net/portal/default.aspx',
                "label": 'Bancroft Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCjtHKqR5R-whq9aKcQJVllw',
                "label": 'Bancroft YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Barrie': {
        "website_url": 'https://www.barrie.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/citybarrie',
                "label": 'Barrie YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Belleville': {
        "website_url": 'https://www.belleville.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://citybellevilleon.civicweb.net',
                "label": 'Belleville Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'http://www.youtube.com/user/BellevilleCityHall',
                "label": 'Belleville YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Blind River': {
        "website_url": 'https://www.blindriver.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-blindriver.escribemeetings.com',
                "label": 'Blind River Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCOINr7KiJr0sF1t9CjTH68A',
                "label": 'Blind River YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Bluewater': {
        "website_url": 'https://www.bluewater.ca/',
        "sources": [
        ],
    },
    'Bracebridge': {
        "website_url": 'https://www.bracebridge.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://bracebridge.civicweb.net/document/16435',
                "label": 'Bracebridge Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Brant': {
        "website_url": 'https://www.brant.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-brant.escribemeetings.com',
                "label": 'Brant Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCR8UjmTndN2iMzySQgiepkA',
                "label": 'Brant YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Brantford': {
        "website_url": 'https://www.brantford.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CityOfBrantford',
                "label": 'Brantford YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Brighton': {
        "website_url": 'https://www.brighton.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://brighton.civicweb.net',
                "label": 'Brighton Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Brockton': {
        "website_url": 'https://www.brockton.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC_w2XYSUIDY4IijNYD6iA6Q',
                "label": 'Brockton YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Burlington': {
        "website_url": 'https://www.burlington.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CityofBurlington',
                "label": 'Burlington YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Caledon': {
        "website_url": 'https://www.caledon.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofcaledon',
                "label": 'Caledon YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Cambridge': {
        "website_url": 'https://www.cambridge.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CityOfCambridgeOn',
                "label": 'Cambridge YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Carling': {
        "website_url": 'https://www.carling.ca/',
        "sources": [
        ],
    },
    'Carlow/Mayo': {
        "website_url": 'https://www.carlowmayo.ca/',
        "sources": [
        ],
    },
    'Casey': {
        "website_url": 'https://www.casey.ca/',
        "sources": [
        ],
    },
    'Casselman': {
        "website_url": 'https://www.casselman.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-casselman.escribemeetings.com',
                "label": 'Casselman Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC1kN30SRMDqRpLyGwd064Zw',
                "label": 'Casselman YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Centre Wellington': {
        "website_url": 'https://www.centrewellington.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://centrewellington.civicweb.net',
                "label": 'Centre Wellington Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Champlain': {
        "website_url": 'https://www.champlain.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-champlain.escribemeetings.com',
                "label": 'Champlain Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC6Xram_3gD39_SG-gI8nB_g',
                "label": 'Champlain YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Chapleau': {
        "website_url": 'https://www.chapleau.ca/',
        "sources": [
        ],
    },
    'Chatham-Kent': {
        "website_url": 'https://www.chathamkent.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@themunicipalityofchatham-k7076',
                "label": 'Chatham-Kent YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Chatsworth': {
        "website_url": 'https://www.chatsworth.ca/',
        "sources": [
        ],
    },
    'Chisholm': {
        "website_url": 'https://www.chisholm.ca/',
        "sources": [
        ],
    },
    'Clearview': {
        "website_url": 'https://www.clearview.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCNlY6-QMWoNRWWt3eK3280w',
                "label": 'Clearview YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Cobalt': {
        "website_url": 'https://www.cobalt.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCkb76eXX-iNnEcHHLbobMYw',
                "label": 'Cobalt YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Cobourg': {
        "website_url": 'https://www.cobourg.ca/',
        "sources": [
        ],
    },
    'Cochrane': {
        "website_url": 'https://www.cochrane.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://cochraneab.civicweb.net/portal/',
                "label": 'Cochrane Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Collingwood': {
        "website_url": 'https://www.collingwood.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://collingwood.civicweb.net/filepro/documents/120312/',
                "label": 'Collingwood Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://bm-public-collingwood.escribemeetings.com',
                "label": 'Collingwood Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofcollingwood-municipa954',
                "label": 'Collingwood YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Cornwall': {
        "website_url": 'https://www.cornwall.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-cornwall.escribemeetings.com',
                "label": 'Cornwall Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Cramahe': {
        "website_url": 'https://www.cramahe.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-cramahe.escribemeetings.com',
                "label": 'Cramahe Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Dawson': {
        "website_url": 'https://www.cityofdawson.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-cityofdawson.escribemeetings.com',
                "label": 'Dawson Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/DawsonCityKlondike',
                "label": 'Dawson YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Deep River': {
        "website_url": 'https://www.deepriver.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://deepriver.civicweb.net',
                "label": 'Deep River Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Deseronto': {
        "website_url": 'https://www.deseronto.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://deseronto.civicweb.net/portal/',
                "label": 'Deseronto Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Dryden': {
        "website_url": 'https://www.dryden.ca/',
        "sources": [
        ],
    },
    'Durham Region': {
        "website_url": 'https://www.durham-region.ca/',
        "sources": [
        ],
    },
    'East Gwillimbury': {
        "website_url": 'https://www.eastgwillimbury.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://eastgwillimbury.civicweb.net',
                "label": 'East Gwillimbury Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/TownEastGwillimbury',
                "label": 'East Gwillimbury YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'East Hawkesbury': {
        "website_url": 'https://www.easthawkesbury.ca/',
        "sources": [
        ],
    },
    'Elgin County': {
        "website_url": 'https://www.elgincounty.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-elgincounty.escribemeetings.com',
                "label": 'Elgin County Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@ElginCountyAdmin',
                "label": 'Elgin County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Elliot Lake': {
        "website_url": 'https://www.elliotlake.ca/',
        "sources": [
        ],
    },
    'Emo': {
        "website_url": 'https://emo.ca/',
        "sources": [
        ],
    },
    'Englehart': {
        "website_url": 'https://www.englehart.ca/',
        "sources": [
        ],
    },
    'Enniskillen': {
        "website_url": 'https://www.enniskillen.ca/',
        "sources": [
        ],
    },
    'Erin': {
        "website_url": 'https://www.erin.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-erin.escribemeetings.com',
                "label": 'Erin Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC-jZVfNa-3RiUj3uLy-RAvA',
                "label": 'Erin YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Espanola': {
        "website_url": 'https://www.espanola.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-espanola.escribemeetings.com?FillWidth=1',
                "label": 'Espanola Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/TownofEspanola',
                "label": 'Espanola YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Essex': {
        "website_url": 'https://www.essex.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/EssexOntario',
                "label": 'Essex YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Essex County': {
        "website_url": 'https://www.essex.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/EssexOntario',
                "label": 'Essex County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Faraday': {
        "website_url": 'https://www.faraday.ca/',
        "sources": [
        ],
    },
    'Fort Erie': {
        "website_url": 'https://www.forterie.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-forterie.escribemeetings.com',
                "label": 'Fort Erie Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/c/townofforterie',
                "label": 'Fort Erie YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Fort Frances': {
        "website_url": 'https://www.fortfrances.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://fortfrances.civicweb.net',
                "label": 'Fort Frances Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@FortFrancesON',
                "label": 'Fort Frances YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'French River': {
        "website_url": 'https://www.frenchriver.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://frenchriver.civicweb.net',
                "label": 'French River Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'http://www.youtube.com/user/FrenchRiverON',
                "label": 'French River YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Frontenac County': {
        "website_url": 'https://www.frontenaccounty.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@frontenaccounty',
                "label": 'Frontenac County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Frontenac Islands': {
        "website_url": 'https://www.frontenacislands.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://frontenac.civicweb.net',
                "label": 'Frontenac Islands Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Gananoque': {
        "website_url": 'https://www.gananoque.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/townofgananoque',
                "label": 'Gananoque YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Georgian Bay': {
        "website_url": 'https://www.georgianbay.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCWH8cJErRppkMklebKtIyzg',
                "label": 'Georgian Bay YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Georgian Bluffs': {
        "website_url": 'https://www.georgianbluffs.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-georgianbluffs.escribemeetings.com',
                "label": 'Georgian Bluffs Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@georgianbluffscouncil',
                "label": 'Georgian Bluffs YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Georgina': {
        "website_url": 'https://www.georgina.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-georgina.escribemeetings.com',
                "label": 'Georgina Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCTOMe6hNkts6kUc0yqGff1A',
                "label": 'Georgina YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Goderich': {
        "website_url": 'https://www.goderich.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-goderich.escribemeetings.com',
                "label": 'Goderich Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Gore Bay': {
        "website_url": 'https://www.gorebay.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://gorebay.civicweb.net',
                "label": 'Gore Bay Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Grand Valley': {
        "website_url": 'https://www.townofgrandvalley.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-townofgrandvalley.escribemeetings.com',
                "label": 'Grand Valley Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Gravenhurst': {
        "website_url": 'https://www.gravenhurst.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://gravenhurst.civicweb.net/document/102971',
                "label": 'Gravenhurst Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCIyDimlIhouNx1QQo7bkDPw',
                "label": 'Gravenhurst YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Greater Napanee': {
        "website_url": 'https://greaternapanee.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://greaternapanee.civicweb.net',
                "label": 'Greater Napanee Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofgreaternapanee1994',
                "label": 'Greater Napanee YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Greater Sudbury': {
        "website_url": 'https://www.greatersudbury.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-greatersudbury.escribemeetings.com',
                "label": 'Greater Sudbury Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC2Xy4HKAOBcxCcSpkBLvh3w',
                "label": 'Greater Sudbury YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Greenstone': {
        "website_url": 'https://www.greenstone.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://greenstone.civicweb.net',
                "label": 'Greenstone Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCc8dnfK7Gm_K5wP2OPfj39w',
                "label": 'Greenstone YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Grey County': {
        "website_url": 'https://www.greycounty.ca/',
        "sources": [
        ],
    },
    'Grimsby': {
        "website_url": 'https://www.grimsby.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-grimsby.escribemeetings.com',
                "label": 'Grimsby Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofgrimsbyontario',
                "label": 'Grimsby YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Guelph': {
        "website_url": 'https://www.guelph.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-guelph.escribemeetings.com',
                "label": 'Guelph Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://youtube.com/user/cityofguelph',
                "label": 'Guelph YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Haldimand County': {
        "website_url": 'https://www.haldimandcounty.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/haldimandcounty',
                "label": 'Haldimand County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Haliburton County': {
        "website_url": 'https://www.haliburtoncounty.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://haliburton.civicweb.net',
                "label": 'Haliburton County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCD5Nnj_j7WcU-OkketJpqqw',
                "label": 'Haliburton County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Halton Hills': {
        "website_url": 'https://www.haltonhills.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/TownHaltonHills',
                "label": 'Halton Hills YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Hamilton Township': {
        "website_url": 'https://www.hamiltontownship.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://hamilton.civicweb.net/portal/',
                "label": 'Hamilton Township Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@HamiltonTownshipOntario',
                "label": 'Hamilton Township YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Hanover': {
        "website_url": 'https://www.hanover.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-hanover.escribemeetings.com',
                "label": 'Hanover Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Harley': {
        "website_url": 'https://harley.ca/',
        "sources": [
        ],
    },
    'Harris': {
        "website_url": 'https://www.harris.ca/',
        "sources": [
        ],
    },
    'Hastings County': {
        "website_url": 'https://www.hastings.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://hastingscounty.civicweb.net',
                "label": 'Hastings County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Hawkesbury': {
        "website_url": 'https://www.hawkesbury.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-hawkesbury.escribemeetings.com',
                "label": 'Hawkesbury Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@HawkesburyON',
                "label": 'Hawkesbury YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Hearst': {
        "website_url": 'https://www.hearst.ca/',
        "sources": [
        ],
    },
    'Highlands East': {
        "website_url": 'https://www.highlandseast.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://highlandseast.civicweb.net',
                "label": 'Highlands East Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCyV-7q-lVSv2MswwDI3j8Sw',
                "label": 'Highlands East YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Howick': {
        "website_url": 'https://www.howick.ca/',
        "sources": [
        ],
    },
    'Hudson': {
        "website_url": 'https://www.hudson.ca/',
        "sources": [
        ],
    },
    'Huntsville': {
        "website_url": 'https://www.huntsville.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://huntsvilleon.civicweb.net/document/95452/2025%20Q2%20Forecast.pdf?handle=297BEB93C7E2495C9299D0D51DA72B80',
                "label": 'Huntsville Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Huron County': {
        "website_url": 'https://www.huroncounty.ca/',
        "sources": [
            {
                "platform": "Platform.GRANICUS",
                "source_type": "SourceType.AGENDA",
                "url": 'https://huroncounty.ca.granicus.com/ViewPublisher.php?view_id=1',
                "label": 'Huron County Granicus Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@CouncilCommitteeBoardMeetings',
                "label": 'Huron County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Ignace': {
        "website_url": 'https://www.ignace.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://ignace.civicweb.net',
                "label": 'Ignace Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Ingersoll': {
        "website_url": 'https://www.ingersoll.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://ingersoll.civicweb.net',
                "label": 'Ingersoll Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofingersoll960',
                "label": 'Ingersoll YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Innisfil': {
        "website_url": 'https://www.innisfil.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://innisfil.civicweb.net',
                "label": 'Innisfil Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCvnGbVPjftQjT8PmI2_2jpw',
                "label": 'Innisfil YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Jocelyn': {
        "website_url": 'https://www.jocelyn.ca/',
        "sources": [
        ],
    },
    'Johnson': {
        "website_url": 'https://www.johnson.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@belairdirect.assurance',
                "label": 'Johnson YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Kapuskasing': {
        "website_url": 'https://www.kapuskasing.ca/',
        "sources": [
        ],
    },
    'Kawartha Lakes': {
        "website_url": 'https://www.kawarthalakes.ca/',
        "sources": [
        ],
    },
    'Kearney': {
        "website_url": 'https://www.townofkearney.ca/',
        "sources": [
        ],
    },
    'Kerns': {
        "website_url": 'https://www.kerns.ca/',
        "sources": [
        ],
    },
    'Killarney': {
        "website_url": 'https://www.killarney.ca/',
        "sources": [
        ],
    },
    'Kincardine': {
        "website_url": 'https://www.kincardine.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-kincardine.escribemeetings.com',
                "label": 'Kincardine Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@MunicipalityofKincardine',
                "label": 'Kincardine YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'King': {
        "website_url": 'https://www.king.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://king.civicweb.net',
                "label": 'King Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-king.escribemeetings.com',
                "label": 'King Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@kingtownship1354',
                "label": 'King YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Kingston': {
        "website_url": 'https://www.cityofkingston.ca/',
        "sources": [
        ],
    },
    'Kingsville': {
        "website_url": 'https://www.kingsville.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCbVKxVodrJTjYU-4e0qJV6A',
                "label": 'Kingsville YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Kirkland Lake': {
        "website_url": 'https://www.kirklandlake.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://kirklandlake.civicweb.net/document/26516/2025-ADM-008.pdf?handle=B84BD840D71B4166BADB2FE7842171BA',
                "label": 'Kirkland Lake Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'LaSalle': {
        "website_url": 'https://www.lasalle.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC6x5UyIhV1zSHkDTV6TCl5g',
                "label": 'LaSalle YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Lake of the Woods': {
        "website_url": 'https://www.lakeofthewoods.ca/',
        "sources": [
        ],
    },
    'Lakeshore': {
        "website_url": 'https://www.lakeshore.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@lakeshoreon',
                "label": 'Lakeshore YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Lambton County': {
        "website_url": 'https://www.lambtoncounty.ca/',
        "sources": [
        ],
    },
    'Lanark Highlands': {
        "website_url": 'https://www.lanarkhighlands.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-lanarkhighlands.escribemeetings.com',
                "label": 'Lanark Highlands Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@LanarkHighlands_Council',
                "label": 'Lanark Highlands YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Larder Lake': {
        "website_url": 'https://www.larderlake.ca/',
        "sources": [
        ],
    },
    'Latchford': {
        "website_url": 'https://www.latchford.ca/',
        "sources": [
        ],
    },
    'Leamington': {
        "website_url": 'https://www.leamington.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/TownofLeamington',
                "label": 'Leamington YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Limerick': {
        "website_url": 'https://www.limerick.ca/',
        "sources": [
        ],
    },
    'Lincoln': {
        "website_url": 'https://www.lincoln.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCrAPAz-HYUv2-tWIg48LWAQ',
                "label": 'Lincoln YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Loyalist': {
        "website_url": 'https://www.loyalist.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://lennoxandaddington.civicweb.net',
                "label": 'Loyalist Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCkFOTqE3meHH8-bexPoayAg',
                "label": 'Loyalist YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Madawaska Valley': {
        "website_url": 'https://www.madawaskavalley.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://madawaskavalley.civicweb.net',
                "label": 'Madawaska Valley Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@madawaskavalley8332',
                "label": 'Madawaska Valley YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Madoc': {
        "website_url": 'https://www.madoc.ca/',
        "sources": [
        ],
    },
    'Malahide': {
        "website_url": 'https://www.malahide.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC2WWxGHYoaNBixWD8viFlGw',
                "label": 'Malahide YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Manitouwadge': {
        "website_url": 'https://www.manitouwadge.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://manitouwadge.civicweb.net',
                "label": 'Manitouwadge Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@thecorporationofthetownshi8774',
                "label": 'Manitouwadge YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Mapleton': {
        "website_url": 'https://www.mapleton.ca/',
        "sources": [
        ],
    },
    'Marathon': {
        "website_url": 'https://www.marathon.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCrwNj88Szza94mOuEw6Jjrg',
                "label": 'Marathon YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Mattawa': {
        "website_url": 'https://www.mattawa.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofmattawa1508',
                "label": 'Mattawa YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Mattawan': {
        "website_url": 'https://www.mattawan.ca/',
        "sources": [
        ],
    },
    'McDougall': {
        "website_url": 'https://www.mcdougall.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-mcdougall.escribemeetings.com?fillWidth=1',
                "label": 'McDougall Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@municipailityofmcdougall9125',
                "label": 'McDougall YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'McGarry': {
        "website_url": 'https://www.mcgarry.ca/',
        "sources": [
        ],
    },
    'McKellar': {
        "website_url": 'https://www.mckellar.ca/',
        "sources": [
        ],
    },
    'Meaford': {
        "website_url": 'https://www.meaford.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://meaford.civicweb.net',
                "label": 'Meaford Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Middlesex County': {
        "website_url": 'https://www.middlesex.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-middlesexcounty.escribemeetings.com',
                "label": 'Middlesex County Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCSlRBMaSUbravUhLTjSKc9A',
                "label": 'Middlesex County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Midland': {
        "website_url": 'https://www.midland.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCZyTTENGQfUuN7M6vwFjLFw',
                "label": 'Midland YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Milton': {
        "website_url": 'https://www.milton.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCD_KE5vUIJDmKNpcsQRnAdg',
                "label": 'Milton YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Mississippi Mills': {
        "website_url": 'https://www.mississippimills.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-mississippimills.escribemeetings.com',
                "label": 'Mississippi Mills Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'http://www.youtube.com/@GetToKnowMississippiMills',
                "label": 'Mississippi Mills YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Mono': {
        "website_url": 'https://www.townofmono.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://mono.civicweb.net',
                "label": 'Mono Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Moonbeam': {
        "website_url": 'https://www.moonbeam.ca/',
        "sources": [
        ],
    },
    'Mulmur': {
        "website_url": 'https://www.mulmur.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@mulmurtownship825',
                "label": 'Mulmur YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Muskoka': {
        "website_url": 'https://www.muskoka.ca/',
        "sources": [
        ],
    },
    'Newbury': {
        "website_url": 'https://www.newbury.ca/',
        "sources": [
        ],
    },
    'Newmarket': {
        "website_url": 'https://www.newmarket.ca/',
        "sources": [
        ],
    },
    'Niagara Falls': {
        "website_url": 'https://www.niagarafalls.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://niagarafalls.civicweb.net/portal/members.aspx?id=10',
                "label": 'Niagara Falls Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/c/niagarafallsca',
                "label": 'Niagara Falls YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Niagara Region': {
        "website_url": 'https://www.niagararegion.ca/',
        "sources": [
        ],
    },
    'Norfolk County': {
        "website_url": 'https://www.norfolkcounty.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@norfolkcounty1073',
                "label": 'Norfolk County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'North Bay': {
        "website_url": 'https://www.northbay.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-northbay.escribemeetings.com',
                "label": 'North Bay Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/c/thecityofnorthbay',
                "label": 'North Bay YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'North Frontenac': {
        "website_url": 'https://www.northfrontenac.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://northfrontenac.civicweb.net/filepro/documents/',
                "label": 'North Frontenac Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@northfrontenac',
                "label": 'North Frontenac YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'North Glengarry': {
        "website_url": 'https://www.northglengarry.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCyHgS_xNDqjpiY9sMdVRL3A',
                "label": 'North Glengarry YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'North Huron': {
        "website_url": 'https://www.northhuron.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/TwpofNorthHuron',
                "label": 'North Huron YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'North Perth': {
        "website_url": 'https://www.northperth.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@NorthPerthOntario',
                "label": 'North Perth YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Northumberland County': {
        "website_url": 'https://northumberlandcounty.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CountyNorthumberland',
                "label": 'Northumberland County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Norwich': {
        "website_url": 'https://www.norwich.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://norwich.civicweb.net/filepro/documents',
                "label": 'Norwich Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Oakville': {
        "website_url": 'https://www.oakville.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-oakville.escribemeetings.com',
                "label": 'Oakville Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofoakville',
                "label": 'Oakville YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Oil Springs': {
        "website_url": 'https://www.oilsprings.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC7GjNf6MIEKx6Hp_fMdIZBA',
                "label": 'Oil Springs YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Orangeville': {
        "website_url": 'https://www.orangeville.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-orangeville.escribemeetings.com//?FillWidth=1&amp;wmode=transparent',
                "label": 'Orangeville Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCBHXROPbMg75y2ZLV5IkhFg',
                "label": 'Orangeville YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Orillia': {
        "website_url": 'https://www.orillia.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://orillia.civicweb.net',
                "label": 'Orillia Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TheCityofOrillia',
                "label": 'Orillia YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Oshawa': {
        "website_url": 'https://www.oshawa.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-oshawa.escribemeetings.com',
                "label": 'Oshawa Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/oshawacity',
                "label": 'Oshawa YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Oxford County': {
        "website_url": 'https://www.oxfordcounty.ca/',
        "sources": [
        ],
    },
    'Parry Sound': {
        "website_url": 'https://www.parrysound.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofparrysound',
                "label": 'Parry Sound YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Peel Region': {
        "website_url": 'https://www.peelregion.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/theregionofpeel',
                "label": 'Peel Region YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Pelham': {
        "website_url": 'https://www.pelham.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/TownOfPelham',
                "label": 'Pelham YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Pembroke': {
        "website_url": 'https://www.pembroke.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TheCityofPembroke',
                "label": 'Pembroke YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Perth': {
        "website_url": 'https://www.perth.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://perth.civicweb.net',
                "label": 'Perth Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofperth9960',
                "label": 'Perth YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Perth County': {
        "website_url": 'https://www.perthcounty.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://perthcounty.civicweb.net',
                "label": 'Perth County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@Perth_County',
                "label": 'Perth County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Perth East': {
        "website_url": 'https://www.pertheast.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townshipofpertheast4753',
                "label": 'Perth East YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Perth South': {
        "website_url": 'https://www.perthsouth.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://perthsouth.civicweb.net',
                "label": 'Perth South Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Petawawa': {
        "website_url": 'https://www.petawawa.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'http://www.youtube.com/channel/UCnzw2dCuHIZj10TmySwThfw',
                "label": 'Petawawa YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Peterborough': {
        "website_url": 'https://www.peterborough.ca/',
        "sources": [
        ],
    },
    'Peterborough County': {
        "website_url": 'https://www.peterborough.ca/',
        "sources": [
        ],
    },
    'Pickering': {
        "website_url": 'https://www.pickering.ca/',
        "sources": [
        ],
    },
    'Port Hope': {
        "website_url": 'https://www.porthope.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-porthope.escribemeetings.com',
                "label": 'Port Hope Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/MunicipalityPortHope',
                "label": 'Port Hope YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Prescott': {
        "website_url": 'https://www.prescott.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-prescott.escribemeetings.com',
                "label": 'Prescott Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCligB93IqnjmXN8mQ7XOENA',
                "label": 'Prescott YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Prince Edward County': {
        "website_url": 'https://www.princeedwardcounty.ca/',
        "sources": [
        ],
    },
    'Quinte West': {
        "website_url": 'https://www.cityofquintewest.ca/',
        "sources": [
        ],
    },
    'Red Lake': {
        "website_url": 'https://www.redlake.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC4-hQMw0uWcfb0rk8eCnMTw',
                "label": 'Red Lake YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Renfrew': {
        "website_url": 'https://www.renfrew.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-renfrew.escribemeetings.com',
                "label": 'Renfrew Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofrenfrew-councilpage1657',
                "label": 'Renfrew YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Renfrew County': {
        "website_url": 'https://www.renfrewcounty.ca/',
        "sources": [
        ],
    },
    'Richmond Hill': {
        "website_url": 'https://www.richmondhill.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/c/CityRichmondHill',
                "label": 'Richmond Hill YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Russell': {
        "website_url": 'https://www.russell.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://russell.civicweb.net/filepro/documents/42032',
                "label": 'Russell Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCc4MO5tif44j0_8cIVEi_fg',
                "label": 'Russell YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Ryerson': {
        "website_url": 'https://www.ryerson.ca/',
        "sources": [
        ],
    },
    'SDG Counties': {
        "website_url": 'https://www.sdgcounties.ca/',
        "sources": [
        ],
    },
    'Sarnia': {
        "website_url": 'https://www.sarnia.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://sarnia.civicweb.net',
                "label": 'Sarnia Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC0OYjybqDhtpncskd31LcuQ',
                "label": 'Sarnia YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Saugeen Shores': {
        "website_url": 'https://www.saugeenshores.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-saugeenshores.escribemeetings.com',
                "label": 'Saugeen Shores Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TownOfSaugeenShores',
                "label": 'Saugeen Shores YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Sault Ste. Marie': {
        "website_url": 'https://www.saultstemarie.ca/',
        "sources": [
        ],
    },
    'Schreiber': {
        "website_url": 'https://www.schreiber.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://schreiber.civicweb.net',
                "label": 'Schreiber Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCgj9znKXX_Ge-LZc3bdAxew',
                "label": 'Schreiber YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Seguin': {
        "website_url": 'https://www.seguin.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@SeguinTownshipOfficial',
                "label": 'Seguin YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Selwyn': {
        "website_url": 'https://www.selwyn.ca/',
        "sources": [
        ],
    },
    'Severn': {
        "website_url": 'https://www.severn.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://severn.civicweb.net',
                "label": 'Severn Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCzhcoASavyb3nVr4jxzx8vA',
                "label": 'Severn YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Shelburne': {
        "website_url": 'https://www.shelburne.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCsar-MwF8CXrgPbe2EVxh-w',
                "label": 'Shelburne YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Simcoe County': {
        "website_url": 'https://www.simcoe.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://simcoe.civicweb.net',
                "label": 'Simcoe County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CountyofSimcoe',
                "label": 'Simcoe County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Sioux Lookout': {
        "website_url": 'https://www.siouxlookout.ca/',
        "sources": [
            {
                "platform": "Platform.GRANICUS",
                "source_type": "SourceType.AGENDA",
                "url": 'https://siouxlookout.ca.granicus.com/ViewPublisher.php?view_id=1',
                "label": 'Sioux Lookout Granicus Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@siouxlookouton',
                "label": 'Sioux Lookout YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Smiths Falls': {
        "website_url": 'https://www.smithsfalls.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@corporationofthetownofsmit6358',
                "label": 'Smiths Falls YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Smooth Rock Falls': {
        "website_url": 'https://www.smoothrockfalls.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://townofsmoothrockfalls.civicweb.net',
                "label": 'Smooth Rock Falls Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCUA7YkNG4ji-02JhN-jB9pw',
                "label": 'Smooth Rock Falls YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'South Bruce': {
        "website_url": 'https://www.southbruce.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://southbruce.civicweb.net/filepro/documents/3261/',
                "label": 'South Bruce Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'South River': {
        "website_url": 'https://www.southriver.ca/',
        "sources": [
        ],
    },
    'South Stormont': {
        "website_url": 'https://www.southstormont.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-southstormont.escribemeetings.com',
                "label": 'South Stormont Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Southgate': {
        "website_url": 'https://www.southgate.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-southgate.escribemeetings.com',
                "label": 'Southgate Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@SouthgateTownship',
                "label": 'Southgate YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Southwest Middlesex': {
        "website_url": 'https://www.southwestmiddlesex.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-southwestmiddlesex.escribemeetings.com',
                "label": 'Southwest Middlesex Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC6oo98BZcAvuVMKLDx88l4A',
                "label": 'Southwest Middlesex YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Southwold': {
        "website_url": 'https://www.southwold.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCwADOaJYFVxPeXijzSiNvRw',
                "label": 'Southwold YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Spanish': {
        "website_url": 'https://www.townofspanish.ca/',
        "sources": [
        ],
    },
    'Springwater': {
        "website_url": 'https://www.springwater.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://springwater.civicweb.net',
                "label": 'Springwater Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCV7aqd68Gy98xmhDW9aWUNg',
                "label": 'Springwater YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'St. Charles': {
        "website_url": 'https://www.stcharles.ca/',
        "sources": [
        ],
    },
    'St. Marys': {
        "website_url": 'https://townofstmarys.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCzuUpFqxcEl8OG-dOYKteFQ',
                "label": 'St. Marys YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'St. Thomas': {
        "website_url": 'https://www.stthomas.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-stthomas.escribemeetings.com',
                "label": 'St. Thomas Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Stone Mills': {
        "website_url": 'https://www.stonemills.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://stonemills.civicweb.net/portal/#',
                "label": 'Stone Mills Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Stratford': {
        "website_url": 'https://www.stratford.ca/',
        "sources": [
        ],
    },
    'Strathroy-Caradoc': {
        "website_url": 'https://www.strathroy-caradoc.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-strathroy-caradoc.escribemeetings.com?wmode=transparent',
                "label": 'Strathroy-Caradoc Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@strathroy-caradoc',
                "label": 'Strathroy-Caradoc YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Sundridge': {
        "website_url": 'https://www.sundridge.ca/',
        "sources": [
        ],
    },
    'Tarbutt': {
        "website_url": 'https://www.tarbutt.ca/',
        "sources": [
        ],
    },
    'Tay': {
        "website_url": 'https://www.tay.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://tay.civicweb.net',
                "label": 'Tay Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TayTownshipON',
                "label": 'Tay YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Tecumseh': {
        "website_url": 'https://www.tecumseh.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@thetownoftecumseh',
                "label": 'Tecumseh YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Temiskaming Shores': {
        "website_url": 'https://www.temiskamingshores.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-temiskamingshores.escribemeetings.com',
                "label": 'Temiskaming Shores Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'The Blue Mountains': {
        "website_url": 'https://www.thebluemountains.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofbluemtns',
                "label": 'The Blue Mountains YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Thessalon': {
        "website_url": 'https://www.thessalon.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCjwjKtOYx2NIZnUUpOImXoA',
                "label": 'Thessalon YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Thunder Bay': {
        "website_url": 'https://www.thunderbay.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CityThunderBay',
                "label": 'Thunder Bay YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Timmins': {
        "website_url": 'https://www.timmins.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://timmins.civicweb.net',
                "label": 'Timmins Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/cotvideos',
                "label": 'Timmins YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Tiny': {
        "website_url": 'https://www.tiny.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://tiny.civicweb.net',
                "label": 'Tiny Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC7Oz4SOg6TRYX1TuJ716WQQ',
                "label": 'Tiny YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Trent Hills': {
        "website_url": 'https://www.trenthills.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://trenthills.civicweb.net',
                "label": 'Trent Hills Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCAw-tegkHB2-0WsfWt-BZYw',
                "label": 'Trent Hills YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Trent Lakes': {
        "website_url": 'https://www.trentlakes.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://trentlakes.civicweb.net/filepro/document/136256/___Special%20Council%20Meeting%20-%20Ratepayer%20-%2025%20Apr%2020.docx?handle=FB4F3D5ACDC64148BD09035CB03A9CD7',
                "label": 'Trent Lakes Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@municipalityoftrentlakes7985',
                "label": 'Trent Lakes YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Tweed': {
        "website_url": 'https://www.tweed.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-tweed.escribemeetings.com',
                "label": 'Tweed Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCqda93MaNm04mSeS4qPPusA',
                "label": 'Tweed YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Uxbridge': {
        "website_url": 'https://www.uxbridge.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-uxbridge.escribemeetings.com?',
                "label": 'Uxbridge Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC4XgxFEZg5c9WVC2gEHVMKA',
                "label": 'Uxbridge YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wainfleet': {
        "website_url": 'https://www.wainfleet.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCsRDFVYmXll4Es4IFnUI_ig',
                "label": 'Wainfleet YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Waterloo': {
        "website_url": 'https://www.waterloo.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@citywaterloo',
                "label": 'Waterloo YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Waterloo Region': {
        "website_url": 'https://www.waterloo-region.ca/',
        "sources": [
        ],
    },
    'Welland': {
        "website_url": 'https://www.welland.ca/',
        "sources": [
        ],
    },
    'Wellesley': {
        "website_url": 'https://www.wellesley.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TownshipofWellesley',
                "label": 'Wellesley YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wellington County': {
        "website_url": 'https://www.wellington.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-wellington.escribemeetings.com',
                "label": 'Wellington County Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CountyofWellington',
                "label": 'Wellington County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'West Lincoln': {
        "website_url": 'https://www.westlincoln.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCpXjnv5GCXU4F0bGYNwER8g',
                "label": 'West Lincoln YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'West Nipissing': {
        "website_url": 'https://www.westnipissing.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-westnipissingouest.escribemeetings.com',
                "label": 'West Nipissing Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCG6HWMXnA-RBiH-UdZVClHg',
                "label": 'West Nipissing YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Westport': {
        "website_url": 'https://www.villageofwestport.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://villageofwestport.civicweb.net',
                "label": 'Westport Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC-fs2y1g5jXLiioR0KdDgbA',
                "label": 'Westport YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Whitby': {
        "website_url": 'https://www.whitby.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-whitby.escribemeetings.com',
                "label": 'Whitby Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC-ZadVBUjEQuqndWEUc-fhg',
                "label": 'Whitby YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Whitchurch-Stouffville': {
        "website_url": 'https://www.whitchurchstouffville.ca/',
        "sources": [
        ],
    },
    'White River': {
        "website_url": 'https://www.whiteriver.ca/',
        "sources": [
        ],
    },
    'Whitestone': {
        "website_url": 'https://www.whitestone.ca/',
        "sources": [
        ],
    },
    'Whitewater Region': {
        "website_url": 'https://www.whitewaterregion.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://whitewaterregion.civicweb.net/portal/',
                "label": 'Whitewater Region Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wilmot': {
        "website_url": 'https://www.wilmot.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCcA8fcRx03H8zYkFLIQMjow',
                "label": 'Wilmot YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wollaston': {
        "website_url": 'https://www.wollaston.ca/',
        "sources": [
        ],
    },
    'Woodstock': {
        "website_url": 'https://www.cityofwoodstock.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCZ13kYbY4HVx_0FVBPJ2k8g',
                "label": 'Woodstock YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Woolwich': {
        "website_url": 'https://www.woolwich.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@woolwichtownship9588',
                "label": 'Woolwich YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
}
