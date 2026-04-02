# prj0000097-stub-module-elimination - Project Overview

_Status: RELEASED_
_Owner: @1project | Updated: 2026-03-29_

## Project Identity
**Project ID:** prj0000097
**Short name:** stub-module-elimination
**Project folder:** `docs/project/prj0000097-stub-module-elimination/`

## Project Overview
Initialize project from idea000011-stub-module-elimination to discover and plan removal
of stub modules and placeholder implementations that hide missing production logic.

## Goal & Scope
**Goal:** Define a safe, staged remediation path to eliminate stub modules and replace them
with verified implementations.
**In scope:**
- Discovery artifacts for stub/module elimination strategy.
- Governance registration and lifecycle tracking.
- Scope map for candidate files under `src/`, `src-old/`, and related tests.
**Out of scope:**
- Implementing remediation code in this @1project step.
- Changing unrelated project lanes or registry rows.

## Branch Plan
**Expected branch:** prj0000097-stub-module-elimination
**Scope boundary:**
- `src/rl/`
- `src/speculation/`
- `tests/rl/`
- `tests/speculation/`
- `tests/guards/test_rl_speculation_import_scope.py`
- `tests/test_rl_package.py`
- `tests/test_speculation_package.py`
- `docs/project/prj0000097-stub-module-elimination/`
- `.github/agents/data/1project.memory.md`
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active
branch matches this project and changed files stay inside the scope boundary.
**Failure rule:** If project ID or branch plan is missing, conflicting, inherited, or
ambiguous, return task to `@0master` before downstream handoff.

## Canonical Artifacts
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.think.md`
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.design.md`
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.plan.md`
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.test.md`
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.code.md`
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.exec.md`
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.ql.md`
- `docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.git.md`

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Options explored | @2think | DONE |
| M2 | Design confirmed | @3design | DONE |
| M3 | Plan finalized | @4plan | DONE |
| M4 | Tests written | @5test | DONE |
| M5 | Code implemented | @6code | DONE |
| M6 | Integration validated | @7exec | DONE |
| M7 | Security clean | @8ql | DONE |
| M8 | Committed | @9git | DONE (merged via #243) |

## Status
_Last updated: 2026-03-29_
Project lifecycle completed and released after downstream completion.

Evidence references:
- Tests complete: `prj0000097-stub-module-elimination.test.md` documents Slice 1 AC coverage and contract/deprecation/guard suites for rl/speculation.
- Code complete: `prj0000097-stub-module-elimination.code.md` records implementation in `src/rl/__init__.py` and `src/speculation/__init__.py` plus targeted and full-suite green runs (`1272 passed, 10 skipped`).
- Execution complete: `prj0000097-stub-module-elimination.exec.md` confirms branch gate PASS and validation commands PASS (`pytest -v --maxfail=1` and targeted rl/speculation/guard slice).
- Quality/security complete: `prj0000097-stub-module-elimination.ql.md` reports overall `CLEAR -> @9git` with one non-blocking governance-drift note resolved here by scope-boundary alignment.
- Release complete: PR #243 merged to `main`; lifecycle transitioned from Review to Released.

One-project-one-branch policy remains enforced via the unchanged Branch Plan handoff rule and expected branch `prj0000097-stub-module-elimination`.
