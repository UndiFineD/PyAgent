from __future__ import annotations
from collections.abc import Iterable
from src.core.base.common.utils.jsontree.types import JSONTree, _T

def json_iter_leaves(value: JSONTree[_T]) -> Iterable[_T]:
    """
    Iterate through each leaf in a nested JSON structure.

    A leaf is any value that is not a dict, list, or tuple.

    Args:
        value: A nested JSON structure (dict, list, tuple, or leaf value).

    Yields:
        Each leaf value in depth-first order.
    """
    if isinstance(value, dict):
        for v in value.values():
            yield from json_iter_leaves(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from json_iter_leaves(v)
    else:
        yield value


def json_iter_leaves_with_path(
    value: JSONTree[_T],
    prefix: str = ""
) -> Iterable[tuple[str, _T]]:
    """
    Iterate through each leaf with its dot-notation path.

    Args:
        value: A nested JSON structure.
        prefix: Optional path prefix (used for recursion).

    Yields:
        Tuples of (path, leaf_value).
    """
    if isinstance(value, dict):
        for k, v in value.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            yield from json_iter_leaves_with_path(v, new_prefix)
    elif isinstance(value, (list, tuple)):
        for i, v in enumerate(value):
            new_prefix = f"{prefix}[{i}]"
            yield from json_iter_leaves_with_path(v, new_prefix)
    else:
        yield (prefix, value)
