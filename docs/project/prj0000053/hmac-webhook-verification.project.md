# hmac-webhook-verification — Project Overview

_Status: IN_SPRINT_
_Owner: @1project | Updated: 2026-03-24_

## Project Identity

**Project ID:** prj0000053
**Short name:** hmac-webhook-verification
**Project folder:** `docs/project/prj0000053/`
**Branch:** `prj0000053-hmac-webhook-verification`
**Date:** 2026-03-24

## Branch Plan

**Expected branch:** `prj0000053-hmac-webhook-verification`
**Observed branch:** `prj0000053-hmac-webhook-verification`
**Project match:** YES

## Project Overview

Wire HMAC-SHA256 signature verification into `src/github_app.py` so that every
incoming GitHub webhook request is authenticated before being processed.

GitHub signs every webhook payload using a shared secret configured in the repository
settings. The `X-Hub-Signature-256` header carries the signature as `sha256=<hex>`.
This project adds a `verify_github_signature()` helper function and gates the
`POST /webhook` endpoint so that unsigned or incorrectly-signed requests are rejected
with HTTP 401 before any event handler runs.

## Goal & Scope

**Goal:** Prevent spoofed or tampered GitHub webhook payloads from being processed
by PyAgent.

**In scope:**
- `src/github_app.py` — add `verify_github_signature()` + enforce it in `/webhook`
- `tests/test_github_app.py` — add HMAC-specific tests (valid, invalid, missing, timing)
- `data/projects.json` — update lane + branch for prj0000053
- `docs/project/kanban.md` — move prj0000053 from Ideas → In Sprint

**Out of scope:**
- Key rotation UI
- Storing or rotating the secret itself
- Changes to other endpoints or agents

## Acceptance Criteria

1. `verify_github_signature(secret, body, header)` returns `True` for a valid signature.
2. Returns `False` if `header` is `None`, malformed, or wrong.
3. Uses `hmac.compare_digest` (timing-safe).
4. `POST /webhook` returns HTTP 401 when `GITHUB_WEBHOOK_SECRET` is set and the
   signature is missing or invalid.
5. `POST /webhook` passes through unchanged when `GITHUB_WEBHOOK_SECRET` is not set
   (backward-compatible dev mode).
6. All existing tests continue to pass.
7. New test coverage ≥ 6 cases for HMAC logic.
