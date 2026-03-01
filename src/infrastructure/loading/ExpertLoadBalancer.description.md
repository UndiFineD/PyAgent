# ExpertLoadBalancer

**File**: `src\infrastructure\loading\ExpertLoadBalancer.py`  
**Type**: Python Module  
**Summary**: 8 classes, 3 functions, 30 imports  
**Lines**: 643  
**Complexity**: 25 (complex)

## Overview

Expert Load Balancer for PyAgent

This module provides expert parallelism load balancing (EPLB) functionality
inspired by vLLM's distributed/eplb module for MoE models.

Key Features:
- Physical-to-logical expert mapping
- Load-balanced expert replication
- Hierarchical packing for locality
- BEYOND vLLM: Locality-aware policies, async rebalancing, adaptive replication

vLLM Patterns:
- AbstractEplbPolicy for rebalancing interface
- DefaultEplbPolicy with balanced packing
- EplbModelState for metrics tracking
- Expert weight rearrangement

## Classes (8)

### `ExpertType`

**Inherits from**: Enum

Types of experts in MoE models.

### `EplbMetrics`

Metrics for expert parallelism load balancing.

vLLM Pattern: EplbModelState from eplb_state.py

**Methods** (3):
- `num_layers(self)`
- `num_physical_experts(self)`
- `num_logical_experts(self)`

### `ExpertMapping`

Complete mapping between logical and physical experts.

vLLM Pattern: Result of rebalance_experts

**Methods** (2):
- `get_physical_experts(self, layer, logical_idx)`
- `get_logical_expert(self, layer, physical_idx)`

### `AbstractEplbPolicy`

**Inherits from**: ABC

Abstract policy for expert load balancing.

vLLM Pattern: AbstractEplbPolicy from policy/abstract.py

**Methods** (1):
- `rebalance_experts(cls, weight, num_replicas, num_groups, num_nodes, num_ranks)`

### `DefaultEplbPolicy`

**Inherits from**: AbstractEplbPolicy

Default EPLB policy with balanced packing.

vLLM Pattern: DefaultEplbPolicy from policy/default.py
Adapted from DeepSeek EPLB algorithm.

**Methods** (3):
- `balanced_packing(cls, weight, num_packs)`
- `replicate_experts(cls, weight, num_physical)`
- `rebalance_experts(cls, weight, num_replicas, num_groups, num_nodes, num_ranks)`

### `LocalityAwarePolicy`

**Inherits from**: AbstractEplbPolicy

Locality-aware EPLB policy.

BEYOND vLLM: Considers network topology for expert placement.
Prioritizes keeping related experts on same node.

**Methods** (1):
- `rebalance_experts(cls, weight, num_replicas, num_groups, num_nodes, num_ranks)`

### `ExpertLoadBalancer`

Main expert load balancer class.

Manages expert replication and rearrangement for MoE models.

**Methods** (6):
- `__init__(self, num_layers, num_logical_experts, num_physical_experts, num_ranks, num_nodes, policy, window_size)`
- `record_load(self, layer, expert_loads)`
- `advance_window(self)`
- `get_average_load(self)`
- `rebalance(self, weight)`
- `mapping(self)`

### `AsyncExpertRebalancer`

Asynchronous expert rebalancer.

BEYOND vLLM: Background rebalancing with minimal inference disruption.

**Methods** (6):
- `__init__(self, balancer, rebalance_interval, load_threshold)`
- `start(self)`
- `stop(self)`
- `_should_rebalance(self)`
- `_rebalance_loop(self)`
- `get_pending_mapping(self)`

## Functions (3)

### `compute_balanced_packing_rust(weights, num_packs)`

Balanced packing using Rust.

### `compute_expert_replication_rust(weights, num_physical)`

Expert replication using Rust.

### `compute_load_imbalance_rust(loads)`

Compute load imbalance ratio using Rust.

## Dependencies

**Imports** (30):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `concurrent.futures`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `rust_core`
- `threading`
- `time`
- `torch`
- `typing.Any`
- ... and 15 more

---
*Auto-generated documentation*
