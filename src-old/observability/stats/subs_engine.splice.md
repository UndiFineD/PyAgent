# Class Breakdown: subs_engine

**File**: `src\observability\stats\subs_engine.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AnnotationManager`

**Line**: 23  
**Methods**: 5

Manage metric annotations and comments.

[TIP] **Suggested split**: Move to `annotationmanager.py`

---

### 2. `StatsAnnotationManager`

**Line**: 72  
**Methods**: 3

Manages annotations on metrics (backward compat).

[TIP] **Suggested split**: Move to `statsannotationmanager.py`

---

### 3. `SubscriptionManager`

**Line**: 97  
**Methods**: 5

Manage metric subscriptions and change notifications.

[TIP] **Suggested split**: Move to `subscriptionmanager.py`

---

### 4. `StatsSubscriptionManager`

**Line**: 149  
**Methods**: 5

Manages metric subscriptions (backward compat).

[TIP] **Suggested split**: Move to `statssubscriptionmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
