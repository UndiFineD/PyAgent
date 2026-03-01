# InfrastructureManagerAgent

**File**: `src\classes\specialized\InfrastructureManagerAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 96  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in infrastructure management, Proxmox orchestration, and HomeAssistant IoT control.
Provides tools for remote system administration and automated environment scaling.

## Classes (1)

### `InfrastructureManagerAgent`

**Inherits from**: BaseAgent

Manages remote infrastructure including Proxmox virtualization and HomeAssistant IoT.

**Methods** (5):
- `__init__(self, file_path)`
- `list_proxmox_vms(self, host, token_id, secret)`
- `control_homeassistant_device(self, entity_id, action, api_url, token)`
- `get_system_metrics(self, server_ip)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
