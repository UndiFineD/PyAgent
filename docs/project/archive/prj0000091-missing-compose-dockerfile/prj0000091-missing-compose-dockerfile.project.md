# missing-compose-dockerfile - Project Overview

_Status: COMMITTED_LOCAL_
_Owner: @9git | Updated: 2026-03-28_

## Project Identity
**Project ID:** prj0000091
**Short name:** missing-compose-dockerfile
**Project folder:** docs/project/prj0000091-missing-compose-dockerfile/
**Source idea:** docs/project/ideas/idea000002-missing-compose-dockerfile.md

## Project Overview
Initialize the next queued idea as a governed project workstream to fix the broken Docker Compose reference to a non-existent Dockerfile and restore clean-checkout deploy reliability.

## Goal & Scope
**Goal:** Ensure compose-based deployment works on clean checkout by resolving the missing Dockerfile reference in deploy/compose.yaml with a validated, maintainable path.

**In scope:**
- deploy/compose.yaml and directly associated Dockerfile path resolution
- deploy/Dockerfile* additions or path corrections required for compose startup
- Validation updates needed to prevent regression of missing Dockerfile references
- docs/project/prj0000091-missing-compose-dockerfile/**
- docs/project/kanban.md
- data/projects.json
- data/nextproject.md

**Out of scope:**
- Broad deploy stack redesign unrelated to the missing Dockerfile reference
- Unrelated backend, web, src, or rust_core feature changes
- Non-essential CI refactors beyond checks required for this compose path fix

## Branch Plan
**Expected branch:** prj0000091-missing-compose-dockerfile
**Scope boundary:** deploy/compose.yaml, deploy/Dockerfile* files needed for path fix, targeted validation files for compose/Dockerfile reference checks, docs/project/prj0000091-missing-compose-dockerfile/**, docs/project/kanban.md, data/projects.json, data/nextproject.md
**Handoff rule:** @9git must refuse staging, commit, push, or PR work unless the active branch matches this project and changed files stay inside the scope boundary.
**Failure rule:** If project ID, branch plan, or scope boundary is missing, inherited, conflicting, or ambiguous, return task to @0master before downstream handoff.

## Acceptance Criteria
- Project is registered as prj0000091 in In Sprint in both docs/project/kanban.md and data/projects.json.
- Canonical project artifacts exist: .project, .think, .design, .plan, .test, .code, .exec, .ql, .git.
- Branch validation record includes observed and expected branch and confirms alignment before artifact writes.
- Source idea traceability to docs/project/ideas/idea000002-missing-compose-dockerfile.md is captured.
- Planned implementation scope explicitly covers fixing missing Dockerfile reference for deploy/compose.yaml and defining validation to prevent recurrence.

## Source Inputs
- docs/project/ideas/idea000002-missing-compose-dockerfile.md
- data/nextproject.md

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
- Canonical options: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.think.md
- Canonical design: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.design.md
- Canonical plan: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.plan.md
- Validation/test log stub: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.test.md
- Code log stub: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.code.md
- Execution log stub: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.exec.md
- Security scan stub: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.ql.md
- Git summary stub: docs/project/prj0000091-missing-compose-dockerfile/prj0000091-missing-compose-dockerfile.git.md

## Branch Validation
- Observed branch at start: main
- Expected branch: prj0000091-missing-compose-dockerfile
- Resolution: switched to expected branch before artifact writes

## Status
_Last updated: 2026-03-28_
@8ql quality/security gate completed. Branch validation passed, scoped acceptance tests passed (`2 passed`), workflow-injection review was not applicable (no workflow file changes), and dependency baseline reported zero CVEs. Non-blocking advisories were recorded for container hardening (`deploy/Dockerfile.pyagent` runtime user not set to non-root) and mutable image tagging (`ollama:latest`).

@9git completed local commit reconciliation. Project change commit recorded as `8f4cb82b3` (`chore(deploy): fix compose dockerfile reference`). Project is now in terminal pre-PR state (`COMMITTED_LOCAL`); pull request has not been opened yet.
