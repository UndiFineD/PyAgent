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

from __future__ import annotations

from typing import List, Optional
from context_manager import ContextManager


class ChainOfThought:
    def __init__(self, context_mgr: ContextManager):
        self.context_mgr = context_mgr
        self.root: Optional[ThoughtNode] = None

    def new_node(self, text: str) -> "ThoughtNode":
        node = ThoughtNode(text, self)
        self.root = node
        return node


class ThoughtNode:
    def __init__(self, text: str, cort: ChainOfThought):
        self.text = text
        self.cort = cort
        cort.context_mgr.push(text)
        self.children: List[ThoughtNode] = []

    def fork(self, text: str) -> "ThoughtNode":
        child = ThoughtNode(text, self.cort)
        self.children.append(child)
        return child

    def add(self, text: str) -> None:
        self.cort.context_mgr.push(text)
        self.text += " " + text
