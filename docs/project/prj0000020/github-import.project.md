# github-import — Project Overview

## Project Identity
**Project ID:** prj0000020
**Short name:** github-import
**Project folder:** `docs/project/prj0000020/`

## Project Overview
Extends the GitHub App webhook receiver with real event routing (push, pull_request, issues, ping) and a health endpoint. Upgrades the importer's `downloader.py` from a placeholder to a real `git clone` wrapper.

## Goal & Scope
**Goal:** Make the GitHub integration and importer functional beyond stubs — handle real webhook events and clone real repositories.

**In scope:**
- `src/github_app.py` — event routing, `/health` endpoint, typed JSON responses
- `src/importer/downloader.py` — real `clone_repo()` using subprocess git
- `src/importer/config.py` — copyright header
- `tests/test_github_app.py` — 7 tests for all event types
- `tests/test_importer_flow.py` — fix size==0 assertion
- `docs/project/prj0000020/` — 9 doc artifacts

**Out of scope:**
- GitHub App authentication (HMAC signature verification) — future work
- Real network calls in tests

## Branch Plan
**Expected branch:** `prj0000020-github-import`
**Scope boundary:** `src/github_app.py`, `src/importer/downloader.py`, `src/importer/config.py`, `tests/test_github_app.py`, `tests/test_importer_flow.py`, `docs/project/prj0000020/`
**Handoff rule:** merge after 9 tests pass
**Failure rule:** if branch mismatch, STOP


_No checkbox tasks found in the plan file._

## Status

0 of 0 tasks completed

## Code detection

- Code detected in:
  - `src\github_app.py`
  - `tests\runtime\test_runtime_import.py`
  - `tests\test_github_app.py`
  - `tests\test_import_config.py`
  - `tests\test_importer_config.py`
  - `tests\test_importer_flow.py`

## Milestones
Legacy milestone details are not specified in this historical document.

