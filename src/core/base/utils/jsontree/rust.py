from __future__ import annotations
import logging
from collections.abc import Iterable
from src.core.base.utils.jsontree.types import JSONTree, _T
from src.core.base.utils.jsontree.iteration import json_iter_leaves
from src.core.base.utils.jsontree.meta import json_count_leaves
from src.core.base.utils.jsontree.transmutation import json_flatten

logger = logging.getLogger(__name__)

# Try to import Rust-accelerated versions
try:
    from rust_core import (
        json_iter_leaves_rust,
        json_map_leaves_rust,
        json_count_leaves_rust,
        json_flatten_rust,
    )
    
    # Use Rust versions if available
    _json_iter_leaves_native = json_iter_leaves
    _json_count_leaves_native = json_count_leaves
    _json_flatten_native = json_flatten
    
    def json_iter_leaves_fast(value: JSONTree[_T]) -> Iterable[_T]:
        """Rust-accelerated leaf iteration."""
        try:
            return json_iter_leaves_rust(value)
        except Exception:
            return _json_iter_leaves_native(value)
    
    def json_count_leaves_fast(value: JSONTree[_T]) -> int:
        """Rust-accelerated leaf counting."""
        try:
            return json_count_leaves_rust(value)
        except Exception:
            return _json_count_leaves_native(value)
    
    def json_flatten_fast(
        value: JSONTree[_T],
        separator: str = ".",
    ) -> dict[str, _T]:
        """Rust-accelerated flattening."""
        try:
            return json_flatten_rust(value, separator)
        except Exception:
            return _json_flatten_native(value, separator)
    
    RUST_ACCELERATION_AVAILABLE = True
    logger.debug("JSONTreeUtils: Rust acceleration available")
    
except ImportError:
    # Rust not available, use pure Python
    json_iter_leaves_fast = json_iter_leaves
    json_count_leaves_fast = json_count_leaves
    json_flatten_fast = json_flatten
    RUST_ACCELERATION_AVAILABLE = False
    logger.debug("JSONTreeUtils: Using pure Python (Rust not available)")
