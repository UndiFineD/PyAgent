# plugin-marketplace-browser — Think / Analysis
_Owner: @2think | Status: DONE_

## Problem Statement

NebulaOS requires a plugin marketplace panel so users can browse available
agent plugins, view metadata (name, description, author, version, tags), and
toggle install/uninstall state. No real install logic is needed in V1 — the
goal is the browsing UX and backend registry contract.

## Backend Options

| Option | Pros | Cons |
|---|---|---|
| Static route in app.py (no auth) | Simple, public, fast, cache-friendly | No per-user install state |
| Protected route via _auth_router | Consistent with other API routes | Unnecessary auth for read-only public data |
| Separate microservice | Scalable | Massive over-engineering for a static list |

**Decision:** Static `GET /api/plugins` on `app` directly (not `_auth_router`), returning a hardcoded `PLUGIN_REGISTRY` list. Auth is not needed — plugin discovery is public information.

## Frontend Options

| Option | Pros | Cons |
|---|---|---|
| New NebulaOS panel app (WindowState) | Consistent with existing pattern | — |
| Embedded in existing app | Less work | Bad UX, breaks OS metaphor |

**Decision:** New `PluginMarketplace` panel app following the existing pattern (Calculator, CodeBuilder, ProjectManager, etc.).

## Data Model

Each plugin entry:
- `id`: unique string slug
- `name`: human-readable name
- `description`: one-line description
- `author`: attribution string
- `version`: semver string
- `tags`: string array
- `installed`: boolean (local UI state only in V1)

## UX Considerations
- Search/filter input at top filters by name, description, tags
- Cards in a responsive grid
- Install toggle changes local React state (no real install)
- Loading and error states for the fetch
