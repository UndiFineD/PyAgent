# conky-real-metrics

**Project ID:** `prj0000047`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [ ] `GET /api/metrics/system` returns JSON with `cpu_percent`, `memory_used_mb`, `memory_total_mb`,
- [ ] Conky widget displays live values, refreshing at a configurable interval (default 2 s).
- [ ] No `Math.random()` or simulated data remains in `Conky.tsx`.
- [ ] All existing tests pass; new unit tests cover the backend endpoint.

## Status

0 of 4 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\inference\metrics.rs`
  - `rust_core\src\metrics.rs`
  - `rust_core\src\stats\metrics.rs`
  - `rust_core\src\utils\metrics.rs`
  - `src\observability\stats\metrics_engine.py`
  - `src\tools\metrics.py`
  - `tests\observability\test_metrics_engine.py`
  - `tests\test_backend_system_metrics.py`
  - `tests\test_metrics.py`
  - `tests\tools\test_metrics_collector.py`