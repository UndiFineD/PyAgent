# Improvements: src/observability/stats/rollup_engine.py

Potential improvements:
- Add unit tests for percentile and aggregation logic, including corner cases (empty lists, small samples).
- Refactor into smaller modules to separate rust adapter, calculation, and configuration.
- Improve percentile calculation to use interpolation instead of naive indexing for non-integer positions.
- Provide deterministic behavior for bucket boundaries (document inclusive/exclusive behavior).
- Add logging for fallback to Python path and metrics about when rust_core is used.
