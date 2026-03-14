#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/MetricsCore.description.md

# MetricsCore

**File**: `src\observability\stats\MetricsCore.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 12 imports  
**Lines**: 593  
**Complexity**: 25 (complex)

## Overview

MetricsCore - Pure calculation logic for metrics processing.

This module contains all pure computational logic without I/O operations,
making it a candidate for Rust conversion. It handles:
- Token cost calculations
- Metric aggregation and rollup
- Formula evaluation and derived metrics
- Correlation analysis
- Statistical forecasting
- A/B comparison analysis

No I/O operations, no file access, no external calls.

## Classes (7)

### `TokenCostResult`

Result of token cost calculation.

### `TokenCostCore`

Pure token cost calculation (Rust-convertible).

Calculates costs based on model pricing without I/O.

**Methods** (3):
- `__init__(self)`
- `calculate_cost(self, input_tokens, output_tokens, model)`
- `estimate_cost_per_token(self, model)`

### `ModelFallbackCore`

Pure logic for model selection and fallback (Rust-convertible).

**Methods** (3):
- `__init__(self)`
- `select_best_model(self, constraints)`
- `get_fallback_chain(self, primary)`

### `DerivedMetricCalculator`

Calculate derived metrics from dependencies (pure calculation).

**Methods** (7):
- `__init__(self)`
- `_eval_node(self, node)`
- `calculate(self, metric_name, context)`
- `get_all_derived(self, context)`
- `register_derived(self, name, dependencies, formula)`
- `evaluate_formula(self, formula, values)`
- `_safe_eval(self, node, values)`

### `StatsRollupCore`

Pure statistics rollup calculations (Rust-convertible).

**Methods** (9):
- `__init__(self)`
- `rollup_sum(self, values)`
- `rollup_avg(self, values)`
- `rollup_min(self, values)`
- `rollup_max(self, values)`
- `rollup_p50(self, values)`
- `rollup_p95(self, values)`
- `rollup_p99(self, values)`
- `rollup_stddev(self, values)`

### `CorrelationCore`

Pure correlation analysis (Rust-convertible).

**Methods** (1):
- `calculate_correlation(self, series1, series2)`

### `ABTestCore`

Pure A/B testing calculations (Rust-convertible).

**Methods** (2):
- `calculate_significance(self, control_values, treatment_values)`
- `calculate_sample_size(self, effect_size, alpha, power)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `ast`
- `dataclasses.dataclass`
- `logging`
- `math`
- `operator`
- `rust_core`
- `src.observability.stats.ObservabilityCore.DerivedMetric`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/MetricsCore.improvements.md

# Improvements for MetricsCore

**File**: `src\observability\stats\MetricsCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 593 lines (large)  
**Complexity**: 25 score (complex)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MetricsCore_test.py` with pytest tests

### Code Organization
- [TIP] **7 classes in one file** - Consider splitting into separate modules

### File Complexity
- [!] **Large file** (593 lines) - Consider refactoring

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""MetricsCore - Pure calculation logic for metrics processing.

This module contains all pure computational logic without I/O operations,
making it a candidate for Rust conversion. It handles:
- Token cost calculations
- Metric aggregation and rollup
- Formula evaluation and derived metrics
- Correlation analysis
- Statistical forecasting
- A/B comparison analysis

No I/O operations, no file access, no external calls.
"""

import ast
import logging
import math
import operator
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


@dataclass
class TokenCostResult:
    """
    """
