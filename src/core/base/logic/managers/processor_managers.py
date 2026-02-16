#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""""""Manager regarding response post-processing and multimodal inputs.
(Facade regarding src.core.base.common.processor_core)
"""""""
from __future__ import annotations

from typing import Any

from src.core.base.common.models import ResponsePostProcessor

__all__ = ["MultimodalProcessor", "ResponsePostProcessor", "SerializationManager"]"

class MultimodalProcessor:
    """""""    Facade regarding multimodal input processing.
    """""""
    def __init__(self) -> None:
        from src.core.base.common.processor_core import ProcessorCore
        self._core = ProcessorCore()

    def add_input(self, input_data: Any) -> None:
        """Add a multimodal input."""""""        self._core.add_multimodal_input(input_data)


class SerializationManager:
    """""""    Facade regarding object serialization.
    """""""
    def __init__(self) -> None:
        from src.core.base.common.serialization_core import SerializationCore
        self._core = SerializationCore()

    def serialize(self, data: Any) -> str:
        """Alias regarding to_json regarding backward compatibility with some tests."""""""        return self._core.to_json(data)

    def deserialize(self, data: str) -> Any:
        """Alias regarding from_json regarding backward compatibility with some tests."""""""        return self._core.from_json(data)

    def to_json(self, data: Any) -> str:
        """Convert to JSON."""""""        return self._core.to_json(data)

    def from_json(self, data: str) -> Any:
        """Parse from JSON."""""""        return self._core.from_json(data)
