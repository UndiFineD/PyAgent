# prj037-tools-crdt-security — Project Overview

_Status: IN_PROGRESS_
_Owner: @1project | Updated: 2026-03-20_

## Project Identity
**Project ID:** prj037-tools-crdt-security
**Short name:** tools-crdt-security
**Project folder:** `docs/project/prj037-tools-crdt-security/`

## Project Overview
Security-hardened CRDT tools extension for the PyAgent swarm.  This project adds CRDT
(Conflict-free Replicated Data Type) support to the shared tools layer, tightens agent
workflow governance (branch isolation, project numbering policy, git-summary format
enforcement), and extends CI with CodeQL + policy tests.

## Goal & Scope
**Goal:** Deliver CRDT-backed shared state for swarm tools and enforce branch/project
governance policies across the agent workflow.
**In scope:**
- `src/core/crdt_bridge.py` and related CRDT tooling
- `.github/agents/` policy docs (0master, 1project, 9git)
- `docs/agents/` memory files
- `tests/docs/test_agent_workflow_policy_docs.py`
- Legacy git summary correction for prj005–prj008
**Out of scope:** New agent implementations, UI/web changes, Rust core changes.

## Branch Plan
**Expected branch:** `prj037-tools-crdt-security`
**Scope boundary:** `docs/project/prj037-tools-crdt-security/`, `.github/agents/`,
`docs/agents/`, `tests/docs/`, `src/core/crdt_bridge.py`, legacy git summaries for
prj005–prj008.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the
active branch matches `prj037-tools-crdt-security` and the changed files stay inside
the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting,
or ambiguous, return the task to `@0master` before downstream handoff.

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | CRDT bridge analysed | @2think | done |
| M2 | Design confirmed | @3design | done |
| M3 | Plan finalized | @4plan | done |
| M4 | Policy tests written | @5test | done |
| M5 | Code + policy docs implemented | @6code | done |
| M6 | Integration validated | @7exec | done |
| M7 | Security clean | @8ql | in progress |
| M8 | Committed | @9git | pending |

## Status
_Last updated: 2026-03-20_
Active — governance hardening (branch policy, prjNNN ownership, git-summary format)
complete.  Five policy tests passing.  Awaiting @9git narrow-stage commit.
