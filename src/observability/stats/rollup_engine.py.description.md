# Description: src/observability/stats/rollup_engine.py

Module overview:
- Implements rollup calculation utilities and rollup manager classes for aggregating metrics over time windows.
- Provides Rust-accelerated fallback for aggregation when available.

Primary classes:
- `StatsRollupCalculator`: lower-level calculator for bucketing and basic aggregation.
- `StatsRollup`: higher-level rollup manager that configures rollups and computes aggregated values.

Behavioral notes:
- Supports aggregation types including SUM, AVG, MIN, MAX, COUNT, and percentiles.
- Attempts to delegate heavy calculations to `rust_core` if available.
