# Alberta Rollout — Phase 1

**Status:** infrastructure validated, scraping live for 6/10 cities, 3/10 partially live.
**Date validated:** 2026-05-04 (live HTTP fetches against each source).

This document captures the per-municipality state of Alberta Phase 1 after live
validation. Use it as the baseline when triaging future regressions; rerun
`scripts/poll.py "<short_name>"` against each muni to refresh the status.

## Phase 0 / Phase 1 — what shipped

- **Phase 0** (commits `41315a0`, `b6268e8`): backend `province` column,
  Alembic migration `002_add_province_columns`, `/api/v1/municipalities?province=…`
  filter, `province` field on subscribe, frontend BC/Alberta tab,
  291 Alberta seed entries (10 Phase 1 + 281 PENDING placeholders).
- **Phase 1** (commits `fe1b1f5`, `0c97776`, `c777d48`, `ee7a109`):
  YouTube `@handle` → `UCxxx` resolver, `scripts/poll.py` ops CLI,
  corrected portal URLs for the 10 Phase 1 cities, eSCRIBE JSON-rendered
  grid fallback, fixture-based regression tests.

## Per-municipality status

| # | Municipality       | Platform → Source URL                                            | Live items (2026-05-04) | Notes |
|---|--------------------|------------------------------------------------------------------|-------------------------|-------|
| 1 | Calgary            | eSCRIBE — `pub-calgary.escribemeetings.com`                       | 8 agendas               | OK |
|   |                    | YouTube — `@thecityofcalgary`                                     | 0 (channel valid)       | Channel posts mostly non-meeting content |
| 2 | Edmonton           | eSCRIBE — `pub-edmonton.escribemeetings.com`                      | 0                       | Calendar UI loaded entirely via AJAX. JSON fallback regex finds zero IDs in the static HTML — needs eSCRIBE Web API call (deferred). |
|   |                    | YouTube — `@CityofEdmonton`                                       | 0 (channel valid)       | Channel valid, no recent meeting-classified videos |
| 3 | Red Deer           | eSCRIBE — `pub-reddeer.escribemeetings.com`                       | 0                       | Same as Edmonton — AJAX-loaded calendar |
|   |                    | YouTube — `@TheCityofRedDeer`                                     | 0 (channel valid)       |   |
| 4 | Lethbridge         | eSCRIBE — `pub-lethbridge.escribemeetings.com`                    | **5 agendas**           | OK; FileStream `<a>` in HTML |
|   |                    | YouTube — `@CityofLethbridge`                                     | **7 videos**            | OK |
| 5 | Medicine Hat       | eSCRIBE — `pub-medicinehat.escribemeetings.com`                   | 0                       | AJAX-only calendar |
|   |                    | YouTube — `@CityMedicineHat`                                      | **3 videos**            | OK (handle had to be corrected from `@CityofMedicineHatAB`) |
| 6 | Airdrie            | eSCRIBE — `pub-airdrie.escribemeetings.com`                       | **4 agendas**           | OK |
|   |                    | YouTube — `@CityofAirdrie` (PENDING)                              | n/a                     | No discoverable public council channel; demoted to PENDING |
| 7 | Spruce Grove       | eSCRIBE — `pub-sprucegrove.escribemeetings.com`                   | 0                       | Initially seeded as CivicWeb; corrected to eSCRIBE. Calendar AJAX-only. |
|   |                    | YouTube — `@CityofSpruceGrove`                                    | 0 (channel valid)       |   |
| 8 | Grande Prairie     | eSCRIBE — `pub-cityofgp.escribemeetings.com`                      | **10 agendas**          | OK (URL was `pub-grandeprairie` in initial seed, corrected) |
|   |                    | YouTube — `/user/GrandePrairieCA`                                 | **3 videos**            | OK (legacy `/user/` URL, real channel) |
| 9 | St. Albert         | Custom (Legistar) — `stalbert.ca.legistar.com/Calendar.aspx` (PENDING) | n/a                | St. Albert uses **Legistar**, which we don't yet have a scraper for. Demoted to PENDING. |
|   |                    | YouTube — `/user/CityofStAlbert`                                  | **3 videos**            | OK |
| 10| Fort McMurray (Wood Buffalo) | eSCRIBE — `pub-rmwb.escribemeetings.com`              | 0                       | AJAX-only calendar |
|   |                    | YouTube — `/user/rmwbwebmaster`                                   | **5 videos**            | OK |

