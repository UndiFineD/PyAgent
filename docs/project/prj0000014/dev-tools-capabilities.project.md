# dev-tools-capabilities — Project Overview

_Status: COMPLETE_
_Owner: @1project | Updated: 2026-03-22_

## Project Identity
**Project ID:** `prj0000014`
**Short name:** `dev-tools-capabilities`
**Project folder:** `docs/project/prj0000014`

## Project Overview
Implements the expanded capability toolkit under `src/tools/`: git helpers,
SSH/SCP remote operations, SSL certificate inspection, IP/CIDR calculators,
TCP connectivity tests, NGINX config validation, proxy testing, port forwarding,
port knocking, and a polyglot project bootstrapper.

## Goal & Scope
**Goal:** Provide working, CLI-accessible Python modules for every capability
listed in the dev-tools design, each with a `main()` entrypoint and unit tests.

**In scope:**
- `src/tools/git_utils.py` — git helpers: `create_feature_branch`, `update_changelog`, `changed_files`.
- `src/tools/remote.py` — SSH/SCP wrappers (no `shell=True`).
- `src/tools/ssl_utils.py` — TLS cert expiry and PEM verification.
- `src/tools/netcalc.py` — CIDR/IP address calculator.
- `src/tools/nettest.py` — async TCP connectivity tester.
- `src/tools/nginx.py` — NGINX config validator.
- `src/tools/proxy_test.py` — HTTP proxy connectivity test.
- `src/tools/port_forward.py` — async TCP port forwarder.
- `src/tools/knock.py` — port knocking client.
- `src/tools/boot.py` — polyglot project bootstrapper.
- `tests/tools/test_capabilities_modules.py` — import + API tests.
- `docs/tools.md` — capability catalog.

**Out of scope:** Production SSH daemon management, full Let's Encrypt ACME flow,
live network infrastructure changes.

## Branch Plan
**Expected branch:** `prj0000014-dev-tools-capabilities`
**Scope boundary:** `docs/project/prj0000014/`, `src/tools/` capability modules,
`tests/tools/test_capabilities_modules.py`.
**Handoff rule:** `@9git` stages `docs/project/prj0000014/` and code files, opens PR to `main`.
**Failure rule:** All `tests/tools/` must pass before merge; do not skip tests.
