"""Package shim for `lora` that prefers `src/lora` if present."""
import os

_root = os.path.dirname(os.path.dirname(__file__))
_src_lora = os.path.join(_root, "src", "lora")
if os.path.isdir(_src_lora):
    __path__.insert(0, _src_lora)

__all__ = []
"""Project `lora` package shim.

Expose both adapter and service metric lora directories to module imports.
"""
import os

_repo_root = os.path.dirname(os.path.dirname(__file__))
_paths = [
    os.path.join(_repo_root, "src", "infrastructure", "adapters", "lora"),
    os.path.join(_repo_root, "src", "infrastructure", "services", "metrics", "lora"),
]

for _p in _paths:
    if os.path.isdir(_p) and _p not in __path__:
        __path__.insert(0, _p)

__all__ = []
