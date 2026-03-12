#!/usr/bin/env python3
"""Context manager module for PyAgent."""
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

from __future__ import annotations


class ContextManager:
    """A simple context manager that maintains a list of text segments and prunes old ones based on a token limit."""

    def __init__(self, max_tokens: int):
        """Initialize the ContextManager with a maximum token limit."""
        self._data: list[str] = []
        self.max_tokens = max_tokens

    async def push(self, text: str) -> None:
        """Add a new text segment to the context and prune old segments if the total token count exceeds the limit."""
        # simple token count based on whitespace-separated words
        self._data.append(text)
        # prune oldest segments if token count exceeds limit
        all_text = " ".join(self._data)
        tokens = all_text.split()
        while len(tokens) > self.max_tokens and self._data:
            # remove first segment and recompute
            self._data.pop(0)
            all_text = " ".join(self._data)
            tokens = all_text.split()

    def snapshot(self) -> str:
        """Get the current context as a single string."""
        return "".join(self._data)
