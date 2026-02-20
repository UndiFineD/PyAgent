#!/usr/bin/env python3
"""Minimal GuardrailCore for tests."""
from __future__ import annotations


import json
import logging
from typing import Any, Dict


class GuardrailCore:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.rules: Dict[str, Any] = {}

    def load_rules(self, data: str) -> bool:
        try:
            self.rules = json.loads(data)
            return True
        except Exception:
            return False

    def check(self, prompt: str) -> bool:
        # Always pass in minimal implementation
        return True


__all__ = ["GuardrailCore"]
