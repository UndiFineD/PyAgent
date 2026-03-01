# c2_framework_core

**File**: `src\core\base\logic\core\c2_framework_core.py`  
**Type**: Python Module  
**Summary**: 13 classes, 0 functions, 20 imports  
**Lines**: 805  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for c2_framework_core.

## Classes (13)

### `CommunicationProtocol`

**Inherits from**: Enum

C2 communication protocols

### `AgentStatus`

**Inherits from**: Enum

Agent status states

### `TaskStatus`

**Inherits from**: Enum

Task execution status

### `ListenerType`

**Inherits from**: Enum

Listener types

### `C2Profile`

C2 server profile configuration

### `C2Agent`

C2 agent representation

### `C2Listener`

C2 listener configuration

### `C2Task`

C2 task/job representation

### `C2Extender`

C2 extender/plugin

### `C2Session`

C2 operator session

### `C2Tunnel`

C2 tunnel for pivoting/port forwarding

### `C2Framework`

Complete C2 framework state

### `C2FrameworkCore`

C2 Framework Core for command and control operations.

Provides comprehensive C2 capabilities including agent management,
task scheduling, listener operations, and post-exploitation workflows.

**Methods** (3):
- `__init__(self)`
- `_hash_password(self, password)`
- `_verify_password(self, password, hash_string)`

## Dependencies

**Imports** (20):
- `asyncio`
- `base64`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `secrets`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 5 more

---
*Auto-generated documentation*
