# Improvements: src/observability/stats/scheduler_stats.py

Potential improvements:
- Add unit tests for `PrefixCacheStats`, `SpecDecodingStats`, and `CUDAGraphStats` to validate hit rates, acceptance rates, and averages.
- Use `time.monotonic()` for timing measurements to avoid system clock changes affecting durations.
- Document units for all timing fields (ms assumed) and consider consistent naming like `_ms` suffix.
- Provide serialization helpers and compact summaries for telemetry export.
- Add optional limits or thresholds to prevent unbounded list growth in `num_accepted_tokens_per_pos`.
