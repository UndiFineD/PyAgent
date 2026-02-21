"""Minimal type helpers for jsontree package."""

from __future__ import annotations
from typing import Any, List, Union

JSONKey = Union[str, int]
JSONPath = List[JSONKey]
JSONType = Any

__all__ = ["JSONKey", "JSONPath", "JSONType"]
