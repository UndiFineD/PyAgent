# Splice: src/observability/telemetry/usage_message.py

This module contains multiple top-level types and callable groups:

Classes / Dataclasses / Enums:
- `UsageMessage` (dataclass): structured telemetry message that holds platform and environment information.
- `UsageContext` (Enum): defines contexts like CLI, API_SERVER, FLEET_ORCHESTRATION, etc.

Functions groups:
- Runtime data management: `set_runtime_usage_data`, `get_runtime_usage_data`, `clear_runtime_usage_data`.
- Opt-out management: `is_usage_stats_enabled`, `disable_usage_stats`, `enable_usage_stats`.
- Platform detection: `detect_cloud_provider`, `get_cpu_info`, `get_gpu_info`, `get_memory_info`.

Suggested splices (logical separation for maintainability):
- `runtime` module: runtime global usage state and setters/getters.
- `detection` module: cloud/CPU/GPU/memory detection helpers.
- `datamodels` module: `UsageMessage` and `UsageContext`.
- `telemetry` module: reporting, async dispatch, and file persistence.
