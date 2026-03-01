# Class Breakdown: bash_core

**File**: `src\logic\agents\development\core\bash_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ShellCheckIssue`

**Line**: 33  
**Inherits**: TypedDict  
**Methods**: 0

Represents a single issue found by shellcheck.

[TIP] **Suggested split**: Move to `shellcheckissue.py`

---

### 2. `BashLintResult`

**Line**: 49  
**Inherits**: TypedDict  
**Methods**: 0

Result of a bash script linting session.

[TIP] **Suggested split**: Move to `bashlintresult.py`

---

### 3. `BashCore`

**Line**: 57  
**Methods**: 2

Core logic for Bash script analysis and linting.

[TIP] **Suggested split**: Move to `bashcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
