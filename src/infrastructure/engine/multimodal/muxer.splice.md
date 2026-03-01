# Class Breakdown: muxer

**File**: `src\infrastructure\engine\multimodal\muxer.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ChannelType`

**Line**: 36  
**Inherits**: Enum  
**Methods**: 0

Enumeration of supported modality channel types.

[TIP] **Suggested split**: Move to `channeltype.py`

---

### 2. `ModalityChannel`

**Line**: 45  
**Methods**: 0

Configuration for a specific modality streaming channel.

[TIP] **Suggested split**: Move to `modalitychannel.py`

---

### 3. `Muxer`

**Line**: 53  
**Methods**: 6

Coordinates multiple high-speed modality channels.
Supports "DVD-style" separate streams for video, audio, and text.

[TIP] **Suggested split**: Move to `muxer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
