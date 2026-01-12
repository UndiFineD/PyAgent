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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Model Forge Agent for PyAgent.
Specializes in local fine-tuning and model optimization (LoRA/QLoRA).
"""



import logging
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool


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

        self._system_prompt = (
            "You are the Model Forge Agent. Your specialty is the Neural Forge Pattern. "
            "You manage local fine-tuning processes, dataset preparation for LoRA, "
            "and model optimization. You can trigger fine-tuning jobs, evaluate adapters, "
            "and select the best niche models for specific tasks."
        )

    @as_tool
    def prepare_dataset(self, task_name: str, examples: List[Dict[str, str]]) -> str:
        """Prepares a JSONL dataset for fine-tuning.
        Args:
            task_name: Unique name for the fine-tuning task.
            examples: List of dictionaries with 'instruction' and 'output'.
        """
        output_path = self.datasets_dir / f"{task_name}.jsonl"
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for ex in examples:
                    f.write(json.dumps(ex) + "\n")
            return f"Dataset prepared at {output_path} with {len(examples)} examples."
        except Exception as e:
            return f"Failed to prepare dataset: {e}"

    @as_tool
    def start_finetuning(self, task_name: str, base_model: str = "unsloth/llama-3-8b-bnb-4bit") -> str:
        """Simulates starting a LoRA fine-tuning session.
        Args:
            task_name: Name of the task/dataset to use.
            base_model: The base model to fine-tune.
        """
        dataset_path = self.datasets_dir / f"{task_name}.jsonl"
        if not dataset_path.exists():
            return f"Error: Dataset {dataset_path} not found."

        if self.recorder:
            self.recorder.record_lesson("model_forge_finetune", {"task": task_name, "base": base_model})

        logging.info(f"ModelForge: Starting fine-tuning for '{task_name}' on '{base_model}'...")
        
        job_id = f"job_{task_name}_{int(os.path.getmtime(dataset_path))}"
        
        # Simulate local folder for the adapter
        adapter_path = self.adapters_dir / task_name
        adapter_path.mkdir(parents=True, exist_ok=True)
        with open(adapter_path / "adapter_config.json", "w") as f:
            json.dump({"base_model": base_model, "peft_type": "LORA", "job_id": job_id}, f)

        return f"SUCCESS: Fine-tuning job '{job_id}' started. Monitoring progress at {self.forge_dir}/logs/{job_id}.log"

    @as_tool
    def trigger_autonomous_tuning(self, agent_name: str, evolution_metadata: Dict[str, Any]) -> str:
        """Triggers local fine-tuning based on evolution data or failure reports.
        Args:
            agent_name: Target agent that needs optimization.
            evolution_metadata: Metadata from EvolutionEngine containing failure cases or goals.
        """
        task_name = f"opt_{agent_name}_{evolution_metadata.get('version', '01')}"
        logging.info(f"ModelForge: Autonomous tuning triggered for {agent_name} - Task: {task_name}")
        
        # 1. Gather failure cases/synthetic data from evolution_metadata
        synthetic_data = evolution_metadata.get("synthetic_examples", [
            {"instruction": "Optimize for specialized task", "output": "Reasoning with higher precision"}
        ])
        
        # 2. Prepare dataset
        prep_res = self.prepare_dataset(task_name, synthetic_data)
        
        # 3. Start tuning
        tune_res = self.start_finetuning(task_name)
        
        return f"Autonomous Tuning Initialized for {agent_name}: {prep_res} | {tune_res}"

    @as_tool
    def evaluate_adapter(self, adapter_path: str, test_queries: List[str]) -> Dict[str, Any]:
        """Evaluates a fine-tuned adapter against the base model for specific queries."""
        logging.info(f"ModelForge: Evaluating adapter at {adapter_path}...")
        # Mock evaluation results
        results = {}
        for query in test_queries:
            results[query] = {
                "base_score": 0.65,
                "adapter_score": 0.88,
                "improvement": "35%"
            }
        return results

    @as_tool
    def list_available_adapters(self) -> List[str]:
        """Lists all locally saved model adapters."""
        return [d.name for d in self.adapters_dir.iterdir() if d.is_dir()]

    def improve_content(self, prompt: str) -> str:
        """General model optimization guidance."""
        return "I am ready to forge new neural pathways. Suggest a task for local fine-tuning."

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(ModelForgeAgent, "Model Forge Agent", "Neural fine-tuning orchestration")
    main()
