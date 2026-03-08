# MultiModalContextAgent

**File**: `src\classes\specialized\MultiModalContextAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 20 imports  
**Lines**: 299  
**Complexity**: 9 (moderate)

## Overview

Agent specializing in visual context, UI analysis, and multimodal reasoning.
Used for interpreting screenshots, diagrams, and vision-based UI testing.

## Classes (1)

### `MultiModalContextAgent`

**Inherits from**: BaseAgent

Interprets visual data and integrates it into the agent's textual context.

**Methods** (9):
- `__init__(self, file_path)`
- `capture_screen(self, label)`
- `analyze_screenshot(self, image_path, query)`
- `extract_text_from_image(self, image_path)`
- `gui_action(self, action, params)`
- `start_gui_recording(self)`
- `stop_gui_recording(self)`
- `replay_gui_interaction(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (20):
- `PIL.Image`
- `__future__.annotations`
- `base64`
- `easyocr`
- `json`
- `logging`
- `pathlib.Path`
- `pyautogui`
- `pynput.keyboard`
- `pynput.mouse`
- `pytesseract`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- ... and 5 more

---
*Auto-generated documentation*
