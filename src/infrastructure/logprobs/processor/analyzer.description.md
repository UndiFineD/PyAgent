# analyzer

**File**: `src\infrastructure\logprobs\processor\analyzer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 54  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for analyzer.

## Classes (1)

### `LogprobsAnalyzer`

Analyze logprobs for insights.

**Methods** (4):
- `rank_token_importance(logprobs, threshold)`
- `compute_confidence(logprobs, method)`
- `detect_anomalies(logprobs, z_threshold)`
- `compute_calibration(logprobs, num_bins)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `config.LogprobEntry`
- `numpy`
- `storage.FlatLogprobs`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
