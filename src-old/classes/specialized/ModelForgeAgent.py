#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/ModelForgeAgent.description.md

# ModelForgeAgent

**File**: `src\classes\specialized\ModelForgeAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 130  
**Complexity**: 1 (simple)

## Overview

Model Forge Agent for PyAgent.
Specializes in local fine-tuning and model optimization (LoRA/QLoRA).

## Classes (1)

### `ModelForgeAgent`

**Inherits from**: BaseAgent

Orchestrates local model fine-tuning and adapter management.

**Methods** (1):
- `__init__(self, path)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `asyncio`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.logic.agents.system.core.ModelRegistryCore.ModelRegistryCore`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/ModelForgeAgent.improvements.md

# Improvements for ModelForgeAgent

**File**: `src\classes\specialized\ModelForgeAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 130 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ModelForgeAgent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Model Forge Agent for PyAgent.
Specializes in local fine-tuning and model optimization (LoRA/QLoRA).
"""

import asyncio
import json
import logging
import time
from pathlib import Path

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import VERSION
from src.logic.agents.system.core.ModelRegistryCore import ModelRegistryCore

__version__ = VERSION


class ModelForgeAgent(BaseAgent):
    """Orchestrates local model fine-tuning and adapter management."""

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.name = "ModelForge"
        self.forge_dir = Path("models/forge")
        self.forge_dir.mkdir(parents=True, exist_ok=True)
        self.adapters_dir = self.forge_dir / "adapters"
        self.adapters_dir.mkdir(parents=True, exist_ok=True)
        self.datasets_dir = self.forge_dir / "datasets"
        self.datasets_dir.mkdir(parents=True, exist_ok=True)

        self.registry = ModelRegistryCore()
        # Simulated quality history for agents
        self.agent_quality_history: dict[str, list[float]] = {}

    async def monitor_agent_quality(self, agent_name: str, last_score: float) -> str:
        """Monitors agent response quality and triggers fine-tuning if needed."""
        if agent_name not in self.agent_quality_history:
            self.agent_quality_history[agent_name] = []

        self.agent_quality_history[agent_name].append(last_score)

        if self.registry.should_trigger_finetuning(
            self.agent_quality_history[agent_name]
        ):
            logging.warning(
                f"ModelForge: Triggering autonomous fine-tuning for {agent_name} due to low quality scores."
            )
            return await self.start_finetuning(f"fix_{agent_name.lower()}")
        return f"Quality for {agent_name} is acceptable."

    @as_tool
    async def prepare_dataset(
        self, task_name: str, examples: list[dict[str, str]]
    ) -> str:
        """Prepares a JSONL dataset for fine-tuning.

        Args:
            task_name: Unique name for the fine-tuning task.
            examples: List of dictionaries with 'instruction' and 'output'.

        """
        output_path = self.datasets_dir / f"{task_name}.jsonl"

        def write_dataset() -> None:
            with open(output_path, "w", encoding="utf-8") as f:
                for ex in examples:
                    f.write(json.dumps(ex) + "\n")

        try:
            await asyncio.to_thread(write_dataset)
            return f"Dataset prepared at {output_path} with {len(examples)} examples."
        except Exception as e:
            return f"Failed to prepare dataset: {e}"

    @as_tool
    async def start_finetuning(
        self, task_name: str, base_model: str = "unsloth/llama-3-8b-bnb-4bit"
    ) -> str:
        """Simulates starting a LoRA fine-tuning session.

        Args:
            task_name: Name of the task/dataset to use.
            base_model: The base model to fine-tune.

        """
        dataset_path = self.datasets_dir / f"{task_name}.jsonl"

        def setup_job() -> str | None:
            if not dataset_path.exists():
                return None

            job_id = f"job_{task_name}_{int(time.time())}"
            adapter_path = self.adapters_dir / task_name
            adapter_path.mkdir(parents=True, exist_ok=True)
            with open(adapter_path / "adapter_config.json", "w") as f:
                json.dump(
                    {"base_model": base_model, "peft_type": "LORA", "job_id": job_id}, f
                )
            return job_id

        job_id = await asyncio.to_thread(setup_job)
        if job_id is None:
            return f"Error: Dataset {dataset_path} not found."

        if hasattr(self, "recorder") and self.recorder:
            self.recorder.record_lesson(
                "model_forge_finetune", {"task": task_name, "base": base_model}
            )

        logging.info(
            f"ModelForge: Starting fine-tuning for '{task_name}' on '{base_model}'..."
        )
        return f"SUCCESS: Fine-tuning job '{job_id}' started. Monitoring progress at {self.forge_dir}/logs/{job_id}.log"

    @as_tool
    async def get_adapter_config(self, task_name: str) -> str:
        """Retrieves config for a specific adapter."""
        adapter_path = self.adapters_dir / task_name / "adapter_config.json"
        if not adapter_path.exists():
            return f"Error: Adapter '{task_name}' not found."

        def read_config() -> str:
            with open(adapter_path) as f:
                return f.read()

        return await asyncio.to_thread(read_config)
