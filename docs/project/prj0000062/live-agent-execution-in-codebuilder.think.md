# live-agent-execution-in-codebuilder — Think / Analysis
_Owner: @2think | Status: DONE_

## Problem Statement

CodeBuilder currently has a "Run/Stop" workflow simulation that steps through agents
locally using timeouts. There is no real backend execution — agent progress is purely
cosmetic. We need a way to start a real (or demo) pipeline run from the UI, track its
status per-stage, and display progress to the user.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| SSE streaming | Real-time, low overhead | Requires SSE infrastructure, CORS complexity |
| WebSocket pipeline channel | Bidirectional, existing WS infra | Requires new message types, stateful routing |
| REST polling (POST run + GET status) | Simple, stateless, easy to test | 2s polling latency, slightly more requests |
| gRPC streaming | High performance | Requires gRPC gateway, large dependency |

## Decision: REST Polling

- POST `/api/pipeline/run` returns a `pipeline_id` immediately (async-friendly)
- GET `/api/pipeline/status/{pipeline_id}` returns current stage states
- Client polls every 2 seconds — acceptable latency for a demonstration workflow
- Easiest to test with `httpx`/`TestClient` (no WS harness needed)
- In-memory store (`_pipelines` dict) is sufficient for demo purposes
- Zero new dependencies

## Security Notes

- `_pipelines` is module-level in-memory — resets on server restart (expected for demo)
- Both endpoints protected by `_auth_router` (requires `require_auth` dependency)
- `pipeline_id` is a UUID4 — unguessable, safe for use as a route parameter
- No file I/O, no subprocess — no injection surface

## UI Design Decision

- Add "Run Pipeline" button to the existing right-pinned toolbar group
- Show status panel only when a `pipelineId` is active (lazy render)
- Stage status indicators: ⚪ pending / 🔵 running / ✅ done / ❌ error
- Polling starts on pipeline launch, stops when status ≠ "running"