**Headline: 6 of 10 cities are producing live items today (Calgary, Lethbridge, Medicine Hat, Airdrie, Grande Prairie, St. Albert via YouTube).**
The other 4 (Edmonton, Red Deer, Spruce Grove, Fort McMurray) have valid YouTube channels but blank discoveries because the channels haven't published meeting-classified videos recently. Their eSCRIBE portals load meetings client-side via AJAX into an empty calendar, which the existing static-HTML scraper can't see.

## Active vs. pending sources by platform

| Platform | ACTIVE | PENDING | Notes |
|----------|-------:|--------:|-------|
| eSCRIBE  | 9      | 0       | All 9 ACTIVE eSCRIBE URLs respond 200 |
| YouTube  | 9      | 1       | Airdrie demoted; channel handle not discoverable |
| Custom (Legistar) | 0 | 2  | St. Albert agendas + minutes — needs new scraper |

(Each muni has 3 source slots; eSCRIBE agendas + minutes share one URL per muni so they show up as 1 ACTIVE eSCRIBE row in the validator. Source row count is preserved at 30 in the seed for inventory purposes.)

## Known issues blocking 100% Phase 1 coverage

1. **eSCRIBE AJAX-only calendars (Edmonton / Red Deer / Medicine Hat / Spruce Grove / Wood Buffalo)** — the meeting list is fetched after page load via JS and never appears in the static HTML the scraper sees. The fix is to call the eSCRIBE Web API endpoint (`/Web/api/Meeting/...`) directly. Targeted for Phase 2.
2. **Legistar (St. Albert)** — needs a brand-new platform scraper. Targeted for Phase 2.
3. **Airdrie YouTube channel** — no public meeting channel is linked from `airdrie.ca` and a brute-force search of common handles all 404. Will revisit if a channel is published.

## How to validate

```bash
# Single muni
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt python3 scripts/poll.py "Calgary"

# Whole province
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt python3 scripts/poll.py --province Alberta

# JSON output (for scripting / CI)
python3 scripts/poll.py "Calgary" --json
```

The `SSL_CERT_FILE` env var is only needed in environments where Python can't find the system CA bundle; production deployments don't need it.

## Regression coverage

`backend/tests/test_alberta_scrapers.py` (4 tests):
- `test_escribe_lethbridge_anchor_path` — pinned snapshot, verifies regular `<a href>` parse path still yields FileStream agendas.
- `test_escribe_calgary_yields_filestream_items` — pinned snapshot, verifies Syncfusion-rendered grid still produces FileStream items.
- `test_escribe_json_fallback_runs_when_anchor_path_yields_nothing` — synthetic HTML, verifies the JSON-fallback fan-out triggers and harvests detail pages.
- `test_alberta_phase_1_seed_inventory` — hard-coded list of the 10 short_names + 3-source-per-muni invariant; fails loudly on accidental deletions.

`backend/tests/test_youtube.py` (5 new tests for the `resolve_channel_id` helper) plus `backend/tests/test_poll_pipeline.py` (3 new YouTube poller tests for cache-hit, fresh-resolution, and resolution-failure paths).

Total backend suite: **205 passing**.

## Out of scope (future phases)

- eSCRIBE Web API integration for AJAX-only calendars
- Legistar platform scraper (St. Albert + many other AB cities will need it)
- Phase 2 municipalities (Banff, Canmore, Cochrane, Okotoks, Strathcona County, etc.)
- PDF parsing pipeline (PyMuPDF / pdfplumber)
- AB Municipal Affairs open-data ingestion
