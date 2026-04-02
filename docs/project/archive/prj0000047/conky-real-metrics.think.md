# conky-real-metrics — Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-23_

---

## Root Cause Analysis

`web/apps/Conky.tsx` contains only a `Math.random()` simulation loop inside `setInterval`.
No network call is made; the backend is never consulted.  The backend (`backend/app.py`) does
**not** have a metrics endpoint.  `psutil 7.2.2` is installed in `.venv` but unused by the
backend.  The Vite proxy already forwards `/api/*` to FastAPI on port 444, so the transport
layer for a REST approach already exists.

Key structural facts:
- `setInterval` runs every **1 s**; data flows through `setData` → `setStats`.
- The component tracks: `cpu %`, `mem %`, `netUp KB/s`, `netDown KB/s`, `diskRead`, `diskWrite`,
  `tokens`.
- Existing WS endpoint at `/ws` is used for agent chat, not metrics.
- `vite-agent-docs` Vite middleware is the only dev-server plugin pattern in the codebase.
- `psutil.net_io_counters()` returns **cumulative** bytes; KB/s requires a two-sample differential,
  meaning the backend must hold state between calls (or sleep between samples).

---

## Options

### Option A — REST Polling: `GET /api/metrics/system` in FastAPI  ✅ RECOMMENDED

**Approach:**
Add a single FastAPI route `GET /api/metrics/system` to `backend/app.py` that:
1. Calls `psutil.cpu_percent(interval=None)` (non-blocking, uses previous sample).
2. Calls `psutil.virtual_memory()` for `used_mb` / `total_mb`.
3. Calls `psutil.net_io_counters(pernic=True)` and diffs against a module-level snapshot
   stored from the previous call to compute KB/s per interface.

Frontend replaces the `setInterval` body with `fetch('/api/metrics/system')` at the same cadence.

**Pros:**
- The `/api` proxy is **already wired** in both `vite.config.ts` and `backend/app.py`.
- One new endpoint (`~30 lines`) is the only backend change.
- HTTP/REST is stateless, curl-testable, easy to mock in tests.
- At 1–2 s poll intervals on localhost, HTTP overhead is negligible.
- psutil module-level state for differential network counters is idiomatic and safe for
  a single-worker FastAPI process.
- Acceptance criteria JSON shape (`cpu_percent`, `memory_used_mb`, `memory_total_mb`,
  `network[{interface, tx_kbps, rx_kbps}]`) maps directly to one pydantic model.

**Cons:**
- Backend must be running for the widget to show real data (but this is an intended
  design constraint, not a bug).
- First call returns `0 KB/s` for network (no prior sample) — needs graceful handling
  (return zeroes on first call, valid values thereafter).

**Network KB/s implementation note:**
```python
# Module-level state in app.py
_prev_net: dict[str, tuple[int,int]] = {}
_prev_net_ts: float = 0.0
```
On each call, compute bytes difference / elapsed time.  This is safe for development
(single Uvicorn worker); for multi-worker prod deployments (out of scope), shared state
would need Redis or a side-car — but that is explicitly out of scope.

---

### Option B — WebSocket Push via existing `/ws`

**Approach:**
Extend `ws_handler.py` to accept a `{"type": "metrics/subscribe"}` message.
Add a server-side asyncio background task that pushes a `{"type": "metrics/snapshot", ...}`
frame to subscribed clients every 1 s.

**Pros:**
- True server-push (no repeated HTTP connections).
- Single persistent connection; marginally lower overhead at high poll rates.

**Cons:**
- The `/ws` endpoint is shared with agent-chat traffic.  Mixing system metrics into the
  chat message bus couples two unrelated concerns.
- Requires adding subscription management to `ws_handler.py` and `session_manager.py` —
  significant complexity vs. a 30-line HTTP endpoint.
- Reconnection logic must be added to the component (WebSocket drops lose the subscription).
- If the backend is not running the WS connection fails entirely; the HTTP polling option
  fails gracefully (returns an error, component can show stale / zero values).
- Over-engineered for a 1–2 s update rate over localhost.

---

### Option C — Vite Dev-Only Middleware (Node.js subprocess callout)

**Approach:**
Add a second Vite plugin in `vite.config.ts` mirroring `vite-agent-docs`.  The middleware
intercepts `GET /api/metrics/system` and spawns `python -c "import psutil; ..."` to collect
metrics, returning the JSON response.

**Pros:**
- Works in dev without the FastAPI backend running (offline mode).
- No backend changes required.
- Extends the established `vite-agent-docs` plugin pattern.

