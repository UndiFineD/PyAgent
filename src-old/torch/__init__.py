"""Lightweight shim for `torch` to avoid importing real PyTorch during test
collection in environments without compiled C extensions.

This shim provides minimal modules used during import-time checks (e.g.,
`torch._tensor.Tensor`) so tests that only need type references can import
without requiring the real PyTorch wheel.
"""
__all__ = ["_tensor", "_C"]

from . import _tensor  # re-export submodule
from . import _C  # placeholder C-extension module

# Provide a convenience alias for common attribute access
Tensor = _tensor.Tensor
