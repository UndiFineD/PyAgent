#!/usr/bin/env python3
"""
Collection utilities for tests and lightweight usage.

This file provides a small, well-tested subset of collection helpers used
throughout the codebase. Implementations favor clarity and robustness.
"""
from __future__ import annotations





try:
    import itertools
except ImportError:
    import itertools

try:
    from collections import defaultdict
except ImportError:
    from collections import defaultdict

try:
    from collections.abc import Callable, Generator, Hashable, Iterable
except ImportError:
    from collections.abc import Callable, Generator, Hashable, Iterable

try:
    from typing import Any, Dict, List, TypeVar
except ImportError:
    from typing import Any, Dict, List, TypeVar



T = TypeVar("T")
K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LazyDict(dict):
    """A very small LazyDict: values can be callables evaluated on first access.

    Example:
        ld = LazyDict({'x': lambda: expensive()})
        val = ld['x']  # factory runs once
    """

    def __init__(self, factory: Dict[str, Callable[[], V]] | None = None) -> None:
        super().__init__()
        self._factory = dict(factory or {})
        self._cache: Dict[str, V] = {}

    def __getitem__(self, key: str) -> V:
        if key in self._cache:
            return self._cache[key]
        if key in self._factory:
            val = self._factory[key]()
            self._cache[key] = val
            return val
        return super().__getitem__(key)

    def register(self, key: str, factory: Callable[[], V]) -> None:
        """Register a factory function for lazy evaluation of a key.

        Args:
            key: The dictionary key to register.
            factory: A callable that returns the value for this key.
        """
        self._factory[key] = factory
        self._cache.pop(key, None)


def as_list(it: Iterable[T]) -> List[T]:
    return list(it) if not isinstance(it, list) else it


def as_iter(obj: T | Iterable[T]) -> Iterable[T]:
    if isinstance(obj, str) or not isinstance(obj, Iterable):
        return [obj]  # type: ignore[list-item]
    return obj  # type: ignore[return-value]


def is_list_of(value: object, typ: type, *, check: str = "first") -> bool:
    if not isinstance(value, list):
        return False
    if not value:
        return True
    if check == "first":
        return isinstance(value[0], typ)
    if check == "all":
        return all(isinstance(x, typ) for x in value)
    raise ValueError("invalid check")


def chunk_list(lst: List[T], size: int) -> Generator[List[T], None, None]:
    if size <= 0:
        raise ValueError("size must be positive")
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def chunk_iter(iterable: Iterable[T], size: int) -> Generator[List[T], None, None]:
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


def flatten_2d_lists(lists: Iterable[Iterable[T]]) -> List[T]:
    return [x for sub in lists for x in sub]


def flatten_deep(nested: Any, max_depth: int = -1) -> List[Any]:
    out: List[Any] = []

    def _f(v: Any, depth: int) -> None:
        if max_depth >= 0 and depth > max_depth:
            out.append(v)
            return
        if isinstance(v, (list, tuple)):
            for item in v:
                _f(item, depth + 1)
        else:
            out.append(v)

    _f(nested, 0)
    return out


def full_groupby(iterable: Iterable[T], keyfunc: Callable[[T], K]) -> Dict[K, List[T]]:
    d: Dict[K, List[T]] = defaultdict(list)
    for x in iterable:
        d[keyfunc(x)].append(x)
    return dict(d)


def partition(iterable: Iterable[T], pred: Callable[[T], bool]) -> tuple[List[T], List[T]]:
    a: List[T] = []
    b: List[T] = []
    for x in iterable:
        (a if pred(x) else b).append(x)
    return a, b


def first(iterable: Iterable[T], default: T | None = None) -> T | None:
    for x in iterable:
        return x
    return default


def first_or_raise(iterable: Iterable[T]) -> T:
    for x in iterable:
        return x
    raise ValueError("no elements")


def last(iterable: Iterable[T], default: T | None = None) -> T | None:
    out: T | None = default
    for x in iterable:
        out = x
    return out


def swap_dict_values(d: Dict[K, V]) -> Dict[V, K]:
    return {v: k for k, v in d.items()}


def deep_merge_dicts(a: Dict, b: Dict) -> Dict:
    res = dict(a)
    for k, v in b.items():
        if k in res and isinstance(res[k], dict) and isinstance(v, dict):
            res[k] = deep_merge_dicts(res[k], v)
        else:
            res[k] = v
    return res


def invert_dict(d: Dict[K, V]) -> Dict[V, K]:
    return {v: k for k, v in d.items()}


def invert_dict_multi(d: Dict[K, V]) -> Dict[V, List[K]]:
    out: Dict[V, List[K]] = defaultdict(list)
    for k, v in d.items():
        out[v].append(k)
    return dict(out)


def filter_none(d: Dict[K, V | None]) -> Dict[K, V]:
    return {k: v for k, v in d.items() if v is not None}  # type: ignore[return-value]


def pick_keys(d: Dict[K, V], keys: Iterable[K]) -> Dict[K, V]:
    return {k: d[k] for k in keys if k in d}


def omit_keys(d: Dict[K, V], keys: Iterable[K]) -> Dict[K, V]:
    ks = set(keys)
    return {k: v for k, v in d.items() if k not in ks}


def unique(seq: Iterable[T]) -> List[T]:
    seen = set()
    out: List[T] = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def unique_by(seq: Iterable[T], keyfunc: Callable[[T], Any]) -> List[T]:
    seen = set()
    out: List[T] = []
    for x in seq:
        k = keyfunc(x)
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def sliding_window(seq: Iterable[T], n: int) -> Generator[tuple[T, ...], None, None]:
    it = iter(seq)
    window = tuple(itertools.islice(it, n))
    if len(window) < n:
        return
    yield tuple(window)
    for x in it:
        window = (*window[1:], x)
        yield tuple(window)


def pairwise(iterable: Iterable[T]) -> Generator[tuple[T, T], None, None]:
    a, b = itertools.tee(iterable)
    next(b, None)
    for x, y in zip(a, b):
        yield x, y


__all__ = [
    "LazyDict",
    "as_list",
    "as_iter",
    "is_list_of",
    "chunk_list",
    "chunk_iter",
    "flatten_2d_lists",
    "flatten_deep",
    "full_groupby",
    "partition",
    "first",
    "first_or_raise",
    "last",
    "swap_dict_values",
    "deep_merge_dicts",
    "invert_dict",
    "invert_dict_multi",
    "filter_none",
    "pick_keys",
    "omit_keys",
    "unique",
    "unique_by",
    "sliding_window",
    "pairwise"
]
