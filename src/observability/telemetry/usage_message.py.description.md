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

