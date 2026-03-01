# LatentLink

**File**: `src\infrastructure\kv_transfer\LatentLink.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 6 imports  
**Lines**: 64  
**Complexity**: 7 (moderate)

## Overview

LatentLink: Cross-model KV alignment for latent communication.
Implemented based on arXiv:2601.06123 (Latent space communication for multi-agent systems).

## Classes (3)

### `SynapticAdapter`

**Inherits from**: Module

Projector layer to align KV caches between different agents/models.
Enables 'SynapticLink' communication for 10x bandwidth reduction.

**Methods** (2):
- `__init__(self, source_dim, target_dim)`
- `forward(self, source_kv)`

### `LatentLinkManager`

Manages synaptic connections between different agent KV caches.

**Methods** (3):
- `__init__(self)`
- `register_connection(self, source_id, target_id, source_dim, target_dim)`
- `transfer_latent(self, source_id, target_id, source_kv)`

### `SynapticLink`

High-level interface for agent-to-agent latent communication.

**Methods** (2):
- `__init__(self, manager, agent_id)`
- `transmit(self, target_agent_id, context_kv)`

## Dependencies

**Imports** (6):
- `torch`
- `torch.nn`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
