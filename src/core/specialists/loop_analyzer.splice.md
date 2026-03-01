# Class Breakdown: loop_analyzer

**File**: `src\core\specialists\loop_analyzer.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LoopAnalysisResult`

**Line**: 32  
**Methods**: 0

Result of loop analysis for a single file.

[TIP] **Suggested split**: Move to `loopanalysisresult.py`

---

### 2. `LoopAnalysisConfig`

**Line**: 45  
**Methods**: 1

Configuration for loop analysis.

[TIP] **Suggested split**: Move to `loopanalysisconfig.py`

---

### 3. `LoopAnalyzer`

**Line**: 64  
**Methods**: 11

Reusable analyzer for detecting loop anti-patterns.

[TIP] **Suggested split**: Move to `loopanalyzer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
