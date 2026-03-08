# video_analyzer_core

**File**: `src\core\base\logic\core\video_analyzer_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 56  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for video_analyzer_core.

## Classes (1)

### `VideoAnalyzerCore`

Core logic for fragmenting and preparing video data for multi-modal inference.
Harvested from .external/AskVideos-VideoCLIP.

**Methods** (4):
- `__init__(self, frame_count, target_dim)`
- `segment_long_video(self, total_duration, segment_length)`
- `sample_frames(self, frames, n_samples)`
- `get_token_budget_ratio(self, width, height)`

## Dependencies

**Imports** (3):
- `math`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
