# dev-tools-autonomy — Project Overview

_Status: COMPLETE_
_Owner: @1project | Updated: 2026-03-22_

## Project Identity
**Project ID:** `prj0000013`
**Short name:** `dev-tools-autonomy`
**Project folder:** `docs/project/prj0000013`

## Project Overview
Builds the self-improving development tools scaffolding: dependency auditor,
code-metrics collector, plugin framework, and self-healing helper. Establishes
TDD tests and extends the setup helper to ensure necessary files and directories
exist on fresh checkouts.

## Goal & Scope
**Goal:** Implement `src/tools/dependency_audit.py`, `src/tools/metrics.py`,
`src/tools/self_heal.py`, and a plugin loader; each with pytest coverage.

**In scope:**
- `src/tools/dependency_audit.py` — dependency audit API.
- `src/tools/metrics.py` — code metrics collector.
- `src/tools/self_heal.py` — self-healing utility helper.
- `src/tools/plugin_loader.py` — plugin discovery and loading.
- `tests/tools/` — TDD tests for each module.
- Extension of `scripts/setup_structure.py` for new directories.

**Out of scope:** Full autonomous self-healing runtime, AI-driven code rewriting,
production telemetry pipelines.

## Branch Plan
**Expected branch:** `prj0000013-dev-tools-autonomy`
**Scope boundary:** `docs/project/prj0000013/`. Implementation files exist in
`src/tools/` and `tests/tools/` on `main`.
**Handoff rule:** `@9git` stages `docs/project/prj0000013/` only.
**Failure rule:** If CI fails, fix before merging; do not skip tests.
