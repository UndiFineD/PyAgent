# api-versioning — Project Overview

_Owner: @1project | Status: In Sprint_

**Goal:** Add versioned API routing (`/api/v1/`) so that future breaking changes can be introduced without disrupting existing clients.

**In scope:**
- `backend/app.py` — wrap existing `_auth_router` routes under `/api/v1/` prefix; keep bare `/api/` as deprecated aliases returning `Deprecation` response header
- `tests/test_api_versioning.py` — tests
- `docs/project/prj0000066/` — 9 artifacts
- `data/projects.json` + `docs/project/kanban.md` — lane transitions

**Out of scope:** Actual schema changes, content negotiation, OpenAPI multi-version docs.

## Branch Plan

**Expected branch:** `prj0000066-api-versioning`

**Scope boundary:** Only `backend/app.py`, `tests/test_api_versioning.py`, and the 9 artifacts may be modified on this branch.

**Handoff rule:** `@9git` must confirm `OBSERVED_BRANCH == prj0000066-api-versioning` before staging.

**Failure rule:** If tests fail or branch mismatch is detected, stop and notify `@0master`.
