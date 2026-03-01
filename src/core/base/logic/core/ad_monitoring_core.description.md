# ad_monitoring_core

**File**: `src\core\base\logic\core\ad_monitoring_core.py`  
**Type**: Python Module  
**Summary**: 10 classes, 0 functions, 24 imports  
**Lines**: 777  
**Complexity**: 23 (complex)

## Overview

Active Directory Monitoring Core

This core implements real-time Active Directory change monitoring patterns inspired by ADSpider.
It provides comprehensive AD security monitoring using Update Sequence Numbers (USN) and replication metadata.

Key Features:
- Real-time AD change monitoring without full object enumeration
- USN-based change detection and filtering
- Human-readable change explanations
- Security-focused attribute monitoring
- Configurable filtering and alerting
- Historical change tracking
- Integration with security incident response workflows

## Classes (10)

### `ChangeType`

**Inherits from**: Enum

Types of AD object changes

### `AttributeChangeType`

**Inherits from**: Enum

Types of attribute changes

### `SecurityEventType`

**Inherits from**: Enum

Security-relevant event types

### `ADObjectChange`

Represents a change to an Active Directory object

### `AttributeChange`

Represents a change to a specific attribute

### `MonitoringSession`

Active Directory monitoring session

### `MonitoringConfig`

Configuration for AD monitoring

### `ADConnectionProvider`

**Inherits from**: Protocol

Protocol for Active Directory connection providers

### `AlertProvider`

**Inherits from**: Protocol

Protocol for alert/notification providers

### `ADMonitoringCore`

**Inherits from**: BaseCore

Active Directory Monitoring Core

Provides real-time monitoring of Active Directory changes using USN-based detection,
inspired by ADSpider's approach to efficient AD monitoring.

Key Capabilities:
- USN-based change detection without full enumeration
- Security-focused attribute monitoring
- Human-readable change explanations
- Configurable alerting and filtering
- Historical change tracking and analysis
- Integration with security incident response

**Methods** (23):
- `__init__(self, config)`
- `_initialize_core(self)`
- `_load_monitoring_config(self)`
- `_initialize_security_rules(self)`
- `_monitoring_loop(self)`
- `_analyze_attribute_change(self, attr_name, attr_data)`
- `_detect_security_event(self, attr_name, change)`
- `_generate_change_explanation(self, changes)`
- `_explain_attribute_change(self, attr_name, new_value, old_value)`
- `_explain_uac_change(self, new_value, old_value)`
- ... and 13 more methods

## Dependencies

**Imports** (24):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `json`
- `logging`
- `src.core.base.common.base_core.BaseCore`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.state.agent_state_manager.StateTransaction`
- `threading`
- `time`
- ... and 9 more

---
*Auto-generated documentation*
