# voice_agent_orchestrator

**File**: `src\core\base\logic\voice_agent_orchestrator.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 14 imports  
**Lines**: 459  
**Complexity**: 17 (moderate)

## Overview

Voice Agent Orchestrator - Voice-Controlled Multi-Agent System
===============================================================

Inspired by big-3-super-agent's OpenAIRealtimeVoiceAgent, this orchestrator provides:
- Voice interaction via OpenAI Realtime API
- Multi-agent coordination (voice, coding, browser agents)
- Tool-based dispatch system for agent orchestration
- Real-time conversation management
- Background task processing with status tracking

Key Patterns Extracted from big-3-super-agent:
- OpenAI Realtime API integration for voice interactions
- Tool-based orchestration via function calls
- Multi-agent coordination and lifecycle management
- Real-time audio processing and conversation handling

## Classes (2)

### `VoiceSession`

Represents an active voice conversation session.

**Methods** (1):
- `__post_init__(self)`

### `VoiceAgentOrchestrator`

Voice-controlled orchestrator for multi-agent systems.

Provides voice interaction capabilities with:
- OpenAI Realtime API integration
- Multi-agent coordination
- Tool-based dispatch system
- Real-time conversation management
- Background task processing

**Methods** (16):
- `__init__(self, orchestrator_core, openai_api_key, model)`
- `start_voice_session(self, context)`
- `end_voice_session(self)`
- `process_voice_input(self, audio_data, context)`
- `get_session_status(self)`
- `_process_transcription(self, transcription, context)`
- `_handle_create_agent(self, transcription, context)`
- `_handle_list_agents(self, context)`
- `_handle_run_task(self, transcription, context)`
- `_handle_check_status(self, transcription, context)`
- ... and 6 more methods

## Dependencies

**Imports** (14):
- `asyncio`
- `dataclasses.dataclass`
- `datetime.datetime`
- `datetime.timezone`
- `json`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.logic.multi_agent_orchestrator.MultiAgentOrchestratorCore`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
