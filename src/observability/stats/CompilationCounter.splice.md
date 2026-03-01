# Class Breakdown: CompilationCounter

**File**: `src\observability\stats\CompilationCounter.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CompileEventType`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Types of compilation events.

[TIP] **Suggested split**: Move to `compileeventtype.py`

---

### 2. `CompileEvent`

**Line**: 39  
**Methods**: 1

A compilation event.

[TIP] **Suggested split**: Move to `compileevent.py`

---

### 3. `FunctionStats`

**Line**: 63  
**Methods**: 3

Statistics for a single function.

[TIP] **Suggested split**: Move to `functionstats.py`

---

### 4. `CompilationCounter`

**Line**: 96  
**Methods**: 15

Counter for tracking compilation statistics.

Based on vLLM's compilation counter pattern.

[TIP] **Suggested split**: Move to `compilationcounter.py`

---

### 5. `RecompileTracker`

**Line**: 333  
**Inherits**: CompilationCounter  
**Methods**: 5

Specialized tracker for recompilation.

Beyond vLLM:
- Detects excessive recompilation
- Suggests optimization strategies

[TIP] **Suggested split**: Move to `recompiletracker.py`

---

### 6. `TrendAnalyzer`

**Line**: 423  
**Methods**: 4

Analyze compilation trends over time.

Beyond vLLM:
- Detects degradation patterns
- Predicts future issues

[TIP] **Suggested split**: Move to `trendanalyzer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
