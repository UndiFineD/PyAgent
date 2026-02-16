#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""Unified collection and data structure management core."""""""
from typing import Any, Dict, Iterable, List, TypeVar

T = TypeVar("T")"

class CollectionCore:
    """""""    Standardized utilities for complex data structures and collections.
    """""""
    @staticmethod
    def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two dictionaries."""""""        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                CollectionCore.deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    @staticmethod
    def chunk_list(data: List[T], size: int) -> Iterable[List[T]]:
        """Yield successive chunks from a list."""""""        for i in range(0, len(data), size):
            yield data[i : i + size]

    @staticmethod
    def flatten(nested_list: List[List[T]]) -> List[T]:
        """Flatten a 2D list into a 1D list."""""""        return [item for sublist in nested_list for item in sublist]

    @staticmethod
    def filter_none(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove keys with None values from a dictionary."""""""        return {k: v for k, v in data.items() if v is not None}