**Cons:**
- **Only works in Vite dev mode** — production build has no Vite server.
- Spawning a new Python process per 1 s poll is expensive (~100–300 ms startup overhead)
  and prevents correct differential network counters (no persistent state between spawns).
- Since `/api` is already proxied to the backend in `vite.config.ts`, the proxy takes
  precedence if the backend is up; the middleware only fires when the backend is down.
  This makes it a fallback stub, not a real solution.
- Adds fragile Node → Python subprocess coupling to the dev config.

**Verdict:** Not appropriate as the primary approach.  Could be added as an optional
offline-stub later (returns zeroes or canned data) — defer to @3design.

---

### Option D — Server-Sent Events (SSE) `GET /api/metrics/stream`

**Approach:**
Add a FastAPI `StreamingResponse` endpoint using `text/event-stream`.  The server sends
a JSON payload every 1–2 s.  Frontend uses `EventSource`.

**Pros:**
- Push-based; no repeated TCP connections once the stream is open.
- Plain HTTP — works through the existing Vite proxy.

**Cons:**
- SSE is one-directional; no control plane (e.g., changing the interval) without REST.
- `EventSource` does not support custom headers, limiting future auth integration.
- Vite dev-proxy may buffer SSE frames unless `Accept: text/event-stream` is forwarded
  correctly — adds proxy configuration risk.
- For a 1–2 s refresh rate the advantage over polling is essentially zero, while
  complexity is higher.

---

## Decision Matrix

| Criterion | Option A (REST Poll) | Option B (WS Push) | Option C (Vite MW) | Option D (SSE) |
|---|---|---|---|---|
| Works in production | ✅ Yes | ✅ Yes | ❌ Dev only | ✅ Yes |
| Backend changes | Minimal (1 route) | Medium (sub + task) | None | Small (1 route+stream) |
| Frontend changes | Minimal | Medium | None | Small |
| Differential net KB/s | ✅ Module state | ✅ Async task | ❌ No persistence | ✅ Generator state |
| Offline dev support | ❌ (backend required) | ❌ | ✅ | ❌ |
| Matches existing patterns | ✅ | ✅ WS already used | ✅ Vite plugin exists | ➖ New pattern |
| Test complexity | Low (mock endpoint) | High (async WS fixture) | Low (subprocess mock) | Medium |
| First-call edge case (net=0) | Trivial fix | Handled in task init | N/A | Handled in generator |
| Risk | Low | Medium | High | Low–Medium |

---

## Recommendation

**Option A — REST Polling via `GET /api/metrics/system`**

Add one FastAPI GET endpoint backed by psutil, maintaining module-level differential state
for network counters.  The Vite proxy is already wired; the component change is a straight
swap of `Math.random()` for `fetch`.  This is the lowest-risk, lowest-complexity path that
satisfies all acceptance criteria and works in both dev and production.

---

## Open Questions for @3design

1. **Network interface filtering**: `psutil.net_io_counters(pernic=True)` returns all
   interfaces including loopback (`lo`) and virtual adapters.  Should the endpoint filter
   to physical interfaces only (e.g., exclude names starting with `lo`, `docker`, `veth`)?
   Suggest: yes, filter by default but make configurable via query param.

2. **Poll interval**: Component currently polls every 1 s; acceptance criteria says
   default 2 s.  The designer should confirm the final default and whether the component
   should accept it as a prop or derive it from a constant.

3. **Offline/dev fallback**: Should a Vite middleware stub be added for offline dev
   (returns zeroes), or is requiring the backend for the metrics widget acceptable?
   This is a UX/DX choice.

4. **First-call network zeroes**: The first call will always return `tx_kbps: 0, rx_kbps: 0`
   since no prior sample exists.  The designer should decide whether to show a loading state
   or accept these zeroes (they resolve on the second call after ~1–2 s).

5. **CORS for `/api/metrics/system`**: The existing `CORSMiddleware` only allows
   `localhost:5173` and `localhost:3000`.  If Conky is served from another origin this will
   need updating.  For the current dev setup it is fine.

6. **Memory display**: The current component shows `mem %`.  The acceptance criteria
   specifies `memory_used_mb` + `memory_total_mb`.  The designer should decide whether the
   component keeps the percentage bar (computed from used/total) or also surfaces absolute MB.

<description, pros, cons>

## Decision Matrix
| Criterion | Opt A | Opt B |
|---|---|---|

## Recommendation
**Option <X>** — <rationale>

## Open Questions
<questions for @3design>
