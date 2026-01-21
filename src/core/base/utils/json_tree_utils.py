"""
JSONTreeUtils - Nested JSON traversal and transformation utilities.

Refactored to modular package structure for Phase 317.
Original monolithic implementation delegated to src.core.base.utils.jsontree modules.
"""

from src.core.base.utils.jsontree.types import JSONTree
from src.core.base.utils.jsontree.iteration import (
    json_iter_leaves,
    json_iter_leaves_with_path,
)
from src.core.base.utils.jsontree.mapping import (
    json_map_leaves,
    json_map_leaves_async,
)
from src.core.base.utils.jsontree.reduction import json_reduce_leaves
from src.core.base.utils.jsontree.meta import (
    json_count_leaves,
    json_depth,
    json_filter_leaves,
    json_validate_leaves,
    json_find_leaves,
)
from src.core.base.utils.jsontree.transmutation import (
    json_flatten,
    json_unflatten,
)
from src.core.base.utils.jsontree.path import (
    json_get_path,
    json_set_path,
)
from src.core.base.utils.jsontree.rust import (
    json_iter_leaves_fast,
    json_count_leaves_fast,
    json_flatten_fast,
    RUST_ACCELERATION_AVAILABLE,
)

__all__ = [
    # Type aliases
    "JSONTree",
    # Iteration
    "json_iter_leaves",
    "json_iter_leaves_with_path",
    "json_iter_leaves_fast",
    # Mapping
    "json_map_leaves",
    "json_map_leaves_async",
    # Reduction
    "json_reduce_leaves",
    # Counting
    "json_count_leaves",
    "json_count_leaves_fast",
    "json_depth",
    # Flattening
    "json_flatten",
    "json_flatten_fast",
    "json_unflatten",
    # Path access
    "json_get_path",
    "json_set_path",
    # Filtering
    "json_filter_leaves",
    # Validation
    "json_validate_leaves",
    "json_find_leaves",
    # Constants
    "RUST_ACCELERATION_AVAILABLE",
]
