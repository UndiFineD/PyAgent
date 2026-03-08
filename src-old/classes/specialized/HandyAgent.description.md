# HandyAgent

**File**: `src\classes\specialized\HandyAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 48  
**Complexity**: 1 (simple)

## Overview

Agent specializing in terminal-native interactions and context-aware shell execution.
Inspired by the Handy pattern (Rust terminal agent) and GitHub Copilot CLI.

## Classes (1)

### `HandyAgent`

**Inherits from**: BaseAgent, HandyFileSystemMixin, HandyTerminalMixin, HandyCoreMixin

Provides a terminal-native interface for the agent to interact with the OS.

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `mixins.HandyCoreMixin.HandyCoreMixin`
- `mixins.HandyFileSystemMixin.HandyFileSystemMixin`
- `mixins.HandyTerminalMixin.HandyTerminalMixin`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`

---
*Auto-generated documentation*
