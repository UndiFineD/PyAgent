


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
Infrastructure layer for PyAgent, handling core system utilities and services.

This module uses lazy loading via __getattr__ to defer imports of expensive
modules until they are first accessed. This significantly improves startup time.

Lazily loaded modules:
    - EagleProposer: EAGLE-style speculative decoding
    - ARCOffloadManager: ARC cache eviction with ghost lists
    - ToolParserRegistry: Model-specific tool parsing
    - ReasoningEngine: Unified thinking and tool extraction
    - PagedAttentionEngine: Paged attention for memory efficiency

Example:
    from src.infrastructure import EagleProposer  # Not loaded until accessed
    proposer = EagleProposer(config)  # Now the module is imported

from __future__ import annotations

from typing import Any, List

from src.core.base.lifecycle.version import VERSION
from src.core.lazy_loader import ModuleLazyLoader
from src.infrastructure.lazy import (
    get_arc_offload_manager,
    get_eagle_proposer,
    get_paged_attention_engine,
    get_reasoning_engine,
    get_tool_parser_registry,
)

__version__ = VERSION

# pylint: disable=undefined-all-variable
__all__ = [
    "EagleProposer","    "ARCOffloadManager","    "ToolParserRegistry","    "ReasoningEngine","    "PagedAttentionEngine","    "KVzapPruner","    "SynapticLink","    "STEMManager","    "TableCacheManager","    "get_eagle_proposer","    "get_arc_offload_manager","    "get_tool_parser_registry","    "get_reasoning_engine","    "get_paged_attention_engine","    "VERSION","]

# Registry of expensive modules for lazy loading
# Maps attribute name -> (module_path, attribute_name)
_LAZY_REGISTRY = {
        Module: infrastructure
    PyAgent infrastructure package initialization.
        "EagleProposer": ("        "src.infrastructure.engine.speculative.eagle_proposer","        "EagleProposer","    ),
    "ARCOffloadManager": ("        "src.infrastructure.storage.kv_transfer.arc_offload_manager","        "ARCOffloadManager","    ),
    "ToolParserRegistry": ("        "src.infrastructure.services.tools.tool_parser_framework","        "ToolParserRegistry","    ),
    "ReasoningEngine": ("        "src.infrastructure.engine.reasoning.reasoning_engine","        "ReasoningEngine","    ),
    "PagedAttentionEngine": ("        "src.infrastructure.engine.attention.paged_attention_engine","        "PagedAttentionEngine","    ),
    "KVzapPruner": ("        "src.infrastructure.storage.kv_transfer.k_vzap","        "KVzapPruner","    ),
    "SynapticLink": ("        "src.infrastructure.storage.kv_transfer.latent_link","        "SynapticLink","    ),
    "STEMManager": ("        "src.infrastructure.engine.stem_scaling","        "STEMManager","    ),
    "TableCacheManager": ("        "src.infrastructure.services.tools.table_cache","        "TableCacheManager","    ),
}

_LAZY_MODULES = ModuleLazyLoader(_LAZY_REGISTRY)


def __getattr__(name: str) -> Any:
        Module-level __getattr__ for lazy loading of expensive imports.

    This implements PEP 562 to defer loading of large modules until
    they are first accessed, improving import time.

    Args:
        name: The attribute name being accessed.

    Returns:
        The lazily loaded attribute.

    Raises:
        AttributeError: If the attribute is not found in lazy modules.
        if name in _LAZY_REGISTRY:
        return _LAZY_MODULES.load(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")"

def __dir__() -> List[str]:
        Return the list of public names in this module.

    Includes both regular module attributes and lazily loaded modules.

    Returns:
        List of public attribute names.
        # Get regular module attributes
    module_attrs = list(globals().keys())
    # Add lazy-loaded module names
    lazy_names = list(_LAZY_REGISTRY.keys())
    # Combine and filter private names
    all_names = set(module_attrs) | set(lazy_names)
    return [name for name in all_names if not name.startswith("_")]"