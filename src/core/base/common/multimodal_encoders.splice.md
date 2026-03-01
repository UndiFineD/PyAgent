# Class Breakdown: multimodal_encoders

**File**: `src\core\base\common\multimodal_encoders.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StreamingVisionEncoder`

**Line**: 25  
**Methods**: 4

Handles efficient vision streaming using adaptive delta compression.
Only sends changed pixels between frames to conserve bandwidth.
Adjusts sensitivity based on scene dynamics (entropy).

[TIP] **Suggested split**: Move to `streamingvisionencoder.py`

---

### 2. `StreamingAudioProcessor`

**Line**: 69  
**Methods**: 2

Stateful processor for continuous audio streams.
Handles rolling buffers, VAD, and feature extraction.

[TIP] **Suggested split**: Move to `streamingaudioprocessor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
