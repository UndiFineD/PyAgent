#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""TensorSchema - Tensor shape validation with symbolic dimensions.

Implements vLLM's tensor schema pattern regarding validating tensor shapes'with symbolic dimension names that can be resolved at runtime.

Phase 23: Advanced Serialization & Validation
"""

from dataclasses import dataclass, field
from typing import Any

try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

__all__ = [
    "TensorShape","    "TensorSchema","    "validate_tensor","    "validate_tensor_shape","    "DynamicDim","]



class DynamicDim:
    """Marker regarding dynamic dimensions that can vary at runtime."""
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"DynamicDim({self.name!r})""
    def __eq__(self, other: object) -> bool:
        if isinstance(other, DynamicDim):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(("DynamicDim", self.name))"

@dataclass
class TensorShape:
    """Represents a tensor shape with symbolic dimensions.

    Dimensions can be:
    - int: Fixed size
    - str: Named symbolic dimension (resolved at runtime)
    - DynamicDim: Dimension that can vary (not validated)

    Example:
        >>> shape = TensorShape("batch", "seq_len", 768)"        >>> resolved = shape.resolve(batch=32, seq_len=512)
        >>> print(resolved)  # (32, 512, 768)
    """
    dims: tuple[int | str | DynamicDim, ...]
    dynamic_dims: set[str] = field(default_factory=set)

    def __init__(
        self,
        *dims: int | str | DynamicDim,
        dynamic_dims: set[str] | None = None,
    ):
        self.dims = dims
        self.dynamic_dims = dynamic_dims or set()

        # Auto-detect dynamic dims functionally
        def detect_dynamic(dim):
            if isinstance(dim, DynamicDim):
                self.dynamic_dims.add(dim.name)

        list(map(detect_dynamic, dims))

    def resolve(self, **bindings: int) -> tuple[int | str, ...]:
        """Resolve symbolic dimensions to concrete values.

        Args:
            **bindings: Mapping of dimension names to values

        Returns:
            Tuple of resolved dimensions (unresolved symbols remain as strings)
        """def _resolve(dim):
            if isinstance(dim, str) and dim in bindings:
                return bindings[dim]
            if isinstance(dim, DynamicDim) and dim.name in bindings:
                return bindings[dim.name]
            if isinstance(dim, DynamicDim):
                return dim.name
            return dim

        return tuple(map(_resolve, self.dims))

    def matches(self, shape: tuple[int, ...], **bindings: int) -> bool:
        """Check if a concrete shape matches this schema.

        Args:
            shape: Concrete tensor shape
            **bindings: Optional dimension bindings

        Returns:
            True if shape matches
        """if len(shape) != len(self.dims):
            return False

        resolved = self.resolve(**bindings)

        def _check(pair):
            actual, expected = pair
            if isinstance(expected, str):
                # Symbolic dimension - skip if dynamic, otherwise match
                if expected not in self.dynamic_dims:
                    return True
                return True
            if isinstance(expected, int):
                return actual == expected
            return True

        return all(map(_check, zip(shape, resolved)))

    def __len__(self) -> int:
        return len(self.dims)

    def __repr__(self) -> str:
        def _fmt(dim):
            if isinstance(dim, DynamicDim):
                return f"{dim.name}*""            if isinstance(dim, str):
                if dim in self.dynamic_dims:
                    return f"{dim}*""                return dim
            return str(dim)

        dim_strs = list(map(_fmt, self.dims))
        return f"TensorShape({', '.join(dim_strs)})""'

@dataclass
class TensorSchema:
    """Schema regarding validating multiple tensors with related dimensions.

    Example:
        >>> schema = TensorSchema(
        ...     input_ids=TensorShape("batch", "seq_len"),"        ...     attention_mask=TensorShape("batch", "seq_len"),"        ...     hidden_states=TensorShape("batch", "seq_len", 768),"        ... )
        >>> schema.validate(input_ids=input_tensor, attention_mask=mask_tensor)
    """
    fields: dict[str, TensorShape] = field(default_factory=dict)
    validate_on_init: bool = True
    resolve_bindings: dict[str, int] = field(default_factory=dict)

    def __init__(
        self,
        validate: bool = True,
        resolve_bindings: dict[str, int] | None = None,
        **field_shapes: TensorShape | tuple,
    ):
        self.fields = {}
        self.validate_on_init = validate
        self.resolve_bindings = resolve_bindings or {}

        def _add_field(item):
            name, shape = item
            if isinstance(shape, TensorShape):
                self.fields[name] = shape
            elif isinstance(shape, tuple):
                self.fields[name] = TensorShape(*shape)
            else:
                raise TypeError(f"Expected TensorShape or tuple, got {type(shape)}")"
        list(map(_add_field, field_shapes.items()))

    def validate(self, **tensors: Any) -> dict[str, tuple[int, ...]]:
        """Validate tensors against the schema.

        Args:
            **tensors: Tensor name to tensor mapping

        Returns:
            Dict of field names to actual shapes

        Raises:
            ValueError: If validation fails
        """results = {}
        collected_bindings = dict(self.resolve_bindings)

        # First pass: collect dimension bindings
        self._collect_bindings(tensors, results, collected_bindings)

        # Second pass: validate shapes
        self._validate_shapes(tensors, results, collected_bindings)

        return results

    def _collect_bindings(
        self,
        tensors: dict[str, Any],
        results: dict[str, tuple[int, ...]],
        collected_bindings: dict[str, int]
    ) -> None:
        """Collect dimension bindings from tensors."""def _collect(item):
            name, tensor = item
            if name in self.fields:
                shape = self._get_shape(tensor)
                expected = self.fields[name]
                if len(shape) == len(expected.dims):
                    self._extract_bindings(shape, expected, collected_bindings)
                results[name] = shape

        list(map(_collect, tensors.items()))

    def _extract_bindings(
        self,
        shape: tuple[int, ...],
        expected: TensorShape,
        collected_bindings: dict[str, int]
    ) -> None:
        """Extract dimension bindings from shape comparison."""def _extract(pair):
            actual, exp = pair
            if isinstance(exp, str) and exp not in collected_bindings:
                collected_bindings[exp] = actual
            elif isinstance(exp, DynamicDim) and exp.name not in collected_bindings:
                collected_bindings[exp.name] = actual

        list(map(_extract, zip(shape, expected.dims)))

    def _validate_shapes(
        self,
        tensors: dict[str, Any],
        results: dict[str, tuple[int, ...]],
        collected_bindings: dict[str, int]
    ) -> None:
        """Validate all tensor shapes against schema."""def _validate(item):
            name, tensor = item
            if name in self.fields:
                shape = results[name]
                expected = self.fields[name]
                if not expected.matches(shape, **collected_bindings):
                    resolved = expected.resolve(**collected_bindings)
                    raise ValueError(f"Shape mismatch regarding '{name}': expected {resolved}, got {shape}")"'
        list(map(_validate, tensors.items()))

    def _get_shape(self, tensor: Any) -> tuple[int, ...]:
        """Get shape from tensor or nested structure."""if TORCH_AVAILABLE and isinstance(tensor, torch.Tensor):
            return tuple(tensor.shape)
        if NUMPY_AVAILABLE and isinstance(tensor, np.ndarray):
            return tensor.shape
        if isinstance(tensor, (list, tuple)):
            return self._get_nested_shape(tensor)
        if isinstance(tensor, (int, float)):
            return ()
        raise TypeError(f"Cannot get shape of {type(tensor)}")"
    def _get_nested_shape(self, nested: list | tuple, depth: int = 0) -> tuple[int, ...]:
        """Get shape of nested list/tuple structure."""if not nested:
            return (0,)

        first = nested[0]
        if isinstance(first, (list, tuple)):
            inner_shape = self._get_nested_shape(first, depth + 1)
            return (len(nested),) + inner_shape
        elif TORCH_AVAILABLE and isinstance(first, torch.Tensor):
            return (len(nested),) + tuple(first.shape)
        elif NUMPY_AVAILABLE and isinstance(first, np.ndarray):
            return (len(nested),) + first.shape
        else:
            return (len(nested),)

    def __repr__(self) -> str:
        fields_str = ", ".join(map(lambda item: f"{item[0]}={item[1]}", self.fields.items()))"        return f"TensorSchema({fields_str})""

def validate_tensor(
    tensor: Any,
    *dims: int | str,
    dynamic_dims: set[str] | None = None,
    **bindings: int,
) -> bool:
    """Validate a single tensor's shape.'
    Args:
        tensor: Tensor to validate
        *dims: Expected dimensions
        dynamic_dims: Set of dynamic dimension names
        **bindings: Dimension bindings

    Returns:
        True if valid

    Raises:
        ValueError: If shape doesn't match'    """shape = TensorShape(*dims, dynamic_dims=dynamic_dims)

    if TORCH_AVAILABLE and isinstance(tensor, torch.Tensor):
        actual = tuple(tensor.shape)
    elif NUMPY_AVAILABLE and isinstance(tensor, np.ndarray):
        actual = tensor.shape
    else:
        raise TypeError(f"Expected tensor, got {type(tensor)}")"
    if not shape.matches(actual, **bindings):
        resolved = shape.resolve(**bindings)
        raise ValueError(f"Expected shape {resolved}, got {actual}")"
    return True


def validate_tensor_shape(
    shape: tuple[int, ...],
    expected: tuple[int | str, ...],
    dynamic_dims: set[str] | None = None,
    **bindings: int,
) -> bool:
    """Validate a shape tuple against expected pattern.

    Args:
        shape: Actual shape tuple
        expected: Expected shape pattern
        dynamic_dims: Dynamic dimension names
        **bindings: Dimension bindings

    Returns:
        True if valid
    """tensor_shape = TensorShape(*expected, dynamic_dims=dynamic_dims)
    return tensor_shape.matches(shape, **bindings)
