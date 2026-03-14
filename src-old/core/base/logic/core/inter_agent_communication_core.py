#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/inter_agent_communication_core.description.md

# inter_agent_communication_core

**File**: `src\\core\base\\logic\\core\\inter_agent_communication_core.py`  
**Type**: Python Module  
**Summary**: 19 classes, 0 functions, 23 imports  
**Lines**: 589  
**Complexity**: 5 (moderate)

## Overview

Inter-Agent Communication Core

Implements A2A (Agent2Agent) protocol for secure, structured communication between agents.
Based on agentgateway patterns with JSON-RPC messaging, agent cards, and capability negotiation.

Key Features:
- Agent card management with capabilities and authentication
- JSON-RPC based message passing
- Task lifecycle management (create, monitor, cancel)
- Streaming message support
- Security scheme negotiation (OAuth2, JWT, etc.)
- Multi-tenant isolation

## Classes (19)

### `Role`

**Inherits from**: str, Enum

Message role enumeration.

### `TaskState`

**Inherits from**: str, Enum

Task execution states.

### `SecuritySchemeType`

**Inherits from**: str, Enum

Supported security scheme types.

### `MessagePart`

**Inherits from**: BaseModel

Base class for message parts.

### `TextPart`

**Inherits from**: BaseModel

Text content part.

### `FilePart`

**Inherits from**: BaseModel

File content part.

### `DataPart`

**Inherits from**: BaseModel

Structured data part.

### `Message`

**Inherits from**: BaseModel

Agent message with multi-part content.

**Methods** (1):
- `to_dict(self)`

### `AgentCapabilities`

**Inherits from**: BaseModel

Agent capabilities declaration.

### `AgentAuthentication`

**Inherits from**: BaseModel

Agent authentication configuration.

### `AgentCard`

**Inherits from**: BaseModel

Agent capability and configuration card.

### `TaskStatus`

**Inherits from**: BaseModel

Task execution status.

### `Task`

**Inherits from**: BaseModel

Agent task representation.

### `JsonRpcRequest`

**Inherits from**: BaseModel

JSON-RPC request structure.

### `JsonRpcResponse`

**Inherits from**: BaseModel

JSON-RPC response structure.

### `JsonRpcError`

**Inherits from**: BaseModel

JSON-RPC error structure.

### `A2AMessage`

**Inherits from**: BaseModel

A2A protocol message envelope.

### `AgentEndpoint`

**Inherits from**: BaseModel

Agent endpoint configuration.

### `InterAgentCommunicationCore`

**Inherits from**: BaseCore

Core for inter-agent communication using A2A protocol.

Provides secure, structured communication between agents with:
- Agent discovery and capability negotiation
- JSON-RPC based message passing
- Task lifecycle management
- Streaming support
- Security scheme handling

**Methods** (4):
- `__init__(self)`
- `register_message_handler(self, method, handler)`
- `add_security_scheme(self, name, scheme)`
- `get_security_scheme(self, name)`

## Dependencies

**Imports** (23):
- `abc.ABC`
- `abc.abstractmethod`
- `aiohttp`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timezone`
- `enum.Enum`
- `json`
- `pydantic.BaseModel`
- `pydantic.ConfigDict`
- `pydantic.Field`
- `src.core.base.common.base_core.BaseCore`
- `typing.Any`
- ... and 8 more

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/inter_agent_communication_core.improvements.md

# Improvements for inter_agent_communication_core

**File**: `src\\core\base\\logic\\core\\inter_agent_communication_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 589 lines (large)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `inter_agent_communication_core_test.py` with pytest tests

### Code Organization
- [TIP] **19 classes in one file** - Consider splitting into separate modules

### File Complexity
- [!] **Large file** (589 lines) - Consider refactoring

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
Inter-Agent Communication Core

Implements A2A (Agent2Agent) protocol for secure, structured communication between agents.
Based on agentgateway patterns with JSON-RPC messaging, agent cards, and capability negotiation.

Key Features:
- Agent card management with capabilities and authentication
- JSON-RPC based message passing
- Task lifecycle management (create, monitor, cancel)
- Streaming message support
- Security scheme negotiation (OAuth2, JWT, etc.)
- Multi-tenant isolation
"""
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union

import aiohttp
from pydantic import BaseModel, ConfigDict, Field
from src.core.base.common.base_core import BaseCore


class Role(str, Enum):
    """
    """
