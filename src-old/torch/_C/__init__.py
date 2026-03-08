"""Package placeholder for torch._C C-extension namespace.

Provides minimal compatibility and exposes submodules such as
`_distributed_c10d` for import-time checks.
"""
__all__ = ["_distributed_c10d"]

from . import _distributed_c10d

__version__ = "0.0.0-shim"
