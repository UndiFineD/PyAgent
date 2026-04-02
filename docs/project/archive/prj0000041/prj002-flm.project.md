# flm - Project Overview

_Status: DONE_
_Owner: @9git | Updated: 2026-03-21_

**Project ID:** prj0000041

## Links

- Plan: plan.md
- Design: brainstorm.md

## Tasks

- [x] Define high-level goal, success criteria, and test plan.
- [x] Document FLM design and implementation details in `brainstorm.md`.
- [x] Ensure there is a clear list of FLM-related tasks and their completion status.
- [x] Keep project docs and implementation in sync with current CI/testing strategy.

## Status

4 of 4 tasks completed — DONE. FLM/Fastflow adapter and provider fully implemented.

## Code detection

- Code detected in:
  - `src/core/providers/FlmChatAdapter.py`
  - `src/core/providers/FlmProviderConfig.py`
  - `tests/test_flm_chat_adapter.py`
  - `tests/test_flm_provider_config.py`
  - `tests/test_flm_runtime_errors.py`
  - `tests/test_flm_tool_loop.py`

## Branch Plan

**Expected branch:** `prj0000041-flm`
**Scope boundary:** `docs/project/prj0000041/`, `src/core/providers/Flm*.py`, related FLM adapter and provider files.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR unless the active branch matches the expected branch above and changed files stay within the scope boundary.
