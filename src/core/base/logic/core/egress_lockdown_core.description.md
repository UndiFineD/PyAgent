# egress_lockdown_core

**File**: `src\core\base\logic\core\egress_lockdown_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 58  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for egress_lockdown_core.

## Classes (1)

### `EgressLockdownCore`

Simulates an egress firewall for agent tools to prevent data exfiltration.
Pattern harvested from agentic-patterns.

**Methods** (4):
- `__init__(self, allowed_domains)`
- `add_allowed_domain(self, domain)`
- `validate_request(self, url)`
- `get_security_policy(self)`

## Dependencies

**Imports** (5):
- `re`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
