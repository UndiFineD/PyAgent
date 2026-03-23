# conky-real-metrics — Implementation Plan

_Status: HANDED_OFF_
_Planner: @4plan | Updated: 2026-03-23_

## Overview

Replace the `Math.random()` simulation in `web/apps/Conky.tsx` with real system metrics
polled from a new `GET /api/metrics/system` FastAPI endpoint in `backend/app.py`.
The endpoint uses `psutil` to read CPU %, memory, network TX/RX KB/s (per physical interface),
and disk read/write KB/s.  The frontend hook `useSystemMetrics` polls every 2 s, preserves
last-known values on error, and surfaces an `OFFLINE` badge when the backend is unreachable.
Disk I/O is added to the rendered widget.  No `vite.config.ts` changes are required.

---

## Task List

### Backend

- [ ] **T1 — Add psutil to backend dependencies**
  - **Files:** `backend/requirements.txt`
  - **Change:** Add `psutil>=5.9` line.
  - **Acceptance:** `pip install -r backend/requirements.txt` succeeds with no resolution
    errors; `python -c "import psutil; print(psutil.__version__)"` prints a version ≥ 5.9.

- [ ] **T2 — Add Pydantic response models to `app.py`**
  - **Files:** `backend/app.py`
  - **Change:** Below existing `BaseModel` imports, add four models:
    `NetworkInterface`, `MemoryMetrics`, `DiskMetrics`, `SystemMetricsResponse`
    with fields exactly matching the design contract.
  - **Acceptance:** `python -c "from backend.app import SystemMetricsResponse; m =
    SystemMetricsResponse(cpu_percent=0, memory=dict(used_mb=0,total_mb=0,percent=0),
    network=[], disk=dict(read_kbps=0,write_kbps=0), sampled_at=0)"` succeeds without
    `ValidationError`.

- [ ] **T3 — Implement differential state, interface filter, and endpoint**
  - **Files:** `backend/app.py`
  - **Change:**
    1. Module-level state:
       `_prev_net: dict[str, tuple[int, int]] = {}`
       `_prev_net_ts: float = 0.0`
       `_prev_disk: tuple[int, int] = (0, 0)`
       `_prev_disk_ts: float = 0.0`
    2. `_IFACE_EXCLUDE_PREFIXES` tuple and `_is_physical_iface(name)` helper.
    3. `@app.get("/api/metrics/system", response_model=SystemMetricsResponse)` endpoint
       reading `psutil.cpu_percent(interval=None)`, `psutil.virtual_memory()`,
       `psutil.net_io_counters(pernic=True)` (filtered + delta), and
       `psutil.disk_io_counters()` (delta).  First call returns `0.0 KB/s` for rate
       fields; subsequent calls return computed KB/s.
  - **Acceptance:**
    - `GET /api/metrics/system` returns HTTP 200 with `Content-Type: application/json`.
    - Response body validates as `SystemMetricsResponse`.
    - On first call: `network[*].tx_kbps == 0.0`, `disk.read_kbps == 0.0`.
    - No loopback/virtual interfaces appear in the `network` array.

### Tests

- [ ] **T4 — Unit tests for `GET /api/metrics/system`**
  - **Files:** `tests/test_backend_system_metrics.py` _(new file)_
  - **Tests:**
    1. `test_first_call_returns_zero_rates` — mock `psutil.*`; assert all KB/s fields `== 0.0`.
    2. `test_second_call_computes_delta` — set module-level `_prev_*` state, provide counter
       diff, assert `tx_kbps > 0` and `disk.read_kbps > 0`.
    3. `test_memory_fields_correct` — mock `virtual_memory()` with known values; assert
       `used_mb`, `total_mb`, `percent` match expectations.
    4. `test_loopback_excluded` — mock `net_io_counters` including a `lo` and `Loopback …`
       interface; assert none appear in response `network` list.
    5. `test_sampled_at_is_recent` — assert `sampled_at` is within 5 s of `time.time()`.
    6. `test_endpoint_returns_200` — use `httpx.AsyncClient` (`app=app`, ASGI) to call
       the route; assert `status_code == 200`.
  - **Acceptance:**
    ```powershell
    & c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
    python -m pytest tests/test_backend_system_metrics.py -v
    ```
    All 6 tests green; 0 errors, 0 warnings.

### Frontend

