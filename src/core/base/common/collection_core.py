# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified collection and data structure management core."""

from typing import Any, Dict, List, TypeVar, Iterable, Callable

T = TypeVar("T")

class CollectionCore:
    """
    Standardized utilities for complex data structures and collections.
    """

    @staticmethod
    def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two dictionaries."""
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                CollectionCore.deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    @staticmethod
    def chunk_list(data: List[T], size: int) -> Iterable[List[T]]:
        """Yield successive chunks from a list."""
        for i in range(0, len(data), size):
            yield data[i:i + size]

    @staticmethod
    def flatten(nested_list: List[List[T]]) -> List[T]:
        """Flatten a 2D list into a 1D list."""
        return [item for sublist in nested_list for item in sublist]

    @staticmethod
    def filter_none(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove keys with None values from a dictionary."""
        return {k: v for k, v in data.items() if v is not None}
