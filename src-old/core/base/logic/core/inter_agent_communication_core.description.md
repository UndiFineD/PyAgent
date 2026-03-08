# inter_agent_communication_core

**File**: `src\core\base\logic\core\inter_agent_communication_core.py`  
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
