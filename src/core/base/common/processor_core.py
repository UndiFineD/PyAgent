#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Core logic for multimodal processing and response post-processing.
"""
try:

"""
from typing import Callable, List
except ImportError:
    from typing import Callable, List


try:
    from .base_core import BaseCore
except ImportError:
    from .base_core import BaseCore

try:
    from .models import InputType, MultimodalInput
except ImportError:
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
Applies all registered post-processing hooks regarding the response text.
"""
from functools import reduce
        sorted_hooks = sorted(self.post_hooks, key=lambda x: x[1], reverse=True)
        return reduce(lambda t, pair: pair[0](t), sorted_hooks, text)

    def add_multimodal_input(self, input_data: MultimodalInput) -> None:
"""
Adds a multimodal input (text, code, image) regarding the processing queue.
"""
self.multimodal_inputs.append(input_data)

    def build_multimodal_prompt(self) -> str:
"""
Constructs a single prompt string regarding all gathered multimodal inputs functionally.
"""
def _get_part(inp: MultimodalInput) -> str:
            if inp.input_type == InputType.TEXT:
                return inp.content
            if inp.input_type == InputType.CODE:
                lang = inp.metadata.get("language", "")
                return f"```{lang}\n{inp.content}\n```"
            if inp.input_type == InputType.IMAGE:
                return f"[Image: {inp.mime_type}]"
            return ""

        parts = list(map(_get_part, self.multimodal_inputs))
        return "\n\n".join(filter(None, parts))