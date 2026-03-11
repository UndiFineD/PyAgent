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

    async def new_node(self, text: str) -> "ThoughtNode":
        """Create a new thought node with the given text and set it as the root.

        The underlying context manager push is asynchronous, so callers must await
        this method. The resulting node is returned once the context has been
        recorded.
        """
        node = ThoughtNode(text, self)
        # record the initial text in the context manager
        await self.context_mgr.push(text)
        self.root = node
        return node


class ThoughtNode:
    """Represents a single thought in the chain, which can have child thoughts (branches)."""

    def __init__(self, text: str, cort: ChainOfThought):
        """Initialize a ThoughtNode with text and a reference to the parent ChainOfThought.

        The actual context push is performed by the caller (typically
        :meth:`ChainOfThought.new_node` or :meth:`fork`).  This keeps __init__
        synchronous so objects can be constructed without awaiting, and avoids
        tangled event loop logic.
        """
        self.text = text
        self.cort = cort
        self.children: List[ThoughtNode] = []

    async def fork(self, text: str) -> "ThoughtNode":
        """Create a new child thought node with the given text.

        The resulting node is returned after the text has been pushed into the
        context manager.
        """
        child = ThoughtNode(text, self.cort)
        await self.cort.context_mgr.push(text)
        self.children.append(child)
        return child

    async def add(self, text: str) -> None:
        """Add additional text to the current thought node.

        The push is awaited before the local state is updated so that the
        context manager remains in sync with the node's contents.
        """
        await self.cort.context_mgr.push(text)
        self.text += " " + text
