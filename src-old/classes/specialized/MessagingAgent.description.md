# MessagingAgent

**File**: `src\classes\specialized\MessagingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 38  
**Complexity**: 3 (simple)

## Overview

Agent specializing in messaging platform integration (WhatsApp, Slack, Discord).
Provides a unified interface for external communications.

## Classes (1)

### `MessagingAgent`

**Inherits from**: BaseAgent

Integrates with messaging platforms for fleet notifications.

**Methods** (3):
- `__init__(self, file_path)`
- `send_notification(self, platform, recipient, message)`
- `format_for_mobile(self, report)`

## Dependencies

**Imports** (8):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
