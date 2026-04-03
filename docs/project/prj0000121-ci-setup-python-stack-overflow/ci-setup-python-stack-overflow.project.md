# ci-setup-python-stack-overflow - Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-04-03_

## Project Identity
**Project ID:** prj0000121
**Short name:** ci-setup-python-stack-overflow
**Project folder:** docs/project/prj0000121-ci-setup-python-stack-overflow/

## Project Overview
Initialize a post-merge hotfix project boundary for the CI regression observed after PR #280 where CI / Lightweight fails in actions/setup-python@v5 with the error 'Maximum call stack size exceeded'.

## Goal & Scope
**Goal:** Establish governance-compliant project artifacts and registry state so downstream agents can execute the CI hotfix safely.
**In scope:** Canonical project artifacts, Discovery lane registry entries, next-project counter advancement, governance validation evidence, and branch-scoped initialization commit.
**Out of scope:** Idea mapping updates, implementation of the setup-python hotfix itself, and non-project registry refactors.

## Branch Plan
**Expected branch:** prj0000121-ci-setup-python-stack-overflow
**Scope boundary:** docs/project/prj0000121-ci-setup-python-stack-overflow/, docs/project/kanban.json, data/projects.json, data/nextproject.md, .github/agents/data/current.1project.memory.md, .github/agents/data/history.1project.memory.md, .github/agents/data/2026-04-03.1project.log.md, and coordinator-approved pre-existing .github/agents/data/2026-04-03.0master.log.md + .github/agents/data/current.0master.memory.md if included by commit flow.
**Handoff rule:** @9git must refuse staging, commit, push, or PR work unless the active branch matches this project and staged files remain inside the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous, return the task to @0master before downstream handoff.

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
Boundary initialization complete on branch prj0000121-ci-setup-python-stack-overflow. Canonical artifacts, Discovery registration, nextproject advancement, and governance validations are complete and ready for downstream discovery.
