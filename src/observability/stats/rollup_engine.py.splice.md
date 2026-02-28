# Splice: src/observability/stats/rollup_engine.py

This module contains multiple classes and logical responsibilities:

- `StatsRollupCalculator`: point bucketing and aggregate calculation helpers.
- `StatsRollup`: configuration, storage, and orchestration for rollup computation, including rust fallback.

Suggested splices:
- `calculator.py`: low-level bucketing and calculation logic.
- `manager.py`: `StatsRollup` orchestration and configuration storage.
- `rust_adapter.py`: encapsulate rust_core checks and calls.
