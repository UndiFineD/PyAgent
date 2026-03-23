# conky-real-metrics — Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-23_

---

## Selected Option

**Option A — REST Polling via `GET /api/metrics/system`**

One FastAPI endpoint backed by `psutil`. Module-level differential state for network and disk
counters. The Vite `/api` proxy is already wired; the component change is a straight swap of
`Math.random()` for `fetch`. Lowest-risk, lowest-complexity path that satisfies all acceptance
criteria in both dev and production.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Browser (port 44)                                        │
│  web/apps/Conky.tsx                                       │
│    └── useSystemMetrics(2000)  — custom hook              │
│          └── fetch('/api/metrics/system')  every 2 s     │
└─────────────────────┬────────────────────────────────────┘
                      │  HTTP GET (Vite proxy → port 444)
┌─────────────────────▼────────────────────────────────────┐
│  FastAPI  backend/app.py  (port 444)                      │
│    └── GET /api/metrics/system                            │
│          ├── psutil.cpu_percent(interval=None)            │
│          ├── psutil.virtual_memory()                      │
│          ├── psutil.net_io_counters(pernic=True)  + delta │
│          └── psutil.disk_io_counters()            + delta │
└──────────────────────────────────────────────────────────┘
```

**Data flow:**
1. Component mounts → `useSystemMetrics` hook starts a 2 s interval.
2. Each tick: `fetch('/api/metrics/system')` → Vite dev proxy → FastAPI.
3. FastAPI reads `psutil`, computes deltas against module-level state, returns JSON.
4. Hook updates `MetricsState` (current snapshot + 20-point rolling history).
5. Component re-renders: bars, charts, and numeric labels reflect real values.
6. On fetch error: hook preserves last good values, sets `error` → component shows
   `OFFLINE` badge; recovers automatically on next successful fetch.

**No Vite dev plugin is required.** The `/api` proxy in `vite.config.ts` already handles
routing. The component's error-handling strategy (stay on last values) covers the offline
case without a Node.js fallback stub.

---

## Interfaces & Contracts

### 1 · API response — TypeScript

```typescript
/** Returned by GET /api/metrics/system */
export interface SystemMetrics {
  /** CPU utilisation 0–100 (non-blocking, uses psutil internal 2-sample window). */
  cpu_percent: number;

  memory: {
    used_mb: number;     // physical RAM used (excl. buffers/cache on Linux)
    total_mb: number;    // total physical RAM
    percent: number;     // pre-computed: used_mb / total_mb × 100
  };

  /** One entry per physical/Wi-Fi adapter (loopback + virtual excluded). */
  network: Array<{
    interface: string;
    tx_kbps: number;     // kilobytes/s sent since previous call (0 on first call)
    rx_kbps: number;     // kilobytes/s received since previous call (0 on first call)
  }>;

  disk: {
    read_kbps: number;   // logical disk read KB/s since previous call
    write_kbps: number;  // logical disk write KB/s since previous call
  };

  /** Unix epoch seconds (float).  Used for delta validation. */
  sampled_at: number;
}
```

### 2 · React state shape

```typescript
interface HistoryPoint {
  time: number;   // sequence counter (incrementing)
  cpu: number;    // cpu_percent
  mem: number;    // memory.percent
  net: number;    // sum of all rx_kbps (total inbound KB/s)
}

interface MetricsState {
  current: SystemMetrics | null;   // latest snapshot; null only before first success
  history: HistoryPoint[];         // rolling window, max 20 points
  error: string | null;            // set on fetch failure; cleared on next success
  lastGoodAt: number | null;       // Date.now() of last successful fetch
}
```

### 3 · Custom hook signature

```typescript
/**
 * Polls GET /api/metrics/system every `intervalMs` milliseconds.
 * On error: preserves last current snapshot, sets error string.
 * On recovery: clears error, resumes normal updates.
 */
