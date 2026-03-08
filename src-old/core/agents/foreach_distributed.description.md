# foreach_distributed

**File**: `src\core\agents\foreach_distributed.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 12 imports  
**Lines**: 299  
**Complexity**: 13 (moderate)

## Overview

Distributed Foreach coordinator and worker helpers.

This module contains a lightweight Worker implementation used by the Foreach
Coordinator to claim shards, acquire per-file locks, and report status to the
scratch area (or recorder). The implementation is intentionally small and
synchronous to make dry-run and staged runs deterministic and easy to test.

## Classes (3)

### `WorkerClaimError`

**Inherits from**: Exception

Raised when a worker fails to claim a shard.

### `Worker`

A simple worker that claims a shard, acquires locks, and reports status.

This is a synchronous helper designed for staged runs and unit tests.

**Methods** (9):
- `__init__(self, worker_id, scratch_dir, file_lock_manager, worker_timeout, shard_lock_prefix, conflict_strategy, sleep_fn)`
- `_status_path(self)`
- `_write_status(self, status, detail)`
- `load_manifest(self, manifest_path)`
- `_lock_id_for_file(self, file_path)`
- `claim_shard(self, manifest_path)`
- `claim_shard_with_retries(self, manifest_path, retries, delay, backoff, sleep_fn)`
- `release_locks(self)`
- `report_progress(self, message, meta)`

### `Coordinator`

A lightweight coordinator for staged Foreach runs.

The Coordinator reads a manifest describing shards and monitors worker
status files in a scratch area. It will detect stalled workers and emit
simple reassign markers, and will detect shard completion (status 'done')
and include a 'merge' hint in the aggregated report.

For safety, the Coordinator ensures that the manifest indicates tests
should be run for staged changes by setting `enforce_tests` to True by
default. Agents and Workers may consult this flag when choosing whether
to run focused tests before staging edits.

**Methods** (4):
- `__init__(self, manifest_path, scratch_dir, poll_interval, worker_timeout, leader_ttl)`
- `assign_shards(self)`
- `monitor_workers_and_merge(self, wait_for_completion)`
- `elect_leader(self, leader_name)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `asyncio`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.common.file_system_core.FileSystemCore`
- `src.core.base.common.utils.file_lock_manager.FileLockManager`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
