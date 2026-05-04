"""Auto-generated from docs/alberta-probe-report.json by
``scripts/apply_alberta_probe.py``. Do not edit by hand —
re-run the script if the probe report changes."""

# Strings reference Platform / SourceType / ScrapeStatus enum values
# defined in app.models.municipality. seed_registry resolves them at
# import time so this module stays free of model-side dependencies.

REMAINDER_PATCHES: dict = {
    'Acme': {
        "website_url": 'https://www.acme.ca/',
        "sources": [
        ],
    },
    'Alix': {
        "website_url": 'https://www.villageofalix.ca/',
        "sources": [
        ],
    },
    'Alliance': {
        "website_url": 'https://www.villageofalliance.ca/',
        "sources": [
        ],
    },
    'Arrowwood': {
        "website_url": 'https://www.villageofarrowwood.ca/',
        "sources": [
        ],
    },
    'Athabasca County': {
        "website_url": 'https://www.athabasca.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://athabasca.civicweb.net/filepro/documents',
                "label": 'Athabasca County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Banff': {
        "website_url": 'https://www.banff.ca/',
        "sources": [
        ],
    },
    'Barnwell': {
        "website_url": 'https://www.barnwell.ca/',
        "sources": [
        ],
    },
    'Barons': {
        "website_url": 'https://www.barons.ca/',
        "sources": [
        ],
    },
    'Barrhead': {
        "website_url": 'https://www.barrhead.ca/',
        "sources": [
        ],
    },
    'Bassano': {
        "website_url": 'https://bassano.ca/',
        "sources": [
        ],
    },
    'Beaumont': {
        "website_url": 'https://www.beaumont.ca/',
        "sources": [
        ],
    },
    'Beaver County': {
        "website_url": 'https://www.beavercounty.ca/',
        "sources": [
        ],
    },
    'Bentley': {
        "website_url": 'https://townofbentley.ca/',
        "sources": [
        ],
    },
    'Berwyn': {
        "website_url": 'https://www.berwyn.ca/',
        "sources": [
        ],
    },
    'Big Lakes County': {
        "website_url": 'https://www.biglakescounty.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-biglakescounty.escribemeetings.com',
                "label": 'Big Lakes County Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Big Valley': {
        "website_url": 'https://www.villageofbigvalley.ca/',
        "sources": [
        ],
    },
    'Bittern Lake': {
        "website_url": 'https://www.villageofbitternlake.ca/',
        "sources": [
        ],
    },
    'Black Diamond': {
        "website_url": 'https://www.blackdiamond.ca/',
        "sources": [
        ],
    },
    'Blackfalds': {
        "website_url": 'https://www.blackfalds.ca/',
        "sources": [
        ],
    },
    'Bon Accord': {
        "website_url": 'https://www.bonaccord.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@bonaccordab',
                "label": 'Bon Accord YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Bonnyville': {
        "website_url": 'https://www.bonnyville.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCzzqOo841-77fv6ifGuV2FQ',
                "label": 'Bonnyville YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Bowden': {
        "website_url": 'https://www.bowden.ca/',
        "sources": [
        ],
    },
    'Brooks': {
        "website_url": 'https://www.brooks.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@CityOfBrooksAB',
                "label": 'Brooks YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Bruderheim': {
        "website_url": 'https://www.bruderheim.ca/',
        "sources": [
        ],
    },
    'Camrose': {
        "website_url": 'https://www.camrose.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://camrose.civicweb.net',
                "label": 'Camrose Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@city-of-camrose',
                "label": 'Camrose YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Camrose County': {
        "website_url": 'https://www.camrose.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://camrose.civicweb.net',
                "label": 'Camrose County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@city-of-camrose',
                "label": 'Camrose County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Canmore': {
        "website_url": 'https://www.canmore.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@thetownofcanmore',
                "label": 'Canmore YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Carbon': {
        "website_url": 'https://www.carbon.ca/',
        "sources": [
        ],
    },
    'Cardston': {
        "website_url": 'https://www.cardston.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCaCwvtT_3RDAa4pxw89e1zg',
                "label": 'Cardston YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Cardston County': {
        "website_url": 'https://www.cardston.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCaCwvtT_3RDAa4pxw89e1zg',
                "label": 'Cardston County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Carmangay': {
        "website_url": 'https://www.carmangay.ca/',
        "sources": [
        ],
    },
    'Carstairs': {
        "website_url": 'https://www.carstairs.ca/',
        "sources": [
        ],
    },
    'Chestermere': {
        "website_url": 'https://www.chestermere.ca/',
        "sources": [
        ],
    },
    'Claresholm': {
        "website_url": 'https://www.claresholm.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-claresholm.escribemeetings.com',
                "label": 'Claresholm Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCe3OPyLhTzPajvPVAtNL1KA',
                "label": 'Claresholm YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Clearwater County': {
        "website_url": 'https://www.clearwatercounty.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://clearwatercounty.civicweb.net',
                "label": 'Clearwater County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/ClearwaterCounty',
                "label": 'Clearwater County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Clive': {
        "website_url": 'https://www.clive.ca/',
        "sources": [
        ],
    },
    'Clyde': {
        "website_url": 'https://www.villageofclyde.ca/',
        "sources": [
        ],
    },
    'Coaldale': {
        "website_url": 'https://www.coaldale.ca/',
        "sources": [
        ],
    },
    'Coalhurst': {
        "website_url": 'https://www.coalhurst.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TownofCoalhurstAB',
                "label": 'Coalhurst YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Coronation': {
        "website_url": 'https://www.coronation.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://coronation.civicweb.net/filepro/documents/',
                "label": 'Coronation Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'County of Barrhead': {
        "website_url": 'https://www.barrhead.ca/',
        "sources": [
        ],
    },
    'County of Stettler': {
        "website_url": 'https://www.stettlercounty.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-stettlercounty.escribemeetings.com',
                "label": 'County of Stettler Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/StettlerCounty',
                "label": 'County of Stettler YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Crowsnest Pass': {
        "website_url": 'https://www.crowsnestpass.ca/',
        "sources": [
        ],
    },
    'Czar': {
        "website_url": 'https://www.villageofczar.ca/',
        "sources": [
        ],
    },
    'Daysland': {
        "website_url": 'https://www.daysland.ca/',
        "sources": [
        ],
    },
    'Delburne': {
        "website_url": 'https://www.delburne.ca/',
        "sources": [
        ],
    },
    'Delia': {
        "website_url": 'https://www.delia.ca/',
        "sources": [
        ],
    },
    'Devon': {
        "website_url": 'https://www.devon.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/DevonAlberta',
                "label": 'Devon YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Dewberry': {
        "website_url": 'https://www.villageofdewberry.ca/',
        "sources": [
        ],
    },
    'Didsbury': {
        "website_url": 'https://www.didsbury.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'http://pub-didsbury.escribemeetings.com',
                "label": 'Didsbury Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'http://www.youtube.com/channel/UC-J11Gmd6oTHRcAWNdzy9fg',
                "label": 'Didsbury YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'East Prairie': {
        "website_url": 'https://www.eastprairie.ca/',
        "sources": [
        ],
    },
    'Edgerton': {
        "website_url": 'https://www.edgerton.ca/',
        "sources": [
        ],
    },
    'Edson': {
        "website_url": 'https://www.edson.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'http://edson.civicweb.net',
                "label": 'Edson Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC0xPmAO5OEP78QFzznJtt5g',
                "label": 'Edson YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Elizabeth': {
        "website_url": 'https://www.elizabeth.ca/',
        "sources": [
        ],
    },
    'Elk Point': {
        "website_url": 'https://www.elkpoint.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofelkpoint3953',
                "label": 'Elk Point YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Fairview': {
        "website_url": 'https://www.fairview.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://fairview.civicweb.net',
                "label": 'Fairview Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCbjwk3a_3T2149jWJuH-NeA',
                "label": 'Fairview YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Falher': {
        "website_url": 'https://www.falher.ca/',
        "sources": [
        ],
    },
    'Fishing Lake': {
        "website_url": 'https://www.fishinglake.ca/',
        "sources": [
        ],
    },
    'Flagstaff County': {
        "website_url": 'https://www.flagstaff.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-flagstaffcounty.escribemeetings.com?FillWidth=1',
                "label": 'Flagstaff County Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCQQgpaW6Wl7mlEWvHqvXESQ',
                "label": 'Flagstaff County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Foremost': {
        "website_url": 'https://www.foremost.ca/',
        "sources": [
        ],
    },
    'Fox Creek': {
        "website_url": 'https://www.foxcreek.ca/',
        "sources": [
        ],
    },
    'Gibbons': {
        "website_url": 'https://www.gibbons.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofgibbons9669',
                "label": 'Gibbons YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Girouxville': {
        "website_url": 'https://www.girouxville.ca/',
        "sources": [
        ],
    },
    'Glendon': {
        "website_url": 'https://www.villageofglendon.ca/',
        "sources": [
        ],
    },
    'Grimshaw': {
        "website_url": 'https://www.grimshaw.ca/',
        "sources": [
        ],
    },
    'Hanna': {
        "website_url": 'https://www.hanna.ca/',
        "sources": [
        ],
    },
    'Hardisty': {
        "website_url": 'https://www.hardisty.ca/',
        "sources": [
        ],
    },
    'Heisler': {
        "website_url": 'https://www.villageofheisler.ca/',
        "sources": [
        ],
    },
    'High Level': {
        "website_url": 'https://www.highlevel.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townhighlevel',
                "label": 'High Level YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'High Prairie': {
        "website_url": 'https://www.highprairie.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCCVAh6oIAOQlKspVSJRKrsg',
                "label": 'High Prairie YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'High River': {
        "website_url": 'https://www.highriver.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://highriver.civicweb.net',
                "label": 'High River Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofhighriver',
                "label": 'High River YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Hill Spring': {
        "website_url": 'https://www.hillspring.ca/',
        "sources": [
        ],
    },
    'Hinton': {
        "website_url": 'https://www.hinton.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'http://hinton.civicweb.net',
                "label": 'Hinton Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@HintonAB',
                "label": 'Hinton YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Hussar': {
        "website_url": 'https://www.villageofhussar.ca/',
        "sources": [
        ],
    },
    'Innisfail': {
        "website_url": 'https://www.innisfail.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://innisfail.civicweb.net/filepro/documents/158313/',
                "label": 'Innisfail Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Irricana': {
        "website_url": 'https://townofirricana.ca/',
        "sources": [
        ],
    },
    'Jasper': {
        "website_url": 'https://jasper.ca/',
        "sources": [
        ],
    },
    'Lacombe': {
        "website_url": 'https://www.lacombe.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCMS2L0Hbvg5vcNHRRU34gwg',
                "label": 'Lacombe YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Lamont': {
        "website_url": 'https://www.lamont.ca/',
        "sources": [
        ],
    },
    'Lamont County': {
        "website_url": 'https://www.lamontcounty.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://lamontcounty.civicweb.net/document/59621',
                "label": 'Lamont County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@LamontCounty',
                "label": 'Lamont County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Leduc': {
        "website_url": 'https://www.leduc.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://bm-public-leduc.escribemeetings.com',
                "label": 'Leduc Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CityofLeduc',
                "label": 'Leduc YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Leduc County': {
        "website_url": 'https://www.leduc.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://bm-public-leduc.escribemeetings.com',
                "label": 'Leduc County Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/CityofLeduc',
                "label": 'Leduc County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Legal': {
        "website_url": 'https://www.legal.ca/',
        "sources": [
        ],
    },
    'Linden': {
        "website_url": 'https://www.linden.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://linden.civicweb.net',
                "label": 'Linden Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Lloydminster': {
        "website_url": 'https://www.lloydminster.ca/',
        "sources": [
        ],
    },
    'Lomond': {
        "website_url": 'https://www.villageoflomond.ca/',
        "sources": [
        ],
    },
    'Lougheed': {
        "website_url": 'https://www.lougheed.ca/',
        "sources": [
        ],
    },
    'Mackenzie County': {
        "website_url": 'https://www.mackenzie.ca/',
        "sources": [
        ],
    },
    'Magrath': {
        "website_url": 'https://www.magrath.ca/',
        "sources": [
        ],
    },
    'Manning': {
        "website_url": 'https://manning.ca/',
        "sources": [
        ],
    },
    'Mannville': {
        "website_url": 'https://www.mannville.ca/',
        "sources": [
        ],
    },
    'Marwayne': {
        "website_url": 'https://www.marwayne.ca/',
        "sources": [
        ],
    },
    'Mayerthorpe': {
        "website_url": 'https://www.mayerthorpe.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC_KdMZEn_zeXbOIQwthRqrg',
                "label": 'Mayerthorpe YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Milk River': {
        "website_url": 'https://www.milkriver.ca/',
        "sources": [
        ],
    },
    'Millet': {
        "website_url": 'https://www.millet.ca/',
        "sources": [
        ],
    },
    'Milo': {
        "website_url": 'https://www.villageofmilo.ca/',
        "sources": [
        ],
    },
    'Morinville': {
        "website_url": 'https://www.morinville.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-morinville.escribemeetings.com',
                "label": 'Morinville Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCd7C8Wp83ghqRWjGM7FmC-w',
                "label": 'Morinville YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Mundare': {
        "website_url": 'https://www.mundare.ca/',
        "sources": [
        ],
    },
    'Myrnam': {
        "website_url": 'https://www.myrnam.ca/',
        "sources": [
        ],
    },
    'Nanton': {
        "website_url": 'https://www.nanton.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofnanton5280',
                "label": 'Nanton YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Nobleford': {
        "website_url": 'https://www.nobleford.ca/',
        "sources": [
        ],
    },
    'Olds': {
        "website_url": 'https://www.olds.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC_NH_Sz_lONHVES9ltADIHw',
                "label": 'Olds YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Onoway': {
        "website_url": 'https://www.onoway.ca/',
        "sources": [
        ],
    },
    'Oyen': {
        "website_url": 'https://oyen.ca/',
        "sources": [
        ],
    },
    'Paradise Valley': {
        "website_url": 'https://www.paradise-valley.ca/',
        "sources": [
        ],
    },
    'Parkland County': {
        "website_url": 'https://www.parkland.ca/',
        "sources": [
        ],
    },
    'Peace River': {
        "website_url": 'https://www.peaceriver.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://peaceriver.civicweb.net',
                "label": 'Peace River Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townofpeaceriver8959',
                "label": 'Peace River YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Penhold': {
        "website_url": 'https://www.townofpenhold.ca/',
        "sources": [
        ],
    },
    'Picture Butte': {
        "website_url": 'https://www.picturebutte.ca/',
        "sources": [
        ],
    },
    'Pincher Creek': {
        "website_url": 'https://pinchercreek.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'http://pub-pinchercreek.escribemeetings.com',
                "label": 'Pincher Creek Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Ponoka': {
        "website_url": 'https://www.ponoka.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCcXFy3eUh6RPZOY1kOKS0lw',
                "label": 'Ponoka YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Ponoka County': {
        "website_url": 'https://www.ponoka.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCcXFy3eUh6RPZOY1kOKS0lw',
                "label": 'Ponoka County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Provost': {
        "website_url": 'https://www.provost.ca/',
        "sources": [
        ],
    },
    'Rainbow Lake': {
        "website_url": 'https://www.rainbowlake.ca/',
        "sources": [
        ],
    },
    'Raymond': {
        "website_url": 'https://www.raymond.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCiHirW3MvrAV0-WdyLGfo_g',
                "label": 'Raymond YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Redcliff': {
        "website_url": 'https://www.redcliff.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://redcliff.civicweb.net',
                "label": 'Redcliff Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Rocky View County': {
        "website_url": 'https://www.rockyviewcounty.ca/',
        "sources": [
        ],
    },
    'Rockyford': {
        "website_url": 'https://www.rockyford.ca/',
        "sources": [
        ],
    },
    'Rosalind': {
        "website_url": 'https://www.villageofrosalind.ca/',
        "sources": [
        ],
    },
    'Rycroft': {
        "website_url": 'https://www.rycroft.ca/',
        "sources": [
        ],
    },
    'Ryley': {
        "website_url": 'https://www.ryley.ca/',
        "sources": [
        ],
    },
    'SV Brentwood': {
        "website_url": 'https://www.brentwood.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/brentwoodcollege',
                "label": 'SV Brentwood YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'SV Crystal Springs': {
        "website_url": 'https://svcrystalsprings.ca/',
        "sources": [
        ],
    },
    'SV Grandview': {
        "website_url": 'https://www.grandview.ca/',
        "sources": [
        ],
    },
    'SV Lakeview': {
        "website_url": 'https://www.lakeview.ca/',
        "sources": [
        ],
    },
    'SV Larkspur': {
        "website_url": 'https://www.svlarkspur.ca/',
        "sources": [
        ],
    },
    'SV West Baptiste': {
        "website_url": 'https://www.svwestbaptiste.ca/',
        "sources": [
        ],
    },
    'SV West Cove': {
        "website_url": 'https://www.svwestcove.ca/',
        "sources": [
        ],
    },
    'SV Yellowstone': {
        "website_url": 'https://www.svyellowstone.ca/',
        "sources": [
        ],
    },
    'Sexsmith': {
        "website_url": 'https://www.sexsmith.ca/',
        "sources": [
        ],
    },
    'Slave Lake': {
        "website_url": 'https://www.slavelake.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://slavelake.civicweb.net',
                "label": 'Slave Lake Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCWF4_0QmulIhjBTlyRRb-gw',
                "label": 'Slave Lake YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Smoky Lake': {
        "website_url": 'https://www.smokylake.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'http://smokylake.civicweb.net',
                "label": 'Smoky Lake Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Spirit River': {
        "website_url": 'https://www.townofspiritriver.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://townofspiritriver.civicweb.net/filepro/documents/1009/',
                "label": 'Spirit River Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'St. Paul': {
        "website_url": 'https://www.stpaul.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://townstpaul.civicweb.net',
                "label": 'St. Paul Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UC2vFbG8WDfXeDvJNXRi2VyQ',
                "label": 'St. Paul YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Standard': {
        "website_url": 'https://www.villageofstandard.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@VillageofStandard',
                "label": 'Standard YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Stavely': {
        "website_url": 'https://www.stavely.ca/',
        "sources": [
        ],
    },
    'Stettler': {
        "website_url": 'https://www.stettlercounty.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-stettlercounty.escribemeetings.com',
                "label": 'Stettler Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/user/StettlerCounty',
                "label": 'Stettler YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Stirling': {
        "website_url": 'https://www.stirling.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCVtOpeAgjnv16vALUFAeg1A',
                "label": 'Stirling YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Strathcona County': {
        "website_url": 'https://www.strathconacounty.ca/',
        "sources": [
        ],
    },
    'Strathmore': {
        "website_url": 'https://www.strathmore.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@TOStrathmore',
                "label": 'Strathmore YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Sylvan Lake': {
        "website_url": 'https://www.sylvanlake.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://sylvanlake.civicweb.net',
                "label": 'Sylvan Lake Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCayZh8L9SE7cw4KRY2qKqqg',
                "label": 'Sylvan Lake YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Thorsby': {
        "website_url": 'https://www.thorsby.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCl8MsMmaRxJcU3tDInER2zA',
                "label": 'Thorsby YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Three Hills': {
        "website_url": 'https://www.threehills.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'http://threehills.civicweb.net/portal/',
                "label": 'Three Hills Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Vermilion': {
        "website_url": 'https://www.vermilion.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://vermilion.civicweb.net/user/signin?url=',
                "label": 'Vermilion Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCZIsdY7YnEiKcO_aNpqIkPw',
                "label": 'Vermilion YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Vilna': {
        "website_url": 'https://www.vilna.ca/',
        "sources": [
        ],
    },
    'Vulcan': {
        "website_url": 'https://www.townofvulcan.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://townofvulcan.civicweb.net/portal/',
                "label": 'Vulcan Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Vulcan County': {
        "website_url": 'https://www.townofvulcan.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://townofvulcan.civicweb.net/portal/',
                "label": 'Vulcan County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wabamun': {
        "website_url": 'https://www.wabamun.ca/',
        "sources": [
        ],
    },
    'Wainwright': {
        "website_url": 'https://www.wainwright.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@townwainwright',
                "label": 'Wainwright YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Warburg': {
        "website_url": 'https://www.warburg.ca/',
        "sources": [
        ],
    },
    'Warner': {
        "website_url": 'https://www.warner.ca/',
        "sources": [
        ],
    },
    'Westlock': {
        "website_url": 'https://www.westlock.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'http://www.youtube.com/user/TownofWestlock',
                "label": 'Westlock YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Westlock County': {
        "website_url": 'https://www.westlock.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'http://www.youtube.com/user/TownofWestlock',
                "label": 'Westlock County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wetaskiwin': {
        "website_url": 'https://www.wetaskiwin.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://wetaskiwin.civicweb.net',
                "label": 'Wetaskiwin Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCosEDSy_HiuWMUPY-uSYNhQ',
                "label": 'Wetaskiwin YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wetaskiwin County': {
        "website_url": 'https://www.wetaskiwin.ca/',
        "sources": [
            {
                "platform": "Platform.CIVICWEB",
                "source_type": "SourceType.AGENDA",
                "url": 'https://wetaskiwin.civicweb.net',
                "label": 'Wetaskiwin County Civicweb Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/channel/UCosEDSy_HiuWMUPY-uSYNhQ',
                "label": 'Wetaskiwin County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Wheatland County': {
        "website_url": 'https://wheatlandcounty.ca/',
        "sources": [
            {
                "platform": "Platform.ESCRIBE",
                "source_type": "SourceType.AGENDA",
                "url": 'https://pub-wheatland.escribemeetings.com',
                "label": 'Wheatland County Escribe Portal',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@wheatlandcounty703',
                "label": 'Wheatland County YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Whitecourt': {
        "website_url": 'https://www.whitecourt.ca/',
        "sources": [
            {
                "platform": "Platform.YOUTUBE",
                "source_type": "SourceType.VIDEO",
                "url": 'https://www.youtube.com/@WhitecourtAB',
                "label": 'Whitecourt YouTube',
                "scrape_status": "ScrapeStatus.ACTIVE",
            },
        ],
    },
    'Youngstown': {
        "website_url": 'https://www.youngstown.ca/',
        "sources": [
        ],
    },
}
