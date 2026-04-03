# rust-sub-crate-unification - Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-04-03_

## Project Identity
**Project ID:** prj0000117
**Short name:** rust-sub-crate-unification
**Project folder:** `docs/project/prj0000117-rust-sub-crate-unification/`

## Project Overview
Unify the standalone Rust sub-crates in `rust_core` under a single workspace-oriented project boundary so dependency graph management, lockfile strategy, and build governance can be designed and implemented consistently.

## Goal & Scope
**Goal:** Initialize and govern project boundary artifacts for idea000018 and prepare deterministic handoff to discovery/design/planning agents.
**In scope:** Project boundary setup, canonical artifact stubs, registry updates, idea mapping, validation evidence, memory/log updates.
**Out of scope:** Implementing Rust workspace refactors, Cargo manifest edits for behavior change, CI changes beyond boundary initialization.

## Branch Plan
**Expected branch:** prj0000117-rust-sub-crate-unification
**Scope boundary:** `docs/project/prj0000117-rust-sub-crate-unification/` plus `docs/project/kanban.json`, `data/projects.json`, `data/nextproject.md`, `docs/project/ideas/idea000018-rust-sub-crate-unification.md`, and `@1project` memory/log files.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch matches this project and changed files remain inside this scope boundary.
**Failure rule:** If project ID or branch plan is missing, conflicting, inherited, or ambiguous, return to `@0master` before downstream handoff.

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Options explored | @2think | NOT_STARTED |
| M2 | Design confirmed | @3design | NOT_STARTED |
| M3 | Plan finalized | @4plan | NOT_STARTED |
| M4 | Tests written | @5test | NOT_STARTED |
| M5 | Code implemented | @6code | NOT_STARTED |
| M6 | Integration validated | @7exec | NOT_STARTED |
| M7 | Security clean | @8ql | NOT_STARTED |
| M8 | Committed | @9git | NOT_STARTED |

## Status
_Last updated: 2026-04-03_
Project boundary initialized for prj0000117 with canonical artifacts created, registries synchronized, and governance validation executed. Registry validation passed; docs policy suite showed a known baseline legacy missing-file failure unrelated to this project boundary.
