# credential_extraction_agent

**File**: `src\core\agents\credential_extraction_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 152  
**Complexity**: 1 (simple)

## Overview

Module: credential_extraction_agent
Agent for extracting credentials from Windows systems.
Implements patterns from ADSyncDump-BOF for Azure AD Connect credential extraction.

## Classes (1)

### `CredentialExtractionAgent`

**Inherits from**: BaseAgent, PrivilegeEscalationMixin, DatabaseAccessMixin, CryptoMixin, DataParsingMixin

Agent for extracting credentials using Windows-specific techniques.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `platform`
- `src.core.base.base_agent.BaseAgent`
- `src.core.base.mixins.crypto_mixin.CryptoMixin`
- `src.core.base.mixins.data_parsing_mixin.DataParsingMixin`
- `src.core.base.mixins.database_access_mixin.DatabaseAccessMixin`
- `src.core.base.mixins.privilege_escalation_mixin.PrivilegeEscalationMixin`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Tuple`
- `uuid.UUID`

---
*Auto-generated documentation*
