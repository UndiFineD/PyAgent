# ad_connect_security_core

**File**: `src\core\base\logic\core\ad_connect_security_core.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 27 imports  
**Lines**: 708  
**Complexity**: 4 (simple)

## Overview

Azure AD Connect Security Core

This core implements Azure AD Connect security analysis patterns inspired by ADSyncDump-BOF.
It provides comprehensive security assessment for Azure AD Connect deployments including
credential analysis, configuration security, and synchronization monitoring.

Key Features:
- Azure AD Connect service account analysis
- Synchronization database security assessment
- Credential encryption validation
- Configuration security auditing
- Service account privilege analysis
- Synchronization health monitoring
- Security vulnerability detection
- Compliance reporting for AD Connect deployments

## Classes (5)

### `ADConnectServiceAccount`

Represents an Azure AD Connect service account.

### `ADConnectDatabase`

Represents Azure AD Connect database information.

### `ADConnectConfiguration`

Represents Azure AD Connect configuration settings.

### `ADConnectSecurityAssessment`

Security assessment results for Azure AD Connect.

### `ADConnectSecurityCore`

**Inherits from**: BaseCore

Core for Azure AD Connect security analysis and assessment.

This core provides comprehensive security analysis for Azure AD Connect deployments,
including service account analysis, database security, configuration auditing,
and vulnerability detection.

**Methods** (4):
- `__init__(self)`
- `_calculate_risk_level(self, score)`
- `get_capabilities(self)`
- `get_supported_task_types(self)`

## Dependencies

**Imports** (27):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `json`
- `logging`
- `os`
- `platform`
- `re`
- `src.core.base.common.base_core.BaseCore`
- `src.core.base.common.models.communication_models.CascadeContext`
- ... and 12 more

---
*Auto-generated documentation*
