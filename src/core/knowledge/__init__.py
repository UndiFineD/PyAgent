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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Core Knowledge Storage Interfaces for PyAgent.
Designed to handle high-volume parameters with efficient access patterns.
"""

from __future__ import annotations
from src.core.base.version import VERSION
from .storage_base import KnowledgeStore
from .vector_store import VectorKnowledgeStore
from .graph_store import GraphKnowledgeStore
from .btree_store import BTreeKnowledgeStore

__version__ = VERSION

__all__ = [
    "KnowledgeStore",
    "VectorKnowledgeStore",
    "GraphKnowledgeStore",
    "BTreeKnowledgeStore",
]