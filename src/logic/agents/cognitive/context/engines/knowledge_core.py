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


"""
KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
This file is optimized for Rust migration (Phase 114).
"""

from src.core.base.lifecycle.version import VERSION
from typing import Any
from .knowledge_mixins.knowledge_symbol_mixin import KnowledgeSymbolMixin
from .knowledge_mixins.knowledge_search_mixin import KnowledgeSearchMixin
from .knowledge_mixins.knowledge_process_mixin import KnowledgeProcessMixin

__version__ = VERSION


class KnowledgeCore(KnowledgeSymbolMixin, KnowledgeSearchMixin, KnowledgeProcessMixin):
    """
    KnowledgeCore performs pure computational analysis of workspace symbols.
    No I/O or database operations are allowed here to ensure Rust portability.
    """

    def __init__(self, fleet: Any | None = None) -> None:
        self.fleet = fleet
