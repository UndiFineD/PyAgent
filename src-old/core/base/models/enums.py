#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/models/enums.description.md

# enums

**File**: `src\core\base\models\enums.py`  
**Type**: Python Module  
**Summary**: 17 classes, 0 functions, 3 imports  
**Lines**: 155  
**Complexity**: 0 (simple)

## Overview

Enum definitions for PyAgent models.

## Classes (17)

### `AgentState`

**Inherits from**: Enum

Agent lifecycle states.

### `ResponseQuality`

**Inherits from**: Enum

AI response quality levels.

### `EventType`

**Inherits from**: Enum

Agent event types for hooks.

### `AuthMethod`

**Inherits from**: Enum

Authentication methods for backends.

### `SerializationFormat`

**Inherits from**: Enum

Custom serialization formats.

### `FilePriority`

**Inherits from**: Enum

File priority levels for request prioritization.

### `InputType`

**Inherits from**: Enum

Input types for multimodal support.

### `AgentType`

**Inherits from**: Enum

Agent type classifications.

### `MessageRole`

**Inherits from**: Enum

Roles for conversation messages.

### `AgentEvent`

**Inherits from**: Enum

Agent event types.

### `AgentExecutionState`

**Inherits from**: Enum

Execution state for an agent run.

### `AgentPriority`

**Inherits from**: Enum

Priority level for agent execution.

### `ConfigFormat`

**Inherits from**: Enum

Configuration file format.

### `DiffOutputFormat`

**Inherits from**: Enum

Output format for diff preview.

### `HealthStatus`

**Inherits from**: Enum

Health status for components.

### `LockType`

**Inherits from**: Enum

File locking type.

### `RateLimitStrategy`

**Inherits from**: Enum

Rate limiting strategy for API calls.

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `enum.Enum`
- `enum.auto`

---
*Auto-generated documentation*
## Source: src-old/core/base/models/enums.improvements.md

# Improvements for enums

**File**: `src\core\base\models\enums.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 155 lines (medium)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `enums_test.py` with pytest tests

### Code Organization
- [TIP] **17 classes in one file** - Consider splitting into separate modules

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

from __future__ import annotations
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

"""Enum definitions for PyAgent models."""

from enum import Enum, auto

class AgentState(Enum):
    """Agent lifecycle states."""
    INITIALIZED = "initialized"
    IDLE = "idle"
    READING = "reading"
    PROCESSING = "processing"
    THINKING = "thinking"
    SIMULATING = "simulating"
    WRITING = "writing"
    COMPLETED = "completed"
    ERROR = "error"

class ResponseQuality(Enum):
    """AI response quality levels."""
    EXCELLENT = 5
    GOOD = 4
    ACCEPTABLE = 3
    POOR = 2
    INVALID = 1

class EventType(Enum):
    """Agent event types for hooks."""
    PRE_READ = "pre_read"
    POST_READ = "post_read"
    PRE_IMPROVE = "pre_improve"
    POST_IMPROVE = "post_improve"
    PRE_WRITE = "pre_write"
    POST_WRITE = "post_write"
    ERROR = "error"

class AuthMethod(Enum):
    """Authentication methods for backends."""
    NONE = "none"
    API_KEY = "api_key"
    TOKEN = "token"
    BEARER_TOKEN = "bearer_token"
    BASIC_AUTH = "basic_auth"
    OAUTH2 = "oauth2"
    CUSTOM = "custom"

class SerializationFormat(Enum):
    """Custom serialization formats."""
    JSON = "json"
    YAML = "yaml"
    MSGPACK = "msgpack"
    PICKLE = "pickle"
    PROTOBUF = "protobuf"
    CBOR = "cbor"

class FilePriority(Enum):
    """File priority levels for request prioritization."""
    CRITICAL = 5
    HIGH = 4
    NORMAL = 3
    LOW = 2
    BACKGROUND = 1

class InputType(Enum):
    """Input types for multimodal support."""
    TEXT = "text"
    IMAGE = "image"
    DIAGRAM = "diagram"
    CODE = "code"
    AUDIO = "audio"
    VIDEO = "video"

class AgentType(Enum):
    """Agent type classifications."""
    GENERAL = "general"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REFACTORING = "refactoring"

class MessageRole(Enum):
    """Roles for conversation messages."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class AgentEvent(Enum):
    """Agent event types."""
    START = "start"
    COMPLETE = "complete"
    ERROR = "error"

class AgentExecutionState(Enum):
    """Execution state for an agent run."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    PAUSED = auto()

class AgentPriority(Enum):
    """Priority level for agent execution."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5

class ConfigFormat(Enum):
    """Configuration file format."""
    YAML = auto()
    TOML = auto()
    JSON = auto()
    INI = auto()

class DiffOutputFormat(Enum):
    """Output format for diff preview."""
    UNIFIED = auto()      # Unified diff format
    CONTEXT = auto()      # Context diff format
    SIDE_BY_SIDE = auto()  # Side by side diff
    HTML = auto()         # HTML formatted diff

class HealthStatus(Enum):
    """Health status for components."""
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()

class LockType(Enum):
    """File locking type."""
    SHARED = auto()       # Multiple readers allowed
    EXCLUSIVE = auto()    # Single writer only
    ADVISORY = auto()     # Advisory lock (not enforced by OS)

class RateLimitStrategy(Enum):
    """Rate limiting strategy for API calls."""
    FIXED_WINDOW = auto()      # Fixed time window rate limiting
    SLIDING_WINDOW = auto()    # Sliding window rate limiting
    TOKEN_BUCKET = auto()      # Token bucket algorithm
    LEAKY_BUCKET = auto()      # Leaky bucket algorithm
