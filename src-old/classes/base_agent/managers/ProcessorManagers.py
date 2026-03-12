#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/base_agent/managers/ProcessorManagers.description.md

# ProcessorManagers

**File**: `src\\classes\base_agent\\managers\\ProcessorManagers.py`  
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
## Source: src-old/classes/base_agent/managers/ProcessorManagers.improvements.md

# Improvements for ProcessorManagers

**File**: `src\\classes\base_agent\\managers\\ProcessorManagers.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 135 lines (medium)  
**Complexity**: 16 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ProcessorManagers_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from src.core.base.models import (
    InputType,
    MultimodalInput,
    SerializationConfig,
    SerializationFormat,
)

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from src.core.base.version import VERSION

__version__ = VERSION


class ResponsePostProcessor:
    """Manages post-processing hooks for agent responses."""

    def __init__(self) -> None:
        self.hooks: list[tuple[Callable[[str], str], int]] = []

    def register(self, hook: Callable[[str], str], priority: int = 0) -> None:
        self.hooks.append((hook, priority))

    def process(self, text: str) -> str:
        sorted_hooks = sorted(self.hooks, key=lambda x: x[1], reverse=True)
        for hook, _ in sorted_hooks:
            text = hook(text)
        return text


class MultimodalProcessor:
    """Processor for multimodal inputs."""

    def __init__(self) -> None:
        self.inputs: list[MultimodalInput] = []
        self.processed: str = ""
        logging.debug("MultimodalProcessor initialized")

    def add_input(self, input_data: MultimodalInput) -> None:
        self.inputs.append(input_data)

    def add_text(self, text: str) -> None:
        self.add_input(MultimodalInput(InputType.TEXT, text))

    def add_image(self, data: str, mime_type: str = "image/png") -> None:
        self.add_input(MultimodalInput(InputType.IMAGE, data, mime_type))

    def add_code(self, code: str, language: str = "python") -> None:
        self.add_input(
            MultimodalInput(InputType.CODE, code, metadata={"language": language})
        )

    def build_prompt(self) -> str:
        parts: list[str] = []
        for inp in self.inputs:
            if inp.input_type == InputType.TEXT:
                parts.append(inp.content)
            elif inp.input_type == InputType.CODE:
                lang = inp.metadata.get("language", "")
                parts.append(f"```{lang}\\n{inp.content}\\n```")
            elif inp.input_type == InputType.IMAGE:
                parts.append(f"[Image: {inp.mime_type}]")
            elif inp.input_type == InputType.DIAGRAM:
                parts.append(f"[Diagram: {inp.metadata.get('type', 'unknown')}]")
        self.processed = "\\n\\n".join(parts)
        return self.processed

    def get_api_messages(self) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = []
        for inp in self.inputs:
            if inp.input_type == InputType.TEXT:
                messages.append({"type": "text", "text": inp.content})
            elif inp.input_type == InputType.IMAGE:
                messages.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{inp.mime_type};base64,{inp.content}"
                        },
                    }
                )
            elif inp.input_type == InputType.CODE:
                messages.append(
                    {
                        "type": "text",
                        "text": f"```{inp.metadata.get('language', '')}\\n{inp.content}\\n```",
                    }
                )
        return messages

    def clear(self) -> None:
        self.inputs.clear()
        self.processed = ""


class SerializationManager:
    """Manager for custom serialization formats (Binary/JSON)."""

    def __init__(self, config: SerializationConfig | None = None) -> None:
        self.config = config or SerializationConfig()

    def serialize(self, data: Any) -> bytes:
        """Serializes data using the configured format (JSON, PICKLE, CBOR)."""
        if self.config.format == SerializationFormat.JSON:
            result = json.dumps(data, indent=2).encode("utf-8")
        elif self.config.format == SerializationFormat.PICKLE:
            import pickle

            result = pickle.dumps(data)
        elif self.config.format == SerializationFormat.CBOR:
            try:
                import cbor2

                result = cbor2.dumps(data)
            except ImportError:
                logging.warning("cbor2 not installed. Falling back to JSON.")
                result = json.dumps(data).encode("utf-8")
        else:
            result = json.dumps(data).encode("utf-8")

        if self.config.compression:
            import zlib

            result = zlib.compress(result)
        return result

    def deserialize(self, data: bytes) -> Any:
        """Deserializes data using the configured format."""
        if self.config.compression:
            import zlib

            data = zlib.decompress(data)

        if self.config.format == SerializationFormat.JSON:
            return json.loads(data.decode("utf-8"))
        elif self.config.format == SerializationFormat.PICKLE:
            import pickle

            return pickle.loads(data)
        elif self.config.format == SerializationFormat.CBOR:
            try:
                import cbor2

                return cbor2.loads(data)
            except (ImportError, ValueError):
                # Fallback to JSON if CBOR fails or is missing
                try:
                    return json.loads(data.decode("utf-8"))
                except Exception:
                    raise ValueError(
                        "Deserialization failed for CBOR and JSON fallback."
                    )
        return json.loads(data.decode("utf-8"))

    def save_to_file(self, data: Any, path: Path) -> None:
        path.write_bytes(self.serialize(data))

    def load_from_file(self, path: Path) -> Any:
        return self.deserialize(path.read_bytes())
