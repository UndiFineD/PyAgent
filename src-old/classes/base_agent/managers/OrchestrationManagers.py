#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/base_agent/managers/OrchestrationManagers.description.md

# OrchestrationManagers

**File**: `src\classes\base_agent\managers\OrchestrationManagers.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 14 imports  
**Lines**: 137  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for OrchestrationManagers.

## Classes (4)

### `AgentComposer`

Composer for multi-agent workflows.

**Methods** (5):
- `__init__(self)`
- `add_agent(self, agent)`
- `_calculate_execution_order(self)`
- `execute(self, file_path, prompt, agent_factory)`
- `get_final_result(self)`

### `ModelSelector`

Selects models for different agent types. Supports GLM-4.7 and DeepSeek V4 (roadmap).

**Methods** (3):
- `__post_init__(self)`
- `select(self, agent_type, token_estimate)`
- `set_model(self, agent_type, config)`

### `QualityScorer`

Scores response quality.

**Methods** (2):
- `add_criterion(self, name, func, weight)`
- `score(self, text)`

### `ABTest`

A/B test for variants.

**Methods** (2):
- `__post_init__(self)`
- `select_variant(self)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `agent.BaseAgent`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `random`
- `src.core.base.models.ComposedAgent`
- `src.core.base.models.ModelConfig`
- `src.core.base.models._empty_list_float`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/managers/OrchestrationManagers.improvements.md

# Improvements for OrchestrationManagers

**File**: `src\classes\base_agent\managers\OrchestrationManagers.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 137 lines (medium)  
**Complexity**: 12 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `OrchestrationManagers_test.py` with pytest tests

### Code Organization
- [TIP] **4 classes in one file** - Consider splitting into separate modules

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from src.core.base.version import VERSION
import logging
import random
from ..agent import BaseAgent
from dataclasses import dataclass, field
from typing import Dict, List, TYPE_CHECKING
from collections.abc import Callable
from src.core.base.models import ModelConfig, ComposedAgent, _empty_list_float

__version__ = VERSION

class AgentComposer:
    """Composer for multi-agent workflows."""

    def __init__(self) -> None:
        self.agents: list[ComposedAgent] = []
        self.results: dict[str, str] = {}
        self.execution_order: list[str] = []

    def add_agent(self, agent: ComposedAgent) -> None:
        self.agents.append(agent)
        self._calculate_execution_order()

    def _calculate_execution_order(self) -> None:
        sorted_agents: list[str] = []
        visited: set[str] = set()
        temp: set[str] = set()

        def visit(agent_type: str) -> None:
            if agent_type in temp:
                raise ValueError(f"Circular dependency for {agent_type}")
            if agent_type in visited:
                return
            temp.add(agent_type)
            agent = next((a for a in self.agents if a.agent_type == agent_type), None)
            if agent:
                for dep in agent.depends_on:
                    visit(dep)
            temp.remove(agent_type)
            visited.add(agent_type)
            sorted_agents.append(agent_type)

        for agent in sorted(self.agents, key=lambda a: a.order):
            if agent.agent_type not in visited:
                visit(agent.agent_type)
        self.execution_order = sorted_agents

    def execute(
        self,
        file_path: str,
        prompt: str,
        agent_factory: Callable[[str, str], BaseAgent],
    ) -> dict[str, str]:
        self.results.clear()
        current_content = ""
        for agent_type in self.execution_order:
            agent_config = next(
                (a for a in self.agents if a.agent_type == agent_type), None
            )
            if not agent_config:
                continue
            agent = agent_factory(agent_type, file_path)
            enhanced_prompt = prompt
            for dep in agent_config.depends_on:
                if dep in self.results:
                    enhanced_prompt += (
                        f"\\n\\nPrevious {dep} result:\\n{self.results[dep][:500]}"
                    )
            if current_content:
                agent.previous_content = current_content
            result = agent.improve_content(enhanced_prompt)
            self.results[agent_type] = result
            current_content = result
        return self.results

    def get_final_result(self) -> str:
        if not self.execution_order:
            return ""
        return self.results.get(self.execution_order[-1], "")


@dataclass
class ModelSelector:
    """Selects models for different agent types. Supports GLM-4.7 and DeepSeek V4 (roadmap)."""

    models: dict[str, ModelConfig] = field(
        default_factory=lambda: {
            "default": ModelConfig(model_id="gpt-3.5-turbo"),
            "coding": ModelConfig(model_id="glm-4.7"),
            "reasoning": ModelConfig(model_id="deepseek-reasoner"),
        }
    )

    def __post_init__(self) -> None:
        if "default" not in self.models:
            self.models["default"] = ModelConfig(model_id="gpt-3.5-turbo")

    def select(self, agent_type: str, token_estimate: int = 0) -> ModelConfig:
        """
        Selects model based on agent type and token size.
        Phase 129: High-token coding tasks route to GLM-4.7 for cost efficiency.
        """
        if agent_type == "coding" and token_estimate > 4000:
            logging.info(
                f"High-token task ({token_estimate}) routing to GLM-4.7 for cost optimization."
            )
            return self.models.get("coding", self.models["default"])

        return self.models.get(agent_type, self.models["default"])

    def set_model(self, agent_type: str, config: ModelConfig) -> None:
        self.models[agent_type] = config


@dataclass
class QualityScorer:
    """Scores response quality."""

    criteria: dict[str, tuple[Callable[[str], float], float]] = field(
        default_factory=dict
    )

    def add_criterion(
        self, name: str, func: Callable[[str], float], weight: float = 1.0
    ) -> None:
        self.criteria[name] = (func, weight)

    def score(self, text: str) -> float:
        if not self.criteria:
            return min(1.0, len(text) / 200.0)
        total_weight, total_score = 0.0, 0.0
        for func, weight in self.criteria.values():
            total_score += func(text) * weight
            total_weight += weight
        return total_score / total_weight if total_weight > 0 else 0.0


@dataclass
class ABTest:
    """A/B test for variants."""

    name: str
    variants: list[str]
    weights: list[float] = field(default_factory=_empty_list_float)
    variant_counts: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for variant in self.variants:
            self.variant_counts[variant] = 0
        if not self.weights:
            self.weights = [1.0 / len(self.variants)] * len(self.variants)

    def select_variant(self) -> str:
        return random.choices(self.variants, weights=self.weights, k=1)[0]
