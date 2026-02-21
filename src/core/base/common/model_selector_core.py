#!/usr/bin/env python3
from __future__ import annotations

"""Parser-safe `ModelSelectorCore` fallback.

Provides a minimal, deterministic interface for selecting models so
dependent modules can import during repair workflows.
"""
from typing import Dict, Optional


class ModelSelectorCore:
    """Conservative model selection helper."""

    def __init__(self, default_model: str = "gpt-3.5-turbo") -> None:
        self._models: Dict[str, str] = {"default": default_model}

    def register(self, name: str, model_id: str) -> None:
        self._models[name] = model_id

    def select(self, agent_type: Optional[str] = None, token_estimate: int = 0) -> str:
        """Select a model id given an agent type and optional token estimate."""
        if agent_type == "coding" and token_estimate > 4000:
            return self._models.get("coding", self._models["default"])
        return self._models.get(agent_type or "default", self._models["default"])