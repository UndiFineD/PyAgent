# Description: src/observability/stats/scheduler_stats.py

Module overview:
- Contains classes and dataclasses for scheduler-related statistics: `PrefixCacheStats`, `SpecDecodingStats`, `CUDAGraphStats`, `PerfStats`, etc.
- Provides methods to record and summarize scheduler-level metrics used for LLM inference orchestration.

Behavioral notes:
- Designed for high-resolution telemetry and performance analysis of scheduling and speculative decoding.
- Includes convenience methods to convert stats to dictionaries and clone/reset state.
