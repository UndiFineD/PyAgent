"""
Orchestration Managers for multi-agent workflows.
(Facade for src.core.base.common.orchestration_core)
"""

from __future__ import annotations
from src.core.base.common.orchestration_core import (
    OrchestrationCore as AgentComposer,
    QualityScorer,
    ABTest
)
from src.core.base.common.model_selector_core import ModelSelectorCore as ModelSelector

