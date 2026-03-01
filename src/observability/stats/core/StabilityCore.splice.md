# Class Breakdown: StabilityCore

**File**: `src\observability\stats\core\StabilityCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FleetMetrics`

**Line**: 7  
**Methods**: 0

[TIP] **Suggested split**: Move to `fleetmetrics.py`

---

### 2. `StabilityCore`

**Line**: 13  
**Methods**: 3

Pure logic for calculating fleet stability and reasoning coherence.
Integrates SAE activation metrics and error trends into a unified score.

[TIP] **Suggested split**: Move to `stabilitycore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
