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


"""JSONTreeUtils - Nested JSON traversal and transformation utilities.

Refactored to modular package structure for Phase 317.
Original monolithic implementation delegated to src.core.base.common.utils.jsontree modules.
"""
from src.core.base.common.utils.jsontree.iteration import (
    json_iter_leaves, json_iter_leaves_with_path)
from src.core.base.common.utils.jsontree.mapping import (json_map_leaves,
                                                         json_map_leaves_async)
from src.core.base.common.utils.jsontree.meta import (json_count_leaves,
                                                      json_depth,
                                                      json_filter_leaves,
                                                      json_find_leaves,
                                                      json_validate_leaves)
from src.core.base.common.utils.jsontree.path import (json_get_path,
                                                      json_set_path)
from src.core.base.common.utils.jsontree.reduction import json_reduce_leaves
from src.core.base.common.utils.jsontree.rust import (
    RUST_ACCELERATION_AVAILABLE, json_count_leaves_fast, json_flatten_fast,
    json_iter_leaves_fast)
from src.core.base.common.utils.jsontree.transmutation import (json_flatten,
                                                               json_unflatten)
from src.core.base.common.utils.jsontree.types import JSONTree

__all__ = [
    # Type aliases
    "JSONTree","    # Iteration
    "json_iter_leaves","    "json_iter_leaves_with_path","    "json_iter_leaves_fast","    # Mapping
    "json_map_leaves","    "json_map_leaves_async","    # Reduction
    "json_reduce_leaves","    # Counting
    "json_count_leaves","    "json_count_leaves_fast","    "json_depth","    # Flattening
    "json_flatten","    "json_flatten_fast","    "json_unflatten","    # Path access
    "json_get_path","    "json_set_path","    # Filtering
    "json_filter_leaves","    # Validation
    "json_validate_leaves","    "json_find_leaves","    # Constants
    "RUST_ACCELERATION_AVAILABLE","]
