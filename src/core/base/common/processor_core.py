#!/usr/bin/env python3
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Core logic for multimodal processing and response post-processing.
"""

from __future__ import annotations
from typing import List, Callable
from .base_core import BaseCore
from .models import InputType, MultimodalInput

class ProcessorCore(BaseCore):
    """
    Authoritative engine for multimodal inputs and hook-based processing.
    """
    def __init__(self) -> None:
        super().__init__()
        self.post_hooks: List[tuple[Callable[[str], str], int]] = []
        self.multimodal_inputs: List[MultimodalInput] = []

    def register_post_hook(self, hook: Callable[[str], str], priority: int = 0) -> None:
        """
        Registers a post-processing hook for agent responses.
        """
        self.post_hooks.append((hook, priority))

    def process_response(self, text: str) -> str:
        """
        Applies all registered post-processing hooks to the response text.
        """
        sorted_hooks = sorted(self.post_hooks, key=lambda x: x[1], reverse=True)
        for hook, _ in sorted_hooks:
            text = hook(text)
        return text

    def add_multimodal_input(self, input_data: MultimodalInput) -> None:
        """
        Adds a multimodal input (text, code, image) to the processing queue.
        """
        self.multimodal_inputs.append(input_data)

    def build_multimodal_prompt(self) -> str:
        """
        Constructs a single prompt string from all gathered multimodal inputs.
        """
        parts: List[str] = []
        for inp in self.multimodal_inputs:
            if inp.input_type == InputType.TEXT:
                parts.append(inp.content)
            elif inp.input_type == InputType.CODE:
                lang = inp.metadata.get("language", "")
                parts.append(f"```{lang}\n{inp.content}\n```")
            elif inp.input_type == InputType.IMAGE:
                parts.append(f"[Image: {inp.mime_type}]")
        return "\n\n".join(parts)
