# Class Breakdown: rust_profiler

**File**: `src\observability\profiling\rust_profiler.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FunctionStats`

**Line**: 38  
**Methods**: 3

Statistics for a single Rust function.

[TIP] **Suggested split**: Move to `functionstats.py`

---

### 2. `RustProfiler`

**Line**: 61  
**Methods**: 11

Singleton profiler for tracking Rust function usage.
Thread-safe and designed for production use.

[TIP] **Suggested split**: Move to `rustprofiler.py`

---

### 3. `RustUsageScanner`

**Line**: 406  
**Methods**: 6

Scans Python source files for Rust function usage.

[TIP] **Suggested split**: Move to `rustusagescanner.py`

---

### 4. `ProfiledRustCore`

**Line**: 550  
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
