# projectmanager-ideas-autosync - Project Overview

_Status: BLOCKED_AT_9GIT_
_Owner: @1project | Updated: 2026-03-28_

## Project Identity
**Project ID:** prj0000093
**Short name:** projectmanager-ideas-autosync
**Project folder:** `docs/project/prj0000093-projectmanager-ideas-autosync/`

## Project Overview
Enable Project Manager to automatically ingest idea files from docs/project/ideas and keep the board focused by excluding ideas that are already implemented as active or released projects.

## Goal & Scope
**Goal:** Project Manager automatically reads docs/project/ideas and excludes implemented ideas.
**In scope:** Backend ideas API enhancements, frontend Project Manager integration to render filtered ideas, tests for filtering and ingestion behavior, project registry/kanban alignment.
**Out of scope:** Rewriting historical idea files, changing lane governance policy, altering unrelated dashboard views.

## Branch Plan
**Expected branch:** prj0000093-projectmanager-ideas-autosync
**Scope boundary:** docs/project/prj0000093-projectmanager-ideas-autosync/, docs/project/kanban.md, data/projects.json, data/nextproject.md, backend ideas/project listing APIs, frontend Project Manager ideas integration, and related tests.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch matches this project and changed files stay inside the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous, return the task to `@0master` before downstream handoff.

## Canonical Artifacts
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.project.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.think.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.design.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.plan.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.test.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.code.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.exec.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.ql.md`
- `docs/project/prj0000093-projectmanager-ideas-autosync/projectmanager-ideas-autosync.git.md`

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
| M8 | Committed | @9git | BLOCKED |

## Status
_Last updated: 2026-03-28_
@8ql completed scoped quality/security review for backend ideas API, frontend ProjectManager integration, and project artifacts. No HIGH/CRITICAL security findings were detected (gate clear). @9git branch/scope gates passed and narrow staging was prepared, but mandatory post-staging pre-commit failed on repository-wide `ruff check src tests` baseline violations outside project scope; commit/push/PR is blocked pending @0master remediation direction.
