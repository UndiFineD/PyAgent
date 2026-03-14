#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/telemetry/usage_message.description.md

# Description: src/observability/telemetry/usage_message.py

Module docstring summary:
- Provides `UsageMessage` dataclass and utilities to collect environment and usage telemetry.
- Includes helpers to detect cloud provider, CPU/GPU/memory info, and opt-out mechanisms for telemetry.
- Exposes runtime global usage data management functions (`set_runtime_usage_data`, `get_runtime_usage_data`, `clear_runtime_usage_data`) and opt-in/out controls (`is_usage_stats_enabled`, `disable_usage_stats`, `enable_usage_stats`).

Primary classes and functions:
- `UsageMessage` (dataclass)
- `UsageContext` (Enum)
- `is_usage_stats_enabled()`
- `detect_cloud_provider()`
- `get_cpu_info()`, `get_gpu_info()`, `get_memory_info()`

Behavioral notes:
- Gathers many system details and attempts to import optional dependencies (`psutil`, `cpuinfo`, `torch`).
- Honors explicit opt-out via environment variables or a `do_not_track` file.
## Source: src-old/observability/telemetry/usage_message.improvements.md

# Improvements: src/observability/telemetry/usage_message.py

Potential improvements:
- Add comprehensive unit tests for `UsageMessage` serialization and opt-out behavior.
- Break module into smaller modules (`datamodels`, `runtime`, `detection`, `reporting`) to reduce cognitive complexity.
- Replace global mutable `_GLOBAL_RUNTIME_DATA` with an injectable runtime store or context object for testability.
- Avoid heavy optional imports at top-level; import lazily inside functions to speed up import time.
- Add type hints for all internal helper functions and document return shapes.
- Add retry/backoff and timeout behavior for any external calls and file I/O.
- Use dependency injection for filesystem paths and telemetry sinks to make testing easier.
- Improve privacy: reduce the amount of environment data collected by default, and add a clear opt-in flag.
- Consider making collection async to avoid blocking critical paths.
- Add clearer logging and metrics around telemetry dispatch and failures.

LLM_CONTEXT_END
"""

r"""UsageMessage dataclass for structured usage telemetry."""
