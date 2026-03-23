# conky-real-metrics — Project Overview

_Status: HANDED_OFF_
_Owner: @1project | Updated: 2026-03-23_

## Project Identity
**Project ID:** prj0000047
**Short name:** conky-real-metrics
**Project folder:** `docs/project/prj0000047/`

## Project Overview
Replace the fake random-data simulation inside `web/apps/Conky.tsx` with real system metrics
(CPU %, Memory used/total, Network TX/RX KB/s per interface) polled from the host machine via
a new backend API endpoint exposed by `backend/app.py`.  The front-end widget will call that
endpoint at a configurable interval and render live values instead of Math.random() noise.

## Goal & Scope
**Goal:** Surface real CPU, memory, and network metrics in the Conky widget instead of simulated data.

**In scope:**
- `web/apps/Conky.tsx` — replace simulation loop with fetch to `/api/metrics/system`
- `backend/app.py` — add `GET /api/metrics/system` endpoint returning JSON metrics
- `web/vite.config.ts` — add Vite dev-server proxy rule for `/api` (if needed for offline fallback)

**Out of scope:**
- Any other widget, backend route, or top-level page
- Database persistence of metrics
- Alerting, thresholds, or historical charting
- Authentication changes

## Branch Plan
**Expected branch:** `prj0000047-conky-real-metrics`
**Scope boundary:** Files explicitly allowed to change:
  - `web/apps/Conky.tsx`
  - `backend/app.py`
  - `web/vite.config.ts` (only if a Vite dev-proxy rule is required)
  - `docs/project/prj0000047/` (all project artifacts)
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch is
`prj0000047-conky-real-metrics` and the changed files stay inside the scope boundary listed above.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous,
return the task to `@0master` before any downstream handoff.

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Options explored | @2think | |
| M2 | Design confirmed | @3design | |
| M3 | Plan finalized | @4plan | |
| M4 | Tests written | @5test | |
| M5 | Code implemented | @6code | |
| M6 | Integration validated | @7exec | |
| M7 | Security clean | @8ql | |
| M8 | Committed | @9git | |

## Acceptance Criteria
_Placeholder — to be filled by @3design_

- [ ] `GET /api/metrics/system` returns JSON with `cpu_percent`, `memory_used_mb`, `memory_total_mb`,
      and `network` (array of `{interface, tx_kbps, rx_kbps}`).
- [ ] Conky widget displays live values, refreshing at a configurable interval (default 2 s).
- [ ] No `Math.random()` or simulated data remains in `Conky.tsx`.
- [ ] All existing tests pass; new unit tests cover the backend endpoint.

## Canonical Artifact Links
| Artifact | File |
|---|---|
| Options | [conky-real-metrics.think.md](conky-real-metrics.think.md) |
| Design | [conky-real-metrics.design.md](conky-real-metrics.design.md) |
| Plan | [conky-real-metrics.plan.md](conky-real-metrics.plan.md) |
| Tests | [conky-real-metrics.test.md](conky-real-metrics.test.md) |
| Code | [conky-real-metrics.code.md](conky-real-metrics.code.md) |
| Exec | [conky-real-metrics.exec.md](conky-real-metrics.exec.md) |
| Security | [conky-real-metrics.ql.md](conky-real-metrics.ql.md) |
| Git | [conky-real-metrics.git.md](conky-real-metrics.git.md) |

## Status
_Last updated: 2026-03-23_
Project folder created; all stubs initialised. Awaiting handoff to @2think for options exploration.
