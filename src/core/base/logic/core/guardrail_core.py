#!/usr/bin/env python3
"""Guardrail core - minimal parser-safe implementation."""
from __future__ import annotations

import logging
from typing import Any, Dict


class GuardrailCore:
    """Conservative guardrail helper used during repair."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.rules: Dict[str, Any] = {}

    def check(self, prompt: str) -> bool:
        """Return True for repair-time safety stub."""
        return True


__all__ = ["GuardrailCore"]
