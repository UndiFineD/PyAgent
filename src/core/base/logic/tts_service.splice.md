# Class Breakdown: tts_service

**File**: `src\core\base\logic\tts_service.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TTSEngine`

**Line**: 33  
**Inherits**: ABC  
**Methods**: 4

Abstract base class for TTS engines.

[TIP] **Suggested split**: Move to `ttsengine.py`

---

### 2. `CoquiTTSEngine`

**Line**: 62  
**Inherits**: TTSEngine  
**Methods**: 7

Coqui TTS engine implementation.

Inspired by Coqui TTS API patterns.

[TIP] **Suggested split**: Move to `coquittsengine.py`

---

### 3. `TTSService`

**Line**: 192  
**Methods**: 6

Unified Text-to-Speech service.

Provides a single interface for various TTS engines.

[TIP] **Suggested split**: Move to `ttsservice.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
