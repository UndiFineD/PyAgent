# devops_intelligence

**File**: `src\logic\agents\security\scanners\devops_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 123  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for devops_intelligence.

## Classes (1)

### `DevOpsIntelligence`

Handles discovery and exploitation of DevOps & Management infrastructure.
Integrates logic from SCMKit, sccm-http-looter, and CI/CD attack tools.

**Methods** (6):
- `__init__(self)`
- `get_scm_recon_endpoints(self, base_url, provider)`
- `get_sccm_looting_paths(self, base_url)`
- `get_sccm_sensitive_extensions(self)`
- `get_ci_cd_attack_patterns(self)`
- `get_github_runner_attack_vectors(self)`

## Dependencies

**Imports** (7):
- `aiohttp`
- `asyncio`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
