# Class Breakdown: ad_monitoring_core

**File**: `src\core\base\logic\core\ad_monitoring_core.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ChangeType`

**Line**: 51  
**Inherits**: Enum  
**Methods**: 0

Types of AD object changes

[TIP] **Suggested split**: Move to `changetype.py`

---

### 2. `AttributeChangeType`

**Line**: 59  
**Inherits**: Enum  
**Methods**: 0

Types of attribute changes

[TIP] **Suggested split**: Move to `attributechangetype.py`

---

### 3. `SecurityEventType`

**Line**: 66  
**Inherits**: Enum  
**Methods**: 0

Security-relevant event types

[TIP] **Suggested split**: Move to `securityeventtype.py`

---

### 4. `ADObjectChange`

**Line**: 78  
**Methods**: 0

Represents a change to an Active Directory object

[TIP] **Suggested split**: Move to `adobjectchange.py`

---

### 5. `AttributeChange`

**Line**: 95  
**Methods**: 0

Represents a change to a specific attribute

[TIP] **Suggested split**: Move to `attributechange.py`

---

### 6. `MonitoringSession`

**Line**: 108  
**Methods**: 0

Active Directory monitoring session

[TIP] **Suggested split**: Move to `monitoringsession.py`

---

### 7. `MonitoringConfig`

**Line**: 123  
**Methods**: 0

Configuration for AD monitoring

[TIP] **Suggested split**: Move to `monitoringconfig.py`

---

### 8. `ADConnectionProvider`

**Line**: 137  
**Inherits**: Protocol  
**Methods**: 0

Protocol for Active Directory connection providers

[TIP] **Suggested split**: Move to `adconnectionprovider.py`

---

### 9. `AlertProvider`

**Line**: 161  
**Inherits**: Protocol  
**Methods**: 0

Protocol for alert/notification providers

[TIP] **Suggested split**: Move to `alertprovider.py`

---

### 10. `ADMonitoringCore`

**Line**: 173  
**Inherits**: BaseCore  
**Methods**: 23

Active Directory Monitoring Core

Provides real-time monitoring of Active Directory changes using USN-based detection,
inspired by ADSpider's approach to efficient AD monitoring.

Key Capabilities:
- ...

[TIP] **Suggested split**: Move to `admonitoringcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
