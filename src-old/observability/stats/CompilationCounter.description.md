# CompilationCounter

**File**: `src\observability\stats\CompilationCounter.py`  
**Type**: Python Module  
**Summary**: 6 classes, 2 functions, 17 imports  
**Lines**: 499  
**Complexity**: 30 (complex)

## Overview

CompilationCounter - Statistics and counters for compilation metrics.

Implements vLLM's compilation counting patterns:
- Track compilation events
- Monitor recompilation rates
- Shape distribution analysis
- Backend performance tracking

Beyond vLLM:
- Real-time metrics emission
- Anomaly detection
- Trend analysis

## Classes (6)

### `CompileEventType`

**Inherits from**: Enum

Types of compilation events.

### `CompileEvent`

A compilation event.

**Methods** (1):
- `to_dict(self)`

### `FunctionStats`

Statistics for a single function.

**Methods** (3):
- `unique_shapes(self)`
- `avg_compile_time(self)`
- `recompile_ratio(self)`

### `CompilationCounter`

Counter for tracking compilation statistics.

Based on vLLM's compilation counter pattern.

**Methods** (15):
- `__init__(self, name, max_events, emit_interval)`
- `record_compile(self, function_id, shape, duration, backend)`
- `record_recompile(self, function_id, shape, duration, backend)`
- `record_cache_hit(self, function_id, shape)`
- `record_fallback(self, function_id, shape, reason)`
- `record_error(self, function_id, shape, error)`
- `_add_event(self, event)`
- `_get_or_create_stats(self, function_id)`
- `get_summary(self)`
- `get_function_stats(self, function_id)`
- ... and 5 more methods

### `RecompileTracker`

**Inherits from**: CompilationCounter

Specialized tracker for recompilation.

Beyond vLLM:
- Detects excessive recompilation
- Suggests optimization strategies

**Methods** (5):
- `__init__(self, max_recompiles, alert_threshold)`
- `record_recompile(self, function_id, shape, duration, backend)`
- `_add_alert(self, function_id, alert_type, message)`
- `get_alerts(self)`
- `get_optimization_suggestions(self)`

### `TrendAnalyzer`

Analyze compilation trends over time.

Beyond vLLM:
- Detects degradation patterns
- Predicts future issues

**Methods** (4):
- `__init__(self, window_size)`
- `add_sample(self, compile_time)`
- `get_trend(self)`
- `get_stats(self)`

## Functions (2)

### `get_global_counter()`

Get or create global compilation counter.

### `reset_global_counter()`

Reset global counter.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `collections.Counter`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