- [ ] **T5 — Add TypeScript interfaces and `useSystemMetrics` hook inline in `Conky.tsx`**
  - **Files:** `web/apps/Conky.tsx`
  - **Change:** Before the component definition, add:
    - `SystemMetrics`, `HistoryPoint`, `MetricsState` interface declarations (matching the
      design contract exactly).
    - `const POLL_INTERVAL_MS = 2000` constant.
    - `useSystemMetrics(intervalMs: number): MetricsState` function using `useState` +
      `useEffect` + `useRef` for the interval handle.  On success: appends `HistoryPoint`,
      caps history at 20, clears `error`.  On failure: preserves `current`, sets `error`.
  - **Acceptance:**
    ```powershell
    cd c:\Dev\PyAgent\web
    npx tsc --noEmit
    ```
    Zero TypeScript errors.  The hook is importable (used inside the same file).

- [ ] **T6 — Replace simulation with hook; add OFFLINE badge, disk row, memory detail**
  - **Files:** `web/apps/Conky.tsx`
  - **Change:**
    1. **Remove:** `generateData()` function; all `Math.random()` calls; `data`/`stats`
       `useState` pair; the 1 000 ms `setInterval` block.
    2. **Replace:** Single `const metrics = useSystemMetrics(POLL_INTERVAL_MS)` call.
       Derive display values from `metrics.current` (fall back to `0` when `null`).
    3. **Memory row label:** `{mem}%  ·  {used_mb} MB / {total_mb} MB`.
    4. **Network:** `netUp` = sum of `network[].tx_kbps`; `netDown` = sum of
       `network[].rx_kbps`.
    5. **Disk I/O row** (new): `DISK  R: {read_kbps} KB/s  W: {write_kbps} KB/s` below
       the Network section.
    6. **OFFLINE badge:** next to `SYSTEM_MONITOR` header — `text-red-500/50 text-[9px]`
       — rendered when `metrics.error !== null`.
    7. Chart `data` prop: `metrics.history`; chart `dataKey` for net chart: `"net"` from
       `HistoryPoint.net` (sum of rx_kbps).
  - **Acceptance:**
    - `grep -r "Math.random" web/apps/Conky.tsx` returns no matches.
    - `npx tsc --noEmit` returns exit code 0.
    - Manual smoke: widget shows live CPU bar movement; memory label has MB detail; disk
      row visible; OFFLINE badge appears within 2 s if backend is stopped.

### Integration

- [ ] **T7 — End-to-end integration validation**
  - **Files:** none _(validation only)_
  - **Steps:**
    1. Start backend: `uvicorn backend.app:app --port 444`.
    2. Call endpoint twice (2 s apart): verify second response has `network` with at least
       one interface and `cpu_percent` in 0–100.
    3. Stop backend; confirm Conky widget shows `OFFLINE` badge and retains last values.
    4. Restart backend; confirm badge clears within one poll cycle.
  - **Acceptance:**
    ```powershell
    # Full backend test suite (no regressions in existing tests)
    & c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
    python -m pytest tests/test_backend_system_metrics.py tests/test_backend_worker.py `
                     tests/test_backend_models.py tests/test_backend_session_manager.py -v
    # TypeScript compile check
    cd c:\Dev\PyAgent\web; npx tsc --noEmit
    ```
    All tests green; tsc exit code 0.

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Backend endpoint live + tested | T1, T2, T3, T4 | |
| M2 | Frontend real-data rendering | T5, T6 | |
| M3 | Full integration validated | T7 | |

---

## Dependency Order

```
T1 (psutil dep)
  └─ T2 (Pydantic models)
       └─ T3 (endpoint impl)
            └─ T4 (unit tests)   ← can run concurrently with T5
T5 (TS interfaces + hook)
  └─ T6 (component swap)
       └─ T7 (integration, depends on T4 + T6)
```

---

## Validation Commands

```powershell
# Activate venv
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Backend unit tests (new + existing, no regressions)
python -m pytest tests/test_backend_system_metrics.py -v

# Full backend regression sweep
python -m pytest tests/test_backend_system_metrics.py `
                 tests/test_backend_worker.py `
                 tests/test_backend_models.py `
                 tests/test_backend_session_manager.py -v

# TypeScript compile (frontend)
cd c:\Dev\PyAgent\web
npx tsc --noEmit
```
