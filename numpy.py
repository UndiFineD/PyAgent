#!/usr/bin/env python3
"""Lightweight numpy shim for test environments without numpy installed.
This provides minimal helpers used by the test-collection path (dot, linalg.norm, asarray).
Not a replacement for real numpy; intended only to let static imports succeed in CI/test sandbox.
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence, List, Any


def asarray(x: Iterable) -> list:
    """Convert an iterable to a list (numpy array-like)."""
    return list(x)


def array(x: Iterable) -> list:
    """Alias for asarray to satisfy common import patterns."""
    return asarray(x)


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute the dot product of two vectors."""
    return sum(float(x) * float(y) for x, y in zip(a, b))


class Linalg:
    """Minimal linear algebra utilities."""
    @staticmethod
    def norm(a: Sequence[float]) -> float:
        """Compute the Euclidean norm of a vector."""
        return math.sqrt(sum(float(x) * float(x) for x in a))


# Alias for backward compatibility with numpy import pattern
linalg = Linalg

__all__ = ["asarray", "array", "dot", "linalg"]

# Minimal aliases to satisfy simple type checks and annotations that expect numpy.ndarray
ndarray = list
# ensure both names are present
array = asarray
asarray = asarray

__version__ = "0.0"
# Minimal dtype aliases used in type annotations
float32 = float
float64 = float
int32 = int
int64 = int
float16 = float
int8 = int
int16 = int
uint8 = int
uint16 = int
uint32 = int
uint64 = int
# Additional dtype aliases used by SciPy and other downstream libs
intc = int
intp = int
int_ = int
uint = int

# Module-level __getattr__ to gracefully provide simple dtype fallbacks
def __getattr__(name: str) -> Any:
    """Provides simple numeric type fallbacks for attributes like 'float32', 'int64', etc."""
    # Provide simple numeric type fallbacks used in import-time checks
    if name.startswith("int") or name.startswith("uint"):
        return int
    if name.startswith("float") or name in ("double", "single"):
        return float
    if name.startswith("complex"):
        return complex
    if name in ("bool", "bool_"):
        return bool
    raise AttributeError(f"module 'numpy' has no attribute '{name}'")

# Minimal complex dtype aliases
complex64 = complex
complex128 = complex
complex_ = complex
# Minimal dtype factory placeholder
def dtype(t: Any) -> Any:
    """Placeholder dtype factory that returns the type itself for simplicity."""
    return t
