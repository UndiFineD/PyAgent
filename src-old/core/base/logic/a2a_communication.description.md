# a2a_communication

**File**: `src\core\base\logic\a2a_communication.py`  
**Type**: Python Module  
**Summary**: 11 classes, 1 functions, 20 imports  
**Lines**: 469  
**Complexity**: 10 (moderate)

## Overview

Inter-Agent Communication System

This module implements Agent-to-Agent (A2A) communication patterns for multi-agent systems.
Provides structured communication protocols, agent discovery, and message routing.

Based on patterns from agentic_design_patterns repository.

## Classes (11)

### `MessageType`

**Inherits from**: Enum

Types of inter-agent messages.

### `AgentCapability`

**Inherits from**: Enum

Standard agent capabilities.

### `AgentSkill`

**Inherits from**: BaseModel

Represents a specific skill an agent can perform.

### `AgentCard`

**Inherits from**: BaseModel

Agent identity and capability card for A2A communication.

**Methods** (1):
- `validate_url(cls, v)`

### `AgentCapabilities`

**Inherits from**: BaseModel

Agent capability flags.

### `A2AMessage`

**Inherits from**: BaseModel

Standard A2A message format.

### `A2AResponse`

**Inherits from**: BaseModel

Standard A2A response format.

### `AgentProtocol`

**Inherits from**: Protocol

Protocol that all agents must implement for A2A communication.

**Methods** (1):
- `agent_card(self)`

### `MessageRouter`

Routes messages between agents in the A2A network.

**Methods** (3):
- `__init__(self)`
- `get_registered_agents(self)`
- `get_agent_card(self, agent_id)`

### `A2ACommunicationMixin`

Mixin class that adds A2A communication capabilities to agents.

**Methods** (3):
- `__init__(self, agent_card, router)`
- `agent_card(self)`
- `register_message_handler(self, message_type, handler)`

### `SimpleA2AAgent`

**Inherits from**: A2ACommunicationMixin

Simple example agent that can respond to basic requests.

**Methods** (1):
- `__init__(self, name, description, capabilities)`

## Functions (1)

### `create_agent_card_from_dict(data)`

Create an AgentCard from a dictionary.

## Dependencies

**Imports** (20):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `json`
- `logging`
- `pydantic.BaseModel`
- `pydantic.Field`
- `pydantic.validator`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- ... and 5 more

---
*Auto-generated documentation*
