# Class Breakdown: voice_agent_orchestrator

**File**: `src\core\base\logic\voice_agent_orchestrator.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `VoiceSession`

**Line**: 47  
**Methods**: 1

Represents an active voice conversation session.

[TIP] **Suggested split**: Move to `voicesession.py`

---

### 2. `VoiceAgentOrchestrator`

**Line**: 70  
**Methods**: 16

Voice-controlled orchestrator for multi-agent systems.

Provides voice interaction capabilities with:
- OpenAI Realtime API integration
- Multi-agent coordination
- Tool-based dispatch system
- Real-t...

[TIP] **Suggested split**: Move to `voiceagentorchestrator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
