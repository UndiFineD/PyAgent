# Class Breakdown: cosy_voice_agent

**File**: `src\logic\agents\multimodal\cosy_voice_agent.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CosyVoiceConfig`

**Line**: 42  
**Methods**: 0

Configuration for the CosyVoice model.

[TIP] **Suggested split**: Move to `cosyvoiceconfig.py`

---

### 2. `CosyVoiceAgent`

**Line**: 49  
**Inherits**: BaseAgent  
**Methods**: 4

Orchestrates the lifecycle of CosyVoice generation.
Handles model loading, unloading, and inference requests.

[TIP] **Suggested split**: Move to `cosyvoiceagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
