# Alberta Rollout — Issue Tracker

Living tracker for every Alberta municipality, every source, and every issue
discovered while bringing them online. **Updated after every phase.**

## Issue ledger

Issues are numbered, dated, and either **OPEN** or **CLOSED**. Each phase
updates this section first.

| ID | Status | Discovered | Description | Affected | Resolution |
|----|--------|------------|-------------|----------|------------|
| AB-001 | CLOSED | Phase 1 | YouTube `@handle` URL fed straight to RSS feed produces 404 because YT requires `UCxxx` channel ids. | All AB+BC YouTube sources with handle URLs | Added `resolve_channel_id()` helper, cached resolution into `Source.scrape_config` (commit `fe1b1f5`). |
| AB-002 | CLOSED | Phase 1 | Six AB Phase 1 portal URLs were guessed and 404 (Red Deer / Spruce Grove on CivicWeb, Grande Prairie eSCRIBE subdomain, St. Albert on Legistar). | Red Deer, Spruce Grove, Grande Prairie, St. Albert | Live-probed real portals and corrected seed entries (commit `c777d48`). |
| AB-003 | CLOSED | Phase 1 | Seven AB YouTube `@handles` 404. | Calgary, Red Deer, Medicine Hat, Wood Buffalo, Grande Prairie, St. Albert, Airdrie | Corrected handles for 6 munis; demoted Airdrie to PENDING (no public meeting channel). |
| AB-004 | CLOSED | Phase 1 | Modern eSCRIBE deployments render the meeting list client-side from a JSON grid (Syncfusion); BeautifulSoup never sees the meeting links. | Calgary and others using new eSCRIBE template | Added `_scrape_meetings_from_json()` regex fallback that fans out to detail pages (commit `c777d48`). |
| AB-005 | CLOSED | Phase 1 | Seed registered separate AGENDA + MINUTES rows for the same eSCRIBE URL → DB dedup left the seed and DB out of sync. | All 10 Phase 1 munis | Collapsed each muni to one portal row (commit `80f450d`). |
| AB-006 | CLOSED | Phase 1 | Poller forced `scrape_status = ACTIVE` after every successful poll, silently un-demoting operator-set PENDING. | Airdrie YT, St. Albert Legistar | Auto-promotion now restricted to BROKEN → ACTIVE (commit `80f450d`). |
| AB-007 | OPEN   | Phase 1 | Five AB cities load their eSCRIBE meeting list entirely via AJAX into an empty calendar; static HTML has zero meeting IDs even after the JSON-fallback regex. | Edmonton, Red Deer, Medicine Hat, Spruce Grove, Wood Buffalo | Needs eSCRIBE Web API integration (`/Web/api/Meeting/...`). Targeted for a dedicated PR after the muni inventory finishes. |
| AB-008 | OPEN   | Phase 1 | No Legistar scraper exists, so `Platform.CUSTOM` placeholder sources can't ingest. | St. Albert (and likely future Phase 2+ Legistar munis) | Needs a new `LegistarScraper` class. Targeted alongside AB-007. |
| AB-009 | OPEN   | Phase 1 | Pre-existing repo bug: SQLAlchemy emits enum values as Python names (`CITY`) but the Alembic migration creates them lowercase (`city`). Production worked because it used `Base.metadata.create_all`; local Alembic-applied DBs need manual enum recreation. | All deployments using Alembic from scratch | Fix is a separate cleanup PR (out of AB rollout scope, but logged for visibility). |

New issues discovered while phasing through the remaining ~280 AB munis are
appended to this table with IDs `AB-010+`.

## Validation matrix

Each row below is one Alberta municipality. Columns:
- **Phase** — when this muni was processed (1 = Phase 1 cities, 2..N = subsequent batches).
- **Sources** — count of source rows in the seed (typically 2 for fully-onboarded munis, 1 for placeholder).
- **Platform** — primary discovery platform (eSCRIBE / CivicWeb / Granicus / Legistar / Custom / YouTube only / unknown).
- **Status** — VALIDATED (≥1 source returns items live), READY (URLs resolve but no items today), DEMOTED (operator-set PENDING — no working source), PLACEHOLDER (still pointing at the directory placeholder URL).
- **Last validated** — UTC date of last live `scripts/poll.py` run.
- **Notes / linked issues**.

The matrix below is rebuilt after each phase. Phase 1 entries are populated;
remaining 281 munis start as `Phase: -` / `Status: PLACEHOLDER` and migrate
into rows as their batches run.

### Phase 1 (10 munis — completed 2026-05-04)

| # | Municipality       | Phase | Sources | Platform           | Status     | Last validated | Notes |
|---|--------------------|------:|--------:|--------------------|------------|----------------|-------|
| 1 | Calgary            | 1     | 2       | eSCRIBE + YouTube  | VALIDATED  | 2026-05-04 | eSCRIBE returns 8 agendas; YT channel valid (no recent meeting videos). |
| 2 | Edmonton           | 1     | 2       | eSCRIBE + YouTube  | READY      | 2026-05-04 | AJAX-only calendar, see AB-007. |
| 3 | Red Deer           | 1     | 2       | eSCRIBE + YouTube  | READY      | 2026-05-04 | AJAX-only calendar, see AB-007. |
| 4 | Lethbridge         | 1     | 2       | eSCRIBE + YouTube  | VALIDATED  | 2026-05-04 | eSCRIBE 5 agendas, YT 7 videos. |
| 5 | Medicine Hat       | 1     | 2       | eSCRIBE + YouTube  | VALIDATED  | 2026-05-04 | eSCRIBE 0 (AB-007), YT 3 videos. |
| 6 | Airdrie            | 1     | 2       | eSCRIBE + YouTube* | VALIDATED  | 2026-05-04 | eSCRIBE 4 agendas; YT demoted PENDING (no public channel). |
| 7 | Spruce Grove       | 1     | 2       | eSCRIBE + YouTube  | READY      | 2026-05-04 | AJAX-only calendar, see AB-007. |
| 8 | Grande Prairie     | 1     | 2       | eSCRIBE + YouTube  | VALIDATED  | 2026-05-04 | eSCRIBE 10 agendas, YT 3 videos. |
| 9 | St. Albert         | 1     | 2       | Legistar* + YouTube| VALIDATED  | 2026-05-04 | YT 3 videos; Legistar PENDING (AB-008). |
| 10| Fort McMurray (RMWB)| 1    | 2       | eSCRIBE + YouTube  | VALIDATED  | 2026-05-04 | eSCRIBE 0 (AB-007), YT 5 videos. |

