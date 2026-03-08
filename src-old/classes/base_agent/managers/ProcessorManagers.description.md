# ProcessorManagers

**File**: `src\classes\base_agent\managers\ProcessorManagers.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 20 imports  
**Lines**: 135  
**Complexity**: 16 (moderate)

## Overview

Python module containing implementation for ProcessorManagers.

## Classes (3)

### `ResponsePostProcessor`

Manages post-processing hooks for agent responses.

**Methods** (3):
- `__init__(self)`
- `register(self, hook, priority)`
- `process(self, text)`

### `MultimodalProcessor`

Processor for multimodal inputs.

**Methods** (8):
- `__init__(self)`
- `add_input(self, input_data)`
- `add_text(self, text)`
- `add_image(self, data, mime_type)`
- `add_code(self, code, language)`
- `build_prompt(self)`
- `get_api_messages(self)`
- `clear(self)`

### `SerializationManager`

Manager for custom serialization formats (Binary/JSON).

**Methods** (5):
- `__init__(self, config)`
- `serialize(self, data)`
- `deserialize(self, data)`
- `save_to_file(self, data, path)`
- `load_from_file(self, path)`

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `cbor2`
- `collections.abc.Callable`
- `json`
- `logging`
- `pathlib.Path`
- `pickle`
- `src.core.base.models.InputType`
- `src.core.base.models.MultimodalInput`
- `src.core.base.models.SerializationConfig`
- `src.core.base.models.SerializationFormat`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 5 more

---
*Auto-generated documentation*