export function useSystemMetrics(intervalMs: number = 2000): MetricsState;
```

Internal shape:
- `useRef<number>` for interval handle.
- `useState<MetricsState>` initialised with `{ current: null, history: [], error: null, lastGoodAt: null }`.
- `useEffect` registers interval → inner async `fetchMetrics()` → on success appends
  `HistoryPoint`, evicts oldest if `history.length > 20`, clears `error`; on error
  preserves `current`, sets `error` to `err.message`.
- Cleanup via returned `clearInterval`.

### 4 · Backend — Python function signatures

**Module-level state (top of `app.py`, below existing module globals):**

```python
import time
import psutil

# Differential state for network and disk KB/s calculation.
# Safe for single-worker Uvicorn (dev default).
_prev_net: dict[str, tuple[int, int]] = {}   # {iface: (bytes_sent, bytes_recv)}
_prev_net_ts: float = 0.0
_prev_disk: tuple[int, int] = (0, 0)         # (read_bytes, write_bytes)
_prev_disk_ts: float = 0.0
```

**Pydantic response models:**

```python
class NetworkInterface(BaseModel):
    interface: str
    tx_kbps: float
    rx_kbps: float

class MemoryMetrics(BaseModel):
    used_mb: float
    total_mb: float
    percent: float

class DiskMetrics(BaseModel):
    read_kbps: float
    write_kbps: float

class SystemMetricsResponse(BaseModel):
    cpu_percent: float
    memory: MemoryMetrics
    network: list[NetworkInterface]
    disk: DiskMetrics
    sampled_at: float
```

**Interface filtering helper:**

```python
# Prefixes that identify loopback, virtual, and tunnel interfaces.
_IFACE_EXCLUDE_PREFIXES: tuple[str, ...] = (
    "lo", "docker", "veth", "br-", "virbr", "tun", "tap",
    "loopback",           # Windows loopback alias
    "isatap", "teredo",   # Windows tunnel adapters
)

def _is_physical_iface(name: str) -> bool:
    """Return True if the interface is likely a physical or Wi-Fi adapter."""
    lower = name.lower()
    return not any(lower.startswith(p) for p in _IFACE_EXCLUDE_PREFIXES)
```

**Endpoint signature:**

```python
@app.get("/api/metrics/system", response_model=SystemMetricsResponse)
async def get_system_metrics() -> SystemMetricsResponse:
    """
    Return current CPU, memory, network, and disk metrics.

    Network and disk rates are kilobytes/s deltas since the previous call.
    Returns 0.0 KB/s for both on the first call (no prior sample).
    psutil.cpu_percent(interval=None) reads the internal OS counter diff;
    the first call may return 0.0 — acceptable, value is valid from the
    second call onward.
    """
    ...
