# DimensionalityAgent

**File**: `src\logic\agents\specialists\DimensionalityAgent.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 18 imports  
**Lines**: 360  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for DimensionalityAgent.

## Classes (3)

### `ReductionMethod`

**Inherits from**: Enum

Class ReductionMethod implementation.

### `EmbeddingStats`

Statistics for an embedding.

### `DimensionalityAgent`

**Inherits from**: BaseAgent

Agent specializing in simplifying complex datasets and high-dimensional spaces.
Focuses on PCA, t-SNE (simulated), UMAP, and semantic embedding compression.

**Methods** (3):
- `__init__(self, file_path)`
- `_pca_reduce(self, embedding, target_dim)`
- `_random_projection(self, embedding, target_dim)`

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `math`
- `random`
- `re`
- `rust_core`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `typing.Any`
- `typing.Dict`
- ... and 3 more

---
*Auto-generated documentation*
