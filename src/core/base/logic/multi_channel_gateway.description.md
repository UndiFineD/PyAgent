# multi_channel_gateway

**File**: `src\core\base\logic\multi_channel_gateway.py`  
**Type**: Python Module  
**Summary**: 9 classes, 0 functions, 20 imports  
**Lines**: 430  
**Complexity**: 6 (moderate)

## Overview

Multi-Channel Messaging Gateway Core

Inspired by OpenClaw's sophisticated gateway architecture, this module provides
a WebSocket-based control plane for multi-channel agent communication with session
routing, presence management, and channel abstraction.

Key Features:
- WebSocket control plane for real-time agent coordination
- Multi-channel support (WhatsApp, Telegram, Discord, Slack, etc.)
- Session-based routing with isolation and activation modes
- Presence management and typing indicators
- Channel abstraction with provider-agnostic messaging
- Tool execution coordination across channels

## Classes (9)

### `ChannelType`

**Inherits from**: Enum

Supported messaging channel types.

### `MessageType`

**Inherits from**: Enum

Types of messages in the gateway protocol.

### `SessionActivationMode`

**Inherits from**: Enum

How sessions are activated in channels.

### `ChannelMessage`

Represents a message from any channel.

### `GatewayPresence`

Presence information for gateway clients.

### `ChannelProvider`

**Inherits from**: ABC

Abstract base class for channel providers.

**Methods** (1):
- `channel_type(self)`

### `GatewaySession`

**Inherits from**: BaseModel

Represents an agent session in the gateway.

### `GatewayProtocol`

WebSocket protocol for gateway communication.

**Methods** (1):
- `__init__(self)`

### `MultiChannelGatewayCore`

Core gateway for multi-channel agent communication.

Provides WebSocket-based control plane with session management,
presence tracking, and channel abstraction.

**Methods** (4):
- `__init__(self, host, port)`
- `register_channel_provider(self, provider)`
- `get_active_sessions(self)`
- `get_sessions_by_channel(self, channel_type, channel_id)`

## Dependencies

**Imports** (20):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `pydantic.BaseModel`
- `pydantic.Field`
- `src.core.base.common.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 5 more

---
*Auto-generated documentation*