```

---

## Component Layout Decision

### What **stays** unchanged
- Black/green monospace `SYSTEM_MONITOR` theme.
- `SYSTEM_MONITOR` header with `Activity` pulse icon.
- CPU section: percent bar + `AreaChart` (20-point rolling history).
- Network section: UP/DOWN KB/s row + `LineChart` (total rx_kbps history).
- Token Usage section at the bottom — **remains fake** (AI token tracking is out of scope).

### What **changes**
| Element | Before | After |
|---|---|---|
| Data source | `Math.random()` inside `setInterval` | `useSystemMetrics(2000)` hook |
| Poll interval | 1 000 ms | 2 000 ms (`POLL_INTERVAL_MS = 2000` constant) |
| Memory row label | `{mem}%` | `{mem}%  ·  {used_mb} MB / {total_mb} MB` |
| Net chart dataKey | `net` (random) | sum of `network[].rx_kbps` (real) |
| Net UP display | random KB/s | sum `tx_kbps` across all interfaces |
| Net DOWN display | random KB/s | sum `rx_kbps` across all interfaces |

### What **is added**
1. **`useSystemMetrics` hook** — may live in `web/apps/Conky.tsx` as a module-level function
   (no new file required unless preferred by `@4plan`).
2. **`OFFLINE` badge** — shown next to the header when `metrics.error !== null`.
   Styling: `text-red-500/50 text-[9px]` — subtle, does not obscure the display.
3. **Disk I/O row** — single line below Network: `DISK  R: {read_kbps} KB/s  W: {write_kbps} KB/s`.
   Data was already in the `stats` object but never rendered.

### What **is removed**
- `generateData()` function.
- All `Math.random()` calls inside the interval.
- The local `stats` / `data` state pair — replaced by `MetricsState` from the hook.

---

## Network Interface Filtering Rules

**Filter-out list (prefixes, case-insensitive):**

| Prefix | Reason |
|---|---|
| `lo` | Linux loopback |
| `loopback` | Windows loopback alias |
| `docker` | Docker bridge |
| `veth` | Docker/Kubernetes virtual Ethernet pair |
| `br-` | Linux software bridge |
| `virbr` | libvirt/KVM bridge |
| `tun` | VPN tunnel (OpenVPN etc.) |
| `tap` | Layer-2 tunnel |
| `isatap` | Windows IPv6 tunnel |
| `teredo` | Windows IPv6 tunnel |

**Aggregation for display:** Sum all passing interfaces for UP/DOWN totals.  
If zero interfaces pass the filter (unusual), return an empty `network` list; the component
displays `0 KB/s` for both directions.

---

## Error-Handling Strategy: Backend Not Running

| State | `current` | `error` | UI |
|---|---|---|---|
| First fetch succeeds | populated | `null` | normal display |
| First fetch fails | `null` | error string | zeros + dim `OFFLINE` badge |
| Subsequent fetch fails | preserved (last good values) | error string | last values + dim `OFFLINE` badge |
| Recovery (fetch succeeds again) | updated | `null` | badge disappears, values update |

**Decision: stay on last known values** — never show a spinner or blank panel when the
backend goes down. The `OFFLINE` badge is the only error signal. This matches the "always
glanceable" intent of a system monitor widget.

---

## vite.config.ts Analysis

**No changes required.**

The existing `/api` proxy block already forwards `GET /api/metrics/system` to the FastAPI
backend:

```typescript
'/api': {
  target: `http://${env.HOST || '0.0.0.0'}:${env.BACKEND_PORT || '444'}`,
  changeOrigin: true,
},
```

A Vite dev-server metrics stub (`vite-metrics-stub`) was evaluated and rejected:
- It would intercept ALL requests (before the proxy), returning stale zeros even when the
  backend is running.
- It cannot call `psutil` (Node.js context).
- The component's `try/catch` error-handling makes it redundant.

The `vite-agent-docs` pattern survives because it reads from the **filesystem** (always
authoritative), not from a live process.

---

## Non-Functional Requirements

- **Performance:** `psutil.cpu_percent(interval=None)` is non-blocking; the endpoint must
  complete in < 50 ms on any development machine. No sleep or blocking I/O allowed.
- **Security:** The endpoint reads local host OS metrics only. No user input is accepted.
  Module-level state holds only numeric counters — no secrets or user data. The existing
  `CORSMiddleware` (allows `localhost:5173`, `localhost:3000`) is sufficient for dev.
- **Testability:** `SystemMetricsResponse` is a plain Pydantic model — unit-testable with
  `psutil` mocked via `unittest.mock.patch`. The `useSystemMetrics` hook is testable by
  mocking `fetch` (Vitest + `vi.spyOn(global, 'fetch')`).

---

## Open Questions for @4plan

1. **File placement for hook:** Place `useSystemMetrics` inline in `Conky.tsx` or extract
   to `web/hooks/useSystemMetrics.ts`? Recommendation: inline for this project size, extract
   if reused by more than one component.
2. **`psutil.cpu_percent` first-call zero:** The first API call returns `cpu_percent: 0.0`
   because the internal OS diff has no baseline. Second call (2 s later) is accurate.
   Accept this or add a startup prime call in `app.py` on module load?
3. **Windows loopback interface name:** Windows uses `Loopback Pseudo-Interface 1` and
   similar names. The prefix `loopback` covers this but should be validated on the target
   dev machine.

---

## Artifact Index

| Artifact | Path |
|---|---|
| This design doc | `docs/project/prj0000047/conky-real-metrics.design.md` |
| Think doc (input) | `docs/project/prj0000047/conky-real-metrics.think.md` |
| Frontend component | `web/apps/Conky.tsx` |
| Backend entry point | `backend/app.py` |
| Vite config (no change) | `web/vite.config.ts` |
