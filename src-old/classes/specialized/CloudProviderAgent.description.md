# CloudProviderAgent

**File**: `src\classes\specialized\CloudProviderAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 49  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for CloudProviderAgent.

## Classes (1)

### `CloudProviderAgent`

**Inherits from**: BaseAgent

Phase 56: Multi-Cloud Infrastructure as Code.
Manages cloud credentials, region selection, and generates IaC templates.

**Methods** (4):
- `__init__(self, path)`
- `configure_provider(self, provider, credentials_mock)`
- `generate_terraform_template(self, provider, node_count, region)`
- `select_optimal_region(self, latency_data)`

## Dependencies

**Imports** (7):
- `json`
- `os`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
