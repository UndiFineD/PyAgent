# ci-security-quality-workflow-consolidation - Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-04-02_

## Project Identity
**Project ID:** prj0000115
**Short name:** ci-security-quality-workflow-consolidation
**Project folder:** `docs/project/prj0000115-ci-security-quality-workflow-consolidation/`

## Project Overview
Initialize discovery artifacts for consolidating CI/security/quality enforcement into a pre-commit-first workflow with minimal verification-only GitHub workflows.

## Goal & Scope
**Goal:** Establish canonical governance artifacts and registry state for project prj0000115 so discovery can begin on idea000131.
**In scope:** Canonical project artifacts under `docs/project/prj0000115-ci-security-quality-workflow-consolidation/`; registry synchronization in `docs/project/kanban.json`, `data/projects.json`, and `data/nextproject.md`; idea mapping update in `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md`.
**Out of scope:** Implementation edits to `.pre-commit-config.yaml`, `.github/workflows/**`, `src/**`, and `scripts/**`.

## Branch Plan
**Expected branch:** prj0000115-ci-security-quality-workflow-consolidation
**Observed branch:** prj0000115-ci-security-quality-workflow-consolidation
**Project match:** PASS
**Scope boundary:** `docs/project/prj0000115-ci-security-quality-workflow-consolidation/**`, `docs/project/kanban.json`, `data/projects.json`, `data/nextproject.md`, `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md`
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch remains `prj0000115-ci-security-quality-workflow-consolidation` and changed files stay inside the declared scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous, return the task to `@0master` before downstream handoff.

## Branch Validation
| Check | Result | Notes |
|---|---|---|
| Expected branch recorded in project overview | PASS | Recorded in this Branch Plan section. |
| Observed branch matches project | PASS | `git branch --show-current` returned `prj0000115-ci-security-quality-workflow-consolidation`. |
| No inherited branch from another `prjNNNNNNN` | PASS | Branch prefix and short name match the assigned project boundary. |

## Scope Validation
| File or scope | Result | Notes |
|---|---|---|
| `docs/project/prj0000115-ci-security-quality-workflow-consolidation/**` | PASS | Canonical artifact folder for this project. |
| `docs/project/kanban.json` | PASS | Added prj0000115 in Discovery with `idea000131` tag and synchronized via governance script. |
| `data/projects.json` | PASS | Added matching Discovery entry for prj0000115. |
| `data/nextproject.md` | PASS | Advanced from `prj0000115` to `prj0000116`. |
| `docs/project/ideas/idea000131-ci-security-quality-workflow-consolidation.md` | PASS | Planned mapping now set to `prj0000115`. |

## Failure Disposition
Docs policy test selector is currently blocked by a pre-existing missing legacy file (`docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`) unrelated to this project scope.

## Canonical Artifacts
- `ci-security-quality-workflow-consolidation.think.md`
- `ci-security-quality-workflow-consolidation.design.md`
- `ci-security-quality-workflow-consolidation.plan.md`
- `ci-security-quality-workflow-consolidation.test.md`
- `ci-security-quality-workflow-consolidation.code.md`
- `ci-security-quality-workflow-consolidation.exec.md`
- `ci-security-quality-workflow-consolidation.ql.md`
- `ci-security-quality-workflow-consolidation.git.md`

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Discovery initialized | @1project | DONE |
| M2 | Design and plan completed | @3design/@4plan | NOT_STARTED |
| M3 | Implementation complete | @6code | NOT_STARTED |
| M4 | Validation complete | @7exec/@8ql | NOT_STARTED |
| M5 | Released | @9git | NOT_STARTED |

## Status
_Last updated: 2026-04-02_
Project branch and canonical artifacts initialized; registry and idea mappings synchronized for Discovery handoff; governance registry validation passed; docs policy selector reported one pre-existing failure outside this scope.
