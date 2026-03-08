# Class Breakdown: ai_talking_head_core

**File**: `src\core\base\logic\core\ai_talking_head_core.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TalkingHeadRequest`

**Line**: 32  
**Methods**: 0

Request for talking head video generation

[TIP] **Suggested split**: Move to `talkingheadrequest.py`

---

### 2. `TalkingHeadResult`

**Line**: 44  
**Methods**: 0

Result of talking head generation

[TIP] **Suggested split**: Move to `talkingheadresult.py`

---

### 3. `FaceAlignmentResult`

**Line**: 56  
**Methods**: 0

Face alignment and pose estimation result

[TIP] **Suggested split**: Move to `facealignmentresult.py`

---

### 4. `AudioFeatures`

**Line**: 65  
**Methods**: 0

Extracted audio features for lip sync

[TIP] **Suggested split**: Move to `audiofeatures.py`

---

### 5. `AITalkingHeadCore`

**Line**: 74  
**Inherits**: BaseCore  
**Methods**: 1

AI Talking Head Core for audio-visual controlled video generation.

Provides capabilities for generating natural talking head videos from audio,
text, and reference images using advanced diffusion and...

[TIP] **Suggested split**: Move to `aitalkingheadcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
