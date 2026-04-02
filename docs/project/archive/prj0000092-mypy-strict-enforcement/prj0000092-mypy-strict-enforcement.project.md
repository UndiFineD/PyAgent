# mypy-strict-enforcement - Project Overview

_Status: READY_FOR_9GIT_
_Owner: @8ql | Updated: 2026-03-28_

## Project Identity
**Project ID:** prj0000092
**Short name:** mypy-strict-enforcement
**Project folder:** docs/project/prj0000092-mypy-strict-enforcement/
**Source idea:** docs/project/ideas/idea000003-mypy-strict-enforcement.md

## Project Overview
Initialize the next queued idea as a governed project workstream to progressively enforce mypy strictness, starting in src/core, with deterministic guardrails that prevent type-safety regressions.

## Goal & Scope
**Goal:** Introduce a progressive, low-risk mypy strictness rollout beginning with src/core so typed contracts become enforced rather than decorative while preserving delivery stability.

**In scope:**
- Type-checking strategy and guardrail design for progressive strictness in src/core/**
- Deterministic CI/validation guardrails for strictness progression and non-regression
- Definition of phase boundaries, error budgets, and rollback criteria for strictness adoption
- docs/project/prj0000092-mypy-strict-enforcement/**
- docs/project/kanban.md
- data/projects.json
- data/nextproject.md

**Out of scope:**
- Full-repo strict mode activation in a single change
- Unrelated refactors outside strictness rollout requirements
- New runtime features not directly tied to mypy strict-enforcement governance

## Branch Plan
**Expected branch:** prj0000092-mypy-strict-enforcement
**Scope boundary:** src/core/** (for progressive strictness rollout design/implementation in downstream phases), mypy.ini and targeted type-check validation config/test files required for deterministic guardrails, docs/project/prj0000092-mypy-strict-enforcement/**, docs/project/kanban.md, data/projects.json, data/nextproject.md
**Handoff rule:** @9git must refuse staging, commit, push, or PR work unless the active branch matches this project and changed files stay inside the scope boundary.
**Failure rule:** If project ID, branch plan, or scope boundary is missing, inherited, conflicting, or ambiguous, return task to @0master before downstream handoff.

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

## Artifacts
- Canonical options: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.think.md
- Canonical design: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.design.md
- Canonical plan: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.plan.md
- Validation/test log stub: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.test.md
- Code log stub: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.code.md
- Execution log stub: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.exec.md
- Security scan stub: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.ql.md
- Git summary stub: docs/project/prj0000092-mypy-strict-enforcement/prj0000092-mypy-strict-enforcement.git.md

## Branch Validation
- Observed branch at start: main
- Expected branch: prj0000092-mypy-strict-enforcement
- Resolution: switched to expected branch before artifact writes

## Status
_Last updated: 2026-03-28_
@8ql completed quality and security gate review for scoped project files.
Gate results are PASS for branch validation, workflow-injection checks, plan-vs-delivery, AC-vs-test coverage, and docs alignment.
`pip-audit` surfaced 1 MEDIUM + 2 LOW dependency advisories (project-external security debt, tracked non-blocking).
@9git validated branch/scope gates, refreshed project dashboard, and prepared narrow-scope commit packaging.
Project status: COMMITTED_LOCAL.
