#!/usr/bin/env python3
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


"""Model Forge Agent for PyAgent.
Specializes in local fine-tuning and model optimization (LoRA/QLoRA).
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import json
import asyncio
import time
from pathlib import Path
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool
from src.logic.agents.system.core.ModelRegistryCore import ModelRegistryCore

__version__ = VERSION


class ModelForgeAgent(BaseAgent):
    """Orchestrates local model fine-tuning and adapter management."""

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.name = "ModelForge"
        self.forge_dir = Path("data/forge")
        self.forge_dir.mkdir(parents=True, exist_ok=True)
        self.adapters_dir = self.forge_dir / "adapters"
        self.adapters_dir.mkdir(parents=True, exist_ok=True)
        self.datasets_dir = Path("data/forge/datasets")
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
    async def trigger_autonomous_tuning(
        self, module_name: str, evolution_data: dict[str, Any]
    ) -> str:
        """
        Triggers an autonomous fine-tuning loop for a specific agent/module.
        Args:
            module_name: The target agent or module (e.g., 'SQLAgent').
            evolution_data: Dictionary containing 'version' and 'synthetic_examples'.
        """
        version = evolution_data.get("version", "v1")
        examples = evolution_data.get("synthetic_examples", [])

        task_name = f"opt_{module_name}_{version}"

        # 1. Prepare Dataset
        await self.prepare_dataset(task_name, examples)

        # 2. Start Fine-tuning (Mock)
        job_id = await self.start_finetuning(task_name)

        if job_id:
            return f"SUCCESS: Fine-tuning job {job_id} started for {task_name}. Autonomous Tuning Initialized."
        return "FAILED: Could not start fine-tuning job."

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
            # Save config to data/config (Phase 282: Dedicated config storage)
            config_path = Path("data/config") / f"{task_name}_adapter_config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(
                    {"base_model": base_model, "peft_type": "LORA", "job_id": job_id}, f
                )

            # Keep adapter directory for other artifacts
            adapter_path = self.adapters_dir / task_name
            adapter_path.mkdir(parents=True, exist_ok=True)
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
        # Check central config store first
        adapter_path = Path("data/config") / f"{task_name}_adapter_config.json"
        if not adapter_path.exists():
            # Fallback to legacy path
            adapter_path = self.adapters_dir / task_name / "adapter_config.json"

        if not adapter_path.exists():
            return f"Error: Adapter '{task_name}' not found."

        def read_config() -> str:
            with open(adapter_path) as f:
                return f.read()

        return await asyncio.to_thread(read_config)
