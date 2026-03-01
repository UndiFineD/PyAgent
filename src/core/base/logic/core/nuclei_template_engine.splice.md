# Class Breakdown: nuclei_template_engine

**File**: `src\core\base\logic\core\nuclei_template_engine.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TemplateInfo`

**Line**: 34  
**Methods**: 0

Template metadata

[TIP] **Suggested split**: Move to `templateinfo.py`

---

### 2. `TemplateRequest`

**Line**: 45  
**Methods**: 0

HTTP request specification

[TIP] **Suggested split**: Move to `templaterequest.py`

---

### 3. `MatcherCondition`

**Line**: 54  
**Methods**: 0

Matcher condition specification

[TIP] **Suggested split**: Move to `matchercondition.py`

---

### 4. `TemplateHTTP`

**Line**: 66  
**Methods**: 0

HTTP template specification

[TIP] **Suggested split**: Move to `templatehttp.py`

---

### 5. `NucleiTemplate`

**Line**: 74  
**Methods**: 0

Complete Nuclei template

[TIP] **Suggested split**: Move to `nucleitemplate.py`

---

### 6. `ScanResult`

**Line**: 82  
**Methods**: 0

Result from template execution

[TIP] **Suggested split**: Move to `scanresult.py`

---

### 7. `NucleiTemplateEngine`

**Line**: 93  
**Methods**: 10

Nuclei-style vulnerability detection engine.

Based on patterns from .external/0day-templates repository.

[TIP] **Suggested split**: Move to `nucleitemplateengine.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
