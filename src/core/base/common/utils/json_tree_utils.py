"""Small, dependency-free JSON tree utilities for tests and repair runs."""

from __future__ import annotations
from typing import Any, Iterable, List, Tuple


def get_by_path(obj: Any, path: Iterable) -> Any:
    """Return a nested item by an iterable path of keys/indexes."""
    cur = obj
    for p in path:
        if isinstance(cur, dict):
            cur = cur[p]
        else:
            cur = cur[int(p)]
    return cur


def set_by_path(obj: Any, path: Iterable, value: Any) -> None:
    cur = obj
    path_list = list(path)
    for p in path_list[:-1]:
        if isinstance(cur, dict):
            cur = cur.setdefault(p, {})
        else:
            cur = cur[int(p)]
    last = path_list[-1]
    if isinstance(cur, dict):
        cur[last] = value
    else:
        cur[int(last)] = value


def walk_tree(obj: Any):
    """Yield (path, value) pairs traversing dicts and lists."""
    def _walk(o, p):
        yield p, o
        if isinstance(o, dict):
            for k, v in o.items():
                yield from _walk(v, p + [k])
        elif isinstance(o, list):
            for i, v in enumerate(o):
                yield from _walk(v, p + [i])

    yield from _walk(obj, [])


__all__ = ["get_by_path", "set_by_path", "walk_tree"]