### Phases 2..N (281 remaining munis)

To be filled in 10-muni batches. The roster lives in
`backend/app/services/seed_registry.py::ALBERTA_MUNICIPALITIES_REMAINDER`
and is processed in alphabetical order of `short_name` so progress is
deterministic.

A separate sub-table is appended after each phase, with the same columns as
Phase 1 above. Phases that consist entirely of summer villages (or other
sparse-data entities) stay PLACEHOLDER and explicitly note the rationale.

## Roll-out cadence

- **Per phase**: 10 munis. Probe portals, update seed, run `scripts/poll.py`,
  assess, log issues, commit, push, update this tracker.
- **Hard stop conditions** (would pause the rollout): a regression in the
  backend test suite, an HTTP rate-limit response from a portal vendor, or
  a new issue category that needs design work before the next batch.

## How to update this tracker

1. Edit the issue ledger if any new issue was discovered. Use a fresh
   `AB-NNN` ID and date the entry. Mark closed issues `CLOSED` and link the
   commit hash.
2. Append a sub-table per phase showing the 10 munis just processed. Don't
   rewrite earlier phase tables.
3. Bump the "Phases completed" counter below.

## Phases completed

- **Phase 1** — 10 / 291 munis done (3.4%). Validated 2026-05-04.
- **Phase 2..N** — pending.

### Phase 2 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Acme | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Alberta Beach | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Alix | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Alliance | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Andrew | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Arrowwood | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Athabasca County | 1 | civicweb | VALIDATED | 3 | 3 items |
| Banff | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Barnwell | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Barons | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |

### Phase 3 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Barrhead | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Bassano | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Bawlf | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Beaumont | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Beaver County | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Bentley | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Berwyn | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Big Lakes County | 1 | escribe | READY | 0 | URLs resolve, no items today |
| Big Valley | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Birch Hills County | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |

### Phase 4 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Bittern Lake | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Black Diamond | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Blackfalds | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Bon Accord | 1 | youtube | VALIDATED | 4 | 4 items |
| Bonnyville | 1 | youtube | VALIDATED | 13 | 13 items |
| Bow Island | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Bowden | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Boyle | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Brazeau County | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Brooks | 1 | youtube | VALIDATED | 15 | 15 items |

### Phase 5 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Bruderheim | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Buffalo Lake | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Camrose | 2 | civicweb + youtube | VALIDATED | 1 | 1 items |
| Camrose County | 2 | civicweb + youtube | VALIDATED | 1 | 1 items |
| Canmore | 1 | youtube | VALIDATED | 7 | 7 items |
| Carbon | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Cardston | 1 | youtube | VALIDATED | 14 | 14 items |
| Cardston County | 1 | youtube | VALIDATED | 14 | 14 items |
| Carmangay | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Caroline | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |

### Phase 6 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Carstairs | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Castor | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Chauvin | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Chestermere | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Chipman | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Claresholm | 2 | escribe + youtube | VALIDATED | 7 | 7 items |
| Clear Hills County | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Clearwater County | 2 | civicweb + youtube | VALIDATED | 12 | 12 items |
| Clive | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Clyde | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |

### Phase 7 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Coaldale | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Coalhurst | 1 | youtube | VALIDATED | 13 | 13 items |
| Cold Lake | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Coronation | 1 | civicweb | VALIDATED | 3 | 3 items |
| County of Barrhead | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| County of Grande Prairie | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| County of Minburn | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| County of Newell | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| County of Northern Lights | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| County of Stettler | 2 | escribe + youtube | VALIDATED | 8 | 8 items |

### Phase 8 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Crossfield | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Crowsnest Pass | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Cypress County | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Czar | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Daysland | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Delburne | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Delia | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Devon | 1 | youtube | READY | 0 | URLs resolve, no items today |
| Dewberry | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Didsbury | 2 | escribe + youtube | VALIDATED | 14 | 14 items |

### Phase 9 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Donalda | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Duchess | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| East Prairie | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Eckville | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Edgerton | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Edson | 2 | civicweb + youtube | VALIDATED | 12 | 12 items |
| Elizabeth | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Elk Point | 1 | youtube | VALIDATED | 12 | 12 items |
| Elnora | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Fairview | 2 | civicweb + youtube | VALIDATED | 11 | 11 items |

### Phase 10 (10 munis — 2026-05-04)

| Municipality | Sources | Platform | Status | Items | Notes |
|---|---:|---|---|---:|---|
| Falher | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Ferintosh | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Fishing Lake | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Flagstaff County | 2 | escribe + youtube | VALIDATED | 2 | 2 items |
| Foothills County | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Foremost | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Fort Macleod | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Fox Creek | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
| Gibbons | 1 | youtube | VALIDATED | 13 | 13 items |
| Gift Lake | 1 | custom* | PLACEHOLDER | 0 | no portal discovered yet |
