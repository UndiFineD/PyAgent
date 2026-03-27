# async-runtime - Project Overview

_Status: DONE_
_Owner: @9git | Updated: 2026-03-21_

## Project Identity
**Project ID:** prj0000001
**Short name:** async-runtime
**Project folder:** docs/project/prj0000001/

## Project Overview
Stabilize and document the async runtime workstream so Python and Rust-backed execution paths provide one deterministic scheduling contract for core agent workloads.

## Goal & Scope
**Goal:** Maintain a reliable async runtime surface that works with Rust acceleration when available and pure-Python fallback when not.
**In scope:** Runtime API contract documentation, workflow artifact records, branch/scope governance metadata, and traceable pipeline status.
**Out of scope:** New runtime features, API expansion, cross-project refactors outside this folder, and retroactive code rewrites.

## Branch Plan
**Expected branch:** prj0000001-async-runtime
**Scope boundary:** docs/project/prj0000001/ plus explicitly approved governance files when required by policy tests.
**Handoff rule:** @9git must refuse staging, commit, push, or PR work unless branch and changed files match this project boundary.
**Failure rule:** If project ID or branch plan is missing, conflicting, or inherited from another workstream, return ownership to @0master before downstream handoff.

## Canonical Artifacts
- async-runtime.project.md
- async-runtime.think.md
- async-runtime.design.md
- async-runtime.plan.md
- async-runtime.test.md
- async-runtime.code.md
- async-runtime.exec.md
- async-runtime.ql.md
- async-runtime.git.md

## Pipeline Artifacts
| Artifact | Owner | Status | File |
|---|---|---|---|
| Options | @2think | DONE | async-runtime.think.md |
| Design | @3design | DONE | async-runtime.design.md |
| Plan | @4plan | DONE | async-runtime.plan.md |
| Tests | @5test | DONE | async-runtime.test.md |
| Code | @6code | DONE | async-runtime.code.md |
| Execution | @7exec | DONE | async-runtime.exec.md |
| Security | @8ql | DONE | async-runtime.ql.md |
| Git | @9git | DONE | async-runtime.git.md |

## Status
_Last updated: 2026-03-21_
- DONE — All pipeline stages complete. Async runtime on main with Rust acceleration + pure-Python fallback.
- 215+ tests passing, zero sync loops verified.
- Security scan completed, git handoff merged.


## Milestones
Legacy milestone details are not specified in this historical document.

