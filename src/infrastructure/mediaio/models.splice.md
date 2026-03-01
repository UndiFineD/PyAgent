# Class Breakdown: models

**File**: `src\infrastructure\mediaio\models.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MediaType`

**Line**: 16  
**Inherits**: Enum  
**Methods**: 0

Supported media types.

[TIP] **Suggested split**: Move to `mediatype.py`

---

### 2. `ImageFormat`

**Line**: 24  
**Inherits**: Enum  
**Methods**: 0

Supported image formats.

[TIP] **Suggested split**: Move to `imageformat.py`

---

### 3. `VideoFormat`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Supported video formats.

[TIP] **Suggested split**: Move to `videoformat.py`

---

### 4. `AudioFormat`

**Line**: 44  
**Inherits**: Enum  
**Methods**: 0

Supported audio formats.

[TIP] **Suggested split**: Move to `audioformat.py`

---

### 5. `ResizeMode`

**Line**: 53  
**Inherits**: Enum  
**Methods**: 0

Image resize modes.

[TIP] **Suggested split**: Move to `resizemode.py`

---

### 6. `MediaMetadata`

**Line**: 63  
**Methods**: 0

Metadata for loaded media.

[TIP] **Suggested split**: Move to `mediametadata.py`

---

### 7. `ImageData`

**Line**: 78  
**Methods**: 3

Loaded image data.

[TIP] **Suggested split**: Move to `imagedata.py`

---

### 8. `VideoData`

**Line**: 102  
**Methods**: 1

Loaded video data.

[TIP] **Suggested split**: Move to `videodata.py`

---

### 9. `AudioData`

**Line**: 115  
**Methods**: 1

Loaded audio data.

[TIP] **Suggested split**: Move to `audiodata.py`

---

### 10. `MediaLoadConfig`

**Line**: 129  
**Methods**: 0

Configuration for media loading.

[TIP] **Suggested split**: Move to `medialoadconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
