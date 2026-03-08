# video_fragment_core

**File**: `src\core\base\logic\core\video_fragment_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 62  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for video_fragment_core.

## Classes (1)

### `VideoFragmentCore`

Handles fragmentation of long-form video files into overlapping clips for multimodal reasoning.
Harvested from .external/AskVideos-VideoCLIP

**Methods** (3):
- `__init__(self, clip_len, overlap)`
- `fragment_video(self, video_path, output_dir)`
- `aggregate_fragments(self, fragment_results)`

## Dependencies

**Imports** (4):
- `os`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
