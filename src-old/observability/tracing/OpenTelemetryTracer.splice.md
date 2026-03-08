# Class Breakdown: OpenTelemetryTracer

**File**: `src\observability\tracing\OpenTelemetryTracer.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SpanAttributes`

**Line**: 93  
**Methods**: 0

Standard span attribute names for LLM and AI operations.

Based on OpenTelemetry semantic conventions for GenAI.

[TIP] **Suggested split**: Move to `spanattributes.py`

---

### 2. `SpanTiming`

**Line**: 466  
**Methods**: 4

Helper for tracking timing within a span.

[TIP] **Suggested split**: Move to `spantiming.py`

---

### 3. `NullSpan`

**Line**: 523  
**Methods**: 7

A no-op span for testing or when tracing is disabled.

[TIP] **Suggested split**: Move to `nullspan.py`

---

### 4. `NullTracer`

**Line**: 548  
**Methods**: 2

A no-op tracer for testing or when tracing is disabled.

[TIP] **Suggested split**: Move to `nulltracer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
