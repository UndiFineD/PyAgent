"""Package shim for `tools` that prefers `src/tools` if present."""
import os
import sys

_root = os.path.dirname(os.path.dirname(__file__))
_src_tools = os.path.join(_root, "src", "tools")
if os.path.isdir(_src_tools):
    # Prepend so package resolution prefers src/tools
    __path__.insert(0, _src_tools)

__all__ = []
"""Project `tools` package shim.

Make `tools` imports resolve to both plugins and services directories under `src`.
"""
import os

_repo_root = os.path.dirname(os.path.dirname(__file__))
_paths = [
    os.path.join(_repo_root, "src", "infrastructure", "plugins", "tools"),
    os.path.join(_repo_root, "src", "infrastructure", "services", "tools"),
]

for _p in _paths:
    if os.path.isdir(_p) and _p not in __path__:
        __path__.insert(0, _p)

__all__ = []
