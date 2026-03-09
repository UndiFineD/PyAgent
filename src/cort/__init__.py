#!/usr/bin/env python3
"""Chain of Thought module for PyAgent."""
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

from typing import List, Optional
from context_manager import ContextManager


class ChainOfThought:
    """Manages a chain of thought process, allowing for branching and context management."""

    def __init__(self, context_mgr: ContextManager):
        """Initialize the Chain of Thought with a context manager."""
        self.context_mgr = context_mgr
        self.root: Optional[ThoughtNode] = None

    def new_node(self, text: str) -> "ThoughtNode":
        """Create a new thought node with the given text and set it as the root."""
        node = ThoughtNode(text, self)
        self.root = node
        return node


class ThoughtNode:
    """Represents a single thought in the chain, which can have child thoughts (branches)."""

    def __init__(self, text: str, cort: ChainOfThought):
        """Initialize a ThoughtNode with text and a reference to the parent ChainOfThought."""
        self.text = text
        self.cort = cort
        cort.context_mgr.push(text)
        self.children: List[ThoughtNode] = []

    def fork(self, text: str) -> "ThoughtNode":
        """Create a new child thought node with the given text."""
        child = ThoughtNode(text, self.cort)
        self.children.append(child)
        return child

    def add(self, text: str) -> None:
        """Add additional text to the current thought node."""
        self.cort.context_mgr.push(text)
        self.text += " " + text
