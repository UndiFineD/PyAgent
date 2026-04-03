# amd-npu-feature-documentation - Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-04-03_

## Project Identity
**Project ID:** prj0000118
**Short name:** amd-npu-feature-documentation
**Project folder:** `docs/project/prj0000118-amd-npu-feature-documentation/`

## Project Overview
Initialize the project boundary and governance artifacts for documenting the `amd_npu` feature so discovery can define activation guidance, validation expectations, and rollout constraints without changing implementation code yet.

## Goal & Scope
**Goal:** Establish canonical governance artifacts and registry state for project prj0000118 so discovery can begin on idea000020.
**In scope:** Canonical project artifacts under `docs/project/prj0000118-amd-npu-feature-documentation/`; registry synchronization in `docs/project/kanban.json`, `data/projects.json`, and `data/nextproject.md`; idea mapping update in `docs/project/ideas/idea000020-amd-npu-feature-documentation.md`; `@1project` memory and daily log updates.
**Out of scope:** Edits to `Cargo.toml`, `rust_core/**`, CI workflows, or source/test files outside project-governance artifacts.

## Branch Plan
**Expected branch:** prj0000118-amd-npu-feature-documentation
**Observed branch:** prj0000118-amd-npu-feature-documentation
**Project match:** PASS
**Scope boundary:** `docs/project/prj0000118-amd-npu-feature-documentation/**`, `docs/project/kanban.json`, `data/projects.json`, `data/nextproject.md`, `docs/project/ideas/idea000020-amd-npu-feature-documentation.md`, `.github/agents/data/current.1project.memory.md`, `.github/agents/data/2026-04-03.1project.log.md`
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the active branch remains `prj0000118-amd-npu-feature-documentation` and changed files stay inside the declared scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting, or ambiguous, return the task to `@0master` before downstream handoff.

## Branch Validation
| Check | Result | Notes |
|---|---|---|
| Expected branch recorded in project overview | PASS | Recorded in this Branch Plan section. |
| Observed branch matches project | PASS | `git branch --show-current` returned `prj0000118-amd-npu-feature-documentation`. |
| No inherited branch from another `prjNNNNNNN` | PASS | Branch prefix and short name match the assigned project boundary. |

## Scope Validation
| File or scope | Result | Notes |
|---|---|---|
| `docs/project/prj0000118-amd-npu-feature-documentation/**` | PASS | Canonical artifact folder created with all nine required artifacts. |
| `docs/project/kanban.json` | PASS | Added prj0000118 in Discovery and normalized lane via governance script. |
| `data/projects.json` | PASS | Added matching Discovery entry for prj0000118. |
| `data/nextproject.md` | PASS | Advanced from `prj0000118` to `prj0000119`. |
| `docs/project/ideas/idea000020-amd-npu-feature-documentation.md` | PASS | Planned mapping now set to `prj0000118`. |
| `.github/agents/data/current.1project.memory.md` | PASS | Current task note recorded with blocked disposition. |
| `.github/agents/data/2026-04-03.1project.log.md` | PASS | Daily interaction log updated with this initialization attempt. |

## Failure Disposition
None. Blocker remediation updated the inherited `prj0000117` git summary to use the required `## Scope Validation` header. The exact docs-policy selector now fails only on the accepted legacy baseline missing file `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`.

## Canonical Artifacts
- `amd-npu-feature-documentation.think.md`
- `amd-npu-feature-documentation.design.md`
- `amd-npu-feature-documentation.plan.md`
- `amd-npu-feature-documentation.test.md`
- `amd-npu-feature-documentation.code.md`
- `amd-npu-feature-documentation.exec.md`
- `amd-npu-feature-documentation.ql.md`
- `amd-npu-feature-documentation.git.md`

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Discovery initialized | @1project | BLOCKED |
| M2 | Options explored | @2think | NOT_STARTED |
| M3 | Design confirmed | @3design | NOT_STARTED |
| M4 | Plan finalized | @4plan | NOT_STARTED |
| M5 | Tests written | @5test | NOT_STARTED |
| M6 | Code implemented | @6code | NOT_STARTED |
| M7 | Integration validated | @7exec | NOT_STARTED |
| M8 | Security clean | @8ql | NOT_STARTED |
| M9 | Committed | @9git | BLOCKED |

## Status
_Last updated: 2026-04-03_
Branch gate passed on `prj0000118-amd-npu-feature-documentation`, blocker remediation was applied in the authorized expanded scope for `prj0000117`, and the exact required validations were rerun. Registry validation returned `VALIDATION_OK` with `projects=117`; docs-policy now reports only the accepted legacy `prj0000005` missing summary baseline, so initialization is clear for scoped commit and push.