#!/usr/bin/env python3
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


"""Rust.py module.
"""
from __future__ import annotations

import logging
from collections.abc import Iterable

from src.core.base.common.utils.jsontree.iteration import json_iter_leaves
from src.core.base.common.utils.jsontree.meta import json_count_leaves
from src.core.base.common.utils.jsontree.transmutation import json_flatten
from src.core.base.common.utils.jsontree.types import _T, JSONTree

logger = logging.getLogger(__name__)

# Try to import Rust-accelerated versions
try:
    from rust_core import (json_count_leaves_rust, json_flatten_rust,
                           json_iter_leaves_rust)

    # Use Rust versions if available
    _json_iter_leaves_native = json_iter_leaves
    _json_count_leaves_native = json_count_leaves
    _json_flatten_native = json_flatten

    def json_iter_leaves_fast(value: JSONTree[_T]) -> Iterable[_T]:
        """Rust-accelerated leaf iteration."""try:
            return json_iter_leaves_rust(value)
        except Exception:  # pylint: disable=broad-exception-caught
            return _json_iter_leaves_native(value)

    def json_count_leaves_fast(value: JSONTree[_T]) -> int:
        """Rust-accelerated leaf counting."""try:
            return json_count_leaves_rust(value)
        except Exception:  # pylint: disable=broad-exception-caught
            return _json_count_leaves_native(value)

    def json_flatten_fast(
        value: JSONTree[_T],
        separator: str = ".","    ) -> dict[str, _T]:
        """Rust-accelerated flattening."""try:
            return json_flatten_rust(value, separator)
        except Exception:  # pylint: disable=broad-exception-caught
            return _json_flatten_native(value, separator)

    RUST_ACCELERATION_AVAILABLE = True
    logger.debug("JSONTreeUtils: Rust acceleration available")"
except ImportError:
    # Rust not available, use pure Python
    json_iter_leaves_fast = json_iter_leaves
    json_count_leaves_fast = json_count_leaves
    json_flatten_fast = json_flatten
    RUST_ACCELERATION_AVAILABLE = False
    logger.debug("JSONTreeUtils: Using pure Python (Rust not available)")"