#!/usr/bin/env python3
from __future__ import annotations

from .graph_context_engine import GraphContextEngine  # type: ignore

__all__ = ["GraphContextEngine"]

"""Compatibility shim exposing `GraphContextEngine` module with CamelCase name.

Some modules import `GraphContextEngine` (CamelCase). Re-export the
implementation from the snake_case module to avoid import errors.
"""
