# private-key-remediation - Project Overview

_Status: RELEASED_
_Owner: @9git | Updated: 2026-03-28_

## Project Identity
**Project ID:** prj0000090
**Short name:** private-key-remediation
**Project folder:** docs/project/prj0000090-private-key-remediation/

## Project Overview
Initialize the first implementation project from the prioritized idea queue to remediate committed private key
exposure and establish durable secret-scanning guardrails.

## Goal & Scope
**Goal:** Remove committed private key material from active repository state, rotate compromised credentials,
and prevent recurrence with automated secret scanning.

**In scope:**
- rust_core/2026-03-11-keys.priv and related key-handling documentation/remediation steps
- Secret scanning guardrails in commit workflow and CI configuration
- docs/project/prj0000090-private-key-remediation/**
- docs/project/kanban.md
- data/projects.json
- data/nextproject.md

**Out of scope:**
- Unrelated refactors in src/, backend/, web/, tests/, or rust_core/ beyond secret-remediation changes
- Feature work not directly tied to key exposure remediation

## Branch Plan
**Expected branch:** prj0000090-private-key-remediation
**Scope boundary:** rust_core/2026-03-11-keys.priv, secret-scan/pre-commit and CI guardrail files,
docs/project/prj0000090-private-key-remediation/**, docs/project/kanban.md, data/projects.json,
data/nextproject.md
**Handoff rule:** @9git must refuse staging, commit, push, or PR work unless the active branch matches this
project and changed files stay inside the scope boundary.
**Failure rule:** If project ID, branch plan, or scope boundary is missing, inherited, conflicting, or ambiguous,
return task to @0master before downstream handoff.

## Acceptance Criteria
- Project registration is created for prj0000090 in Discovery lane in both board and registry.
- Canonical project artifacts (.project/.think/.design/.plan/.test/.code/.exec/.ql/.git) exist in project folder.
- Branch isolation check is recorded with observed and expected branch values.
- Source idea linkage is captured and traceable from this project overview.

## Source Inputs
- docs/project/ideas/idea000001-private-key-in-repo.md

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
- Canonical options: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.think.md
- Canonical design: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.design.md
- Canonical plan: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.plan.md
- Validation/test log stub: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.test.md
- Code log stub: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.code.md
- Execution log stub: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.exec.md
- Security scan stub: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.ql.md
- Git summary stub: docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.git.md

## Branch Validation
- Observed branch at start: main
- Expected branch: prj0000090-private-key-remediation
- Resolution: switched to expected branch before artifact writes

## Status
_Last updated: 2026-03-28_
Project prj0000090 is complete and released. Implementation landed through PRs #233 and #234, and the project is now tracked in the Released lane in kanban and projects registry.
