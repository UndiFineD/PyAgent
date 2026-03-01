# UsageMessage

**File**: `src\observability\telemetry\UsageMessage.py`  
**Type**: Python Module  
**Summary**: 2 classes, 12 functions, 19 imports  
**Lines**: 446  
**Complexity**: 17 (moderate)

## Overview

UsageMessage - Structured telemetry for platform detection and async reporting.

Inspired by vLLM's UsageMessage pattern for collecting environment information
and reporting usage statistics with privacy-respecting opt-out support.

Phase 24: Advanced Observability & Parsing

## Classes (2)

### `UsageContext`

**Inherits from**: str, Enum

Context in which PyAgent is being used.

### `UsageMessage`

Structured usage telemetry message.

Collects platform information and reports it asynchronously.

**Methods** (5):
- `collect_environment_info(self)`
- `report_usage(self, context, app_version, extra_kvs)`
- `_report_usage_worker(self, context, app_version, extra_kvs)`
- `_save_local_stats(self, extra_kvs)`
- `to_dict(self)`

## Functions (12)

### `set_runtime_usage_data(key, value)`

Set global usage data to include in telemetry.

Args:
    key: Data key
    value: Data value

### `get_runtime_usage_data()`

Get all global runtime usage data.

### `clear_runtime_usage_data()`

Clear all global runtime usage data.

### `is_usage_stats_enabled()`

Check if usage statistics collection is enabled.

Respects the following opt-out mechanisms:
- PYAGENT_DO_NOT_TRACK=1
- DO_NOT_TRACK=1
- PYAGENT_NO_USAGE_STATS=1
- ~/.config/pyagent/do_not_track file exists

Returns:
    True if usage stats are enabled, False otherwise

### `disable_usage_stats()`

Programmatically disable usage stats collection.

### `enable_usage_stats()`

Programmatically enable usage stats collection.

### `detect_cloud_provider()`

Detect the cloud provider where the code is running.

Returns:
    Cloud provider name or "UNKNOWN"

### `get_cpu_info()`

Get CPU information.

Returns:
    Dictionary with CPU details

### `get_gpu_info()`

Get GPU information if available.

Returns:
    Dictionary with GPU details or empty dict

### `get_memory_info()`

Get system memory information.

Returns:
    Dictionary with memory details in bytes

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `cpuinfo`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timezone`
- `enum.Enum`
- `json`
- `os`
- `pathlib.Path`
- `platform`
- `psutil`
- `sys`
- `threading.Thread`
- `time`
- ... and 4 more

---
*Auto-generated documentation*
