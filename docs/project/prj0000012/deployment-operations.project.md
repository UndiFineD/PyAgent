# deployment-operations — Project Overview

_Status: COMPLETE_
_Owner: @1project | Updated: 2026-03-22_

## Project Identity
**Project ID:** `prj0000012`
**Short name:** `deployment-operations`
**Project folder:** `docs/project/prj0000012`

## Project Overview
Bootstraps CI/CD workflow, deployment directory hierarchy, and verification
tests so the repository has a verifiable, reproducible deployment skeleton.
The primary deliverable is `scripts/setup_deployment.py` and its companion tests.

## Goal & Scope
**Goal:** Implement CI/CD workflow skeleton, deployment folder hierarchy, and
pytest-verified structure tests.

**In scope:**
- `scripts/setup_deployment.py` — creates `Deployment/` hierarchy.
- `.github/workflows/ci.yml` — GitHub Actions CI workflow.
- `tests/structure/test_deployment_dirs.py` — verifies deployment dirs exist.
- `tests/ci/` — CI workflow validation tests.

**Out of scope:** Production infrastructure provisioning, cloud deployments,
Docker image builds, runtime secrets management.

## Branch Plan
**Expected branch:** `prj0000012-deployment-operations`
**Scope boundary:** All changes under `docs/project/prj0000012/`. Implementation
files (`scripts/setup_deployment.py`, `.github/workflows/`, `tests/structure/`,
`tests/ci/`) were merged to `main` in prior work and are not re-staged here.
**Handoff rule:** `@9git` stages `docs/project/prj0000012/` only and opens PR
targeting `main`.
**Failure rule:** If CI fails on this branch, fix before merging; do not force-push
`main`.

