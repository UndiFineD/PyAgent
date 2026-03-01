# ShardingOrchestrator

**File**: `src\infrastructure\fleet\ShardingOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 141  
**Complexity**: 7 (moderate)

## Overview

Dynamic Communication Sharding Orchestrator (Phase 128).
Optimizes swarm latency by clustering frequently interacting agents.

## Classes (1)

### `ShardingOrchestrator`

Analyzes agent interactions and suggests/implements logical grouping.
Phase 234: Implements Dynamic Shard Rebalancing via DBSCAN and Live Migration.

**Methods** (7):
- `__init__(self, workspace_root, interaction_threshold)`
- `record_interaction(self, agent_a, agent_b, vram_a, vram_b)`
- `migrate_agent(self, agent_name, target_shard_id)`
- `rebalance_shards(self)`
- `_sync_mapping_to_disk(self)`
- `_save_mapping(self, mapping)`
- `load_mapping(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `collections.Counter`
- `json`
- `logging`
- `numpy`
- `pathlib.Path`
- `sklearn.cluster.DBSCAN`
- `sklearn.preprocessing.StandardScaler`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
