# voice_agent_orchestrator

**File**: `src\logic\agents\voice\voice_agent_orchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 24 imports  
**Lines**: 321  
**Complexity**: 9 (moderate)

## Overview

Voice Agent Orchestrator - Multi-modal agent coordination
========================================================

Inspired by big-3-super-agent's sophisticated orchestration system.
Provides voice-controlled coordination of multiple specialized agents.

Key Features:
- OpenAI Realtime API integration for voice I/O
- Multi-agent orchestration (coding, browser, analysis agents)
- Tool calling infrastructure
- Cost and token tracking
- Real-time audio processing

## Classes (1)

### `VoiceAgentOrchestrator`

**Inherits from**: BaseAgent

Voice-controlled multi-agent orchestrator inspired by big-3-super-agent.

Coordinates voice interactions with specialized agents for:
- Code generation and editing
- Web browsing and automation
- Data analysis and research
- Real-time conversation

**Methods** (9):
- `__init__(self)`
- `register_agent(self, name, agent)`
- `_build_tool_specs(self)`
- `setup_audio(self)`
- `cleanup_audio(self)`
- `base64_encode_audio(self, audio_bytes)`
- `base64_decode_audio(self, base64_str)`
- `_log_panel(self, message, title, style)`
- `get_status(self)`

## Dependencies

**Imports** (24):
- `asyncio`
- `base64`
- `datetime.datetime`
- `datetime.timezone`
- `json`
- `logging`
- `numpy`
- `os`
- `pathlib.Path`
- `pyaudio`
- `rich.console.Console`
- `rich.panel.Panel`
- `rich.table.Table`
- `src.core.base.base_agent.BaseAgent`
- `src.core.base.models.communication_models.CascadeContext`
- ... and 9 more

---
*Auto-generated documentation*
