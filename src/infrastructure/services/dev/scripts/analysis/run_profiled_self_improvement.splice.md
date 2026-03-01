# Class Breakdown: run_profiled_self_improvement

**File**: `src\infrastructure\services\dev\scripts\analysis\run_profiled_self_improvement.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RustFunctionStats`

**Line**: 53  
**Methods**: 2

Statistics for a Rust function.

[TIP] **Suggested split**: Move to `rustfunctionstats.py`

---

### 2. `RustProfiler`

**Line**: 69  
**Methods**: 3

Profiler specifically for rust_core function calls.

[TIP] **Suggested split**: Move to `rustprofiler.py`

---

### 3. `ComprehensiveProfileAnalyzer`

**Line**: 128  
**Methods**: 7

Analyzes cProfile results and filters for src/ code.

[TIP] **Suggested split**: Move to `comprehensiveprofileanalyzer.py`

---

### 4. `ProfiledRustCore`

**Line**: 96  
**Methods**: 1

Wrapper that profiles all rust_core function calls.

[TIP] **Suggested split**: Move to `profiledrustcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
