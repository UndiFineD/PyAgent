# websocket-e2e-encryption — Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000055
**Short name:** websocket-e2e-encryption
**Project folder:** `docs/project/prj0000055/`
**Branch:** `prj0000055-websocket-e2e-encryption`
**Date:** 2026-03-25

## Project Overview

Wire an E2E encryption layer into the WebSocket transport. Each session performs
an X25519 ECDH key exchange, then messages are encrypted AES-256-GCM using the
derived session key. Server sends its public key as the first WebSocket message;
client sends its public key back; both derive the shared secret; all subsequent
messages are encrypted.

## Goal & Scope

**Goal:** Wire X25519 ECDH key exchange and AES-256-GCM message encryption into
the WebSocket transport, providing per-session forward secrecy for all WebSocket
communications.

**In scope:**
- `backend/ws_crypto.py` — NEW: X25519 key generation, ECDH, AES-256-GCM encrypt/decrypt
- `backend/app.py` — MODIFY: WebSocket endpoint performs key exchange before any message handling
- `tests/test_ws_crypto.py` — NEW: unit tests for ws_crypto (5 tests)
- `tests/test_backend_worker.py` — UPDATE: WS tests updated to perform E2E handshake
- `backend/requirements.txt` — add `cryptography>=41.0.0`
- `docs/project/prj0000055/` — 9 project artifacts
- `data/projects.json` — update prj0000055 lane to "Review"
- `docs/project/kanban.md` — move prj0000055 to Review table

**Out of scope:** Frontend-side decryption (future project), certificate pinning, key rotation

## Branch Plan

**Expected branch:** `prj0000055-websocket-e2e-encryption`
**Scope boundary:**
  - `docs/project/prj0000055/` — all project artifacts
  - `backend/ws_crypto.py` — new crypto primitives module
  - `backend/app.py` — WebSocket handler E2E encryption wiring only
  - `tests/test_ws_crypto.py` — new test file
  - `tests/test_backend_worker.py` — WS test helpers updated
  - `data/projects.json` — lane + pr update
  - `docs/project/kanban.md` — lane row update
**Handoff rule:** All tests pass, PR open → hand to reviewer
**Failure rule:** If tests fail, stop and report. Do not push broken code.
