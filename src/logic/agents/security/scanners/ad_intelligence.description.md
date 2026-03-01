# ad_intelligence

**File**: `src\logic\agents\security\scanners\ad_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 236  
**Complexity**: 17 (moderate)

## Overview

Python module containing implementation for ad_intelligence.

## Classes (1)

### `ADIntelligence`

Intelligence engine for Active Directory enumeration and exploitation.

**Methods** (17):
- `get_certificate_abuse_scenarios()`
- `get_replication_rights_guids()`
- `get_weak_permission_abuse_types()`
- `generate_certex_command(action, target, template, cert_path)`
- `get_sensitive_spns()`
- `get_laps_attributes()`
- `get_sccm_vulnerability_indicators()`
- `get_gpo_abuse_indicators()`
- `get_bitlocker_recovery_attributes()`
- `get_bitlocker_ldap_query()`
- ... and 7 more methods

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
