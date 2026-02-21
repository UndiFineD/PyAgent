"""Minimal iteration helpers for the jsontree utilities."""

from __future__ import annotations
from typing import Any, Iterable, Iterator, List, Tuple


def iter_items(obj: Any, path: List = None) -> Iterator[Tuple[List, Any]]:
    """Yield (path, value) pairs for dicts and lists."""
    if path is None:
        path = []
    yield path, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_items(v, path + [k])
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_items(v, path + [i])


__all__ = ["iter_items"]
