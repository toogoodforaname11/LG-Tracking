# Ontario Rollout — Issue Tracker

Living tracker for every Ontario municipality, every source, and every issue
discovered while bringing them online. **Updated after every phase.**

## Issue ledger

Issues are numbered, dated, and either **OPEN** or **CLOSED**. Each phase
updates this section first.

| ID | Status | Discovered | Description | Affected | Resolution |
|----|--------|------------|-------------|----------|------------|
| ON-001 | OPEN   | Phase 1 | Toronto's council portal at `secure.toronto.ca/council` is bespoke (not eSCRIBE/CivicWeb/Granicus). The existing platform scrapers don't understand its layout. | Toronto agendas + minutes | Needs a new `TorontoCouncilScraper`. Initial seed source ships PENDING; Toronto YouTube is ACTIVE. Targeted for a follow-up PR after the muni inventory finishes. |
| ON-002 | OPEN   | Phase 1 | The seed roster covers 349 of the official ~444 ON municipalities (Wikipedia's public list + hand-curated upper-tier/single-tier). The 95-muni gap is mostly small villages, townships and First Nations entities not on the public list. | All ON munis | Future phases manually seed missing entries via `_on_remainder_patches.py` as they're identified, same way AB phase work patched its long tail. |

New issues discovered while phasing through the remainder are appended with
IDs `ON-003+`.

## Validation matrix

Each row is one Ontario municipality. Columns:
- **Phase** — when this muni was processed (1 = Phase 1 cities, 2..N = subsequent batches).
- **Tier** — upper / lower / single.
- **Sources** — count of source rows in the seed.
- **Platform** — primary discovery platform (eSCRIBE / CivicWeb / Granicus / Custom / YouTube only / unknown).
- **Status** — VALIDATED (≥1 source returns items live), READY (URLs resolve but no items today), DEMOTED, PLACEHOLDER (still pointing at the AMO directory placeholder URL).
- **Last validated** — UTC date of last live `scripts/poll.py` run.
- **Notes / linked issues**.

The matrix is rebuilt after each phase. Phase 1 entries below; remaining
339 entries start as `Phase: -` / `Status: PLACEHOLDER` and migrate into
phase sub-tables as their batches run.

### Phase 1 (10 munis — completed 2026-05-04)

| # | Municipality | Tier   | Sources | Platform           | Status     | Items | Last validated | Notes |
|---|--------------|--------|--------:|--------------------|------------|------:|----------------|-------|
| 1 | Toronto      | single | 2       | Custom* + YouTube  | DEMOTED    | 0     | 2026-05-04 | Bespoke portal — see ON-001. |
| 2 | Ottawa       | single | 2       | eSCRIBE + YouTube  | READY      | 0     | 2026-05-04 | eSCRIBE portal returns 200 but no items today (AJAX-only calendar similar to AB-007). |
| 3 | Mississauga  | lower  | 2       | eSCRIBE + YouTube  | VALIDATED  | 13    | 2026-05-04 | eSCRIBE 13 agendas live. |
| 4 | Brampton     | lower  | 2       | eSCRIBE + YouTube  | VALIDATED  | 10    | 2026-05-04 | eSCRIBE 10 agendas live. |
| 5 | Hamilton     | single | 2       | eSCRIBE + YouTube  | VALIDATED  | 13    | 2026-05-04 | eSCRIBE 13 agendas live. |
| 6 | London       | single | 2       | eSCRIBE + YouTube  | VALIDATED  |  6    | 2026-05-04 | eSCRIBE 6 agendas live. |
| 7 | Markham      | lower  | 2       | eSCRIBE + YouTube  | VALIDATED  |  5    | 2026-05-04 | eSCRIBE 5 agendas live. |
| 8 | Vaughan      | lower  | 2       | eSCRIBE + YouTube  | VALIDATED  | 10    | 2026-05-04 | eSCRIBE 10 agendas live. |
| 9 | Kitchener    | lower  | 2       | eSCRIBE + YouTube  | VALIDATED  | 12    | 2026-05-04 | eSCRIBE 12 agendas live. |
| 10| Windsor      | single | 2       | eSCRIBE + YouTube  | READY      | 0     | 2026-05-04 | eSCRIBE portal returns 200 but no items today (AJAX-only calendar similar to AB-007). |

**Phase 1 summary**: 7/10 VALIDATED, 2 READY (AJAX-only — same pattern as AB-007), 1 DEMOTED (Toronto's custom portal — ON-001).

## Phases completed

- **Phase 1** — 10 / 349 munis done. 7 producing items live as of 2026-05-04.
- **Phases 2..N** — pending.

## How to advance the tracker

1. Edit the issue ledger if any new issue was discovered. Use a fresh
   `ON-NNN` ID and date the entry. Mark closed issues `CLOSED` with the
   commit hash.
2. Append a sub-table per phase showing the 10 munis just processed.
3. Bump the "Phases completed" counter above.
