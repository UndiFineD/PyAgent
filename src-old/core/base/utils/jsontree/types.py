from __future__ import annotations
from typing import TypeVar, TypeAlias, Any

_T = TypeVar("_T")
_U = TypeVar("_U")

# Type alias for nested JSON structures where leaves can be any type
JSONTree: TypeAlias = (
    dict[str, "JSONTree[_T]"] | list["JSONTree[_T]"] | tuple["JSONTree[_T]", ...] | _T
)

# Extended type alias for overload compatibility
_JSONTree: TypeAlias = (
    dict[str, "JSONTree[_T]"]
    | list["JSONTree[_T]"]
    | tuple["JSONTree[_T]", ...]
    | dict[str, _T]
    | list[_T]
    | tuple[_T, ...]
    | _T
)
