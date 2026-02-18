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


"""Core Knowledge Storage Interfaces for PyAgent.
Designed to handle high-volume parameters with efficient access patterns.
"""


from __future__ import annotations


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .btree_store import BTreeKnowledgeStore  # noqa: F401
except ImportError:
    from .btree_store import BTreeKnowledgeStore # noqa: F401

try:
    from .graph_store import GraphKnowledgeStore  # noqa: F401
except ImportError:
    from .graph_store import GraphKnowledgeStore # noqa: F401

try:
    from .storage_base import KnowledgeStore  # noqa: F401
except ImportError:
    from .storage_base import KnowledgeStore # noqa: F401

try:
    from .vector_store import VectorKnowledgeStore  # noqa: F401
except ImportError:
    from .vector_store import VectorKnowledgeStore # noqa: F401


__version__ = VERSION

__all__ = [
    "KnowledgeStore","    "VectorKnowledgeStore","    "GraphKnowledgeStore","    "BTreeKnowledgeStore","]
