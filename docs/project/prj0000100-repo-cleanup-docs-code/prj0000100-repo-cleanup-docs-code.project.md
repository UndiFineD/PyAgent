# prj0000100-repo-cleanup-docs-code - Project Overview

_Status: REVIEW_
_Owner: @1project | Updated: 2026-03-29_

## Project Identity
**Project ID:** prj0000100
**Short name:** repo-cleanup-docs-code
**Project folder:** `docs/project/prj0000100-repo-cleanup-docs-code/`

## Project Overview
Repository-wide cleanup initiative focused on reviewing and improving non-dot files, updating documentation quality and consistency, cleaning code hygiene issues, and introducing durable governance artifacts for code structure indexing and internet search policy controls for agents in `.github/agents/data/allowed_websites.md`.

## Goal & Scope
**Goal:** Improve repository maintainability and agent execution safety via coordinated docs/code cleanup and governance updates.
**In scope:**
- review and cleanup all non-dot files where practical under project scope
- update documentation for lifecycle/process clarity
- code cleanup and structure hygiene updates
- add code structure index tracking (`.github/agents/data/codestructure.md`)
- add allowed websites policy (`.github/agents/data/allowed_websites.md`) and align agent guidance
**Out of scope:**
- destructive history rewrites or broad refactors not required for cleanup goals
- unrelated feature development

## Acceptance Criteria
- AC-01: Canonical lifecycle artifacts exist under this project folder and follow required section templates.
- AC-02: Project tracking is updated consistently in `docs/project/kanban.md`, `data/projects.json`, and `data/nextproject.md`.
- AC-03: `codestructure.md` exists with required schema (`| file | line | code |`) and seeded entries anchored to real code locations.
- AC-04: `.github/agents/data/allowed_websites.md` exists and includes explicit allowed domains including `wikipedia.org` and `github.com`.
- AC-05: Agent guidance is updated to prefer local search first and internet fetch/search only for domains listed in `.github/agents/data/allowed_websites.md`.

## Branch Plan
**Expected branch:** prj0000100-repo-cleanup-docs-code
**Scope boundary:** `docs/project/prj0000100-repo-cleanup-docs-code/`, `docs/project/kanban.md`, `data/projects.json`, `data/nextproject.md`, `.github/agents/data/codestructure.md`, `.github/agents/data/allowed_websites.md`, and focused agent guidance updates.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch matches this project and changed files remain inside the scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous, return the task to `@0master` before downstream handoff.

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
| M8 | Committed | @9git | DONE |

## Status
_Last updated: 2026-03-29_
Focused governance quality/security review completed by @8ql with no blocking findings for project scope; residual risk for non-scoped full-repo checks is documented in the QL artifact.
