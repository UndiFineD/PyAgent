#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/SynthesisAgent.description.md

# SynthesisAgent

**File**: `src\classes\specialized\SynthesisAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 113  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for SynthesisAgent.

## Classes (1)

### `SynthesisAgent`

**Inherits from**: BaseAgent

Tier 2 (Cognitive Logic) - Synthesis Agent: Responsible for Swarm Synthesis, 
merging specialized agent capabilities into optimized super-agent architectures.

**Methods** (3):
- `__init__(self, workspace_root)`
- `fuse_agents(self, agent_names, new_agent_name)`
- `analyze_fusion_candidates(self, fleet_agents)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `os`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/SynthesisAgent.improvements.md

# Improvements for SynthesisAgent

**File**: `src\classes\specialized\SynthesisAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 113 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SynthesisAgent_test.py` with pytest tests

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

import logging
import os
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

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

__version__ = VERSION


class SynthesisAgent(BaseAgent):
    """Tier 2 (Cognitive Logic) - Synthesis Agent: Responsible for Swarm Synthesis,
    merging specialized agent capabilities into optimized super-agent architectures.
    """

    def __init__(self, workspace_root: str) -> None:
        # Initialize with a dummy path as base_agent needs a file path
        dummy_path = os.path.join(
            workspace_root, "src/logic/agents/cognitive/SynthesisAgent.py"
        )
        super().__init__(dummy_path)
        self.workspace_root = workspace_root
        self._system_prompt = (
            "You are the Synthesis Agent. "
            "Your goal is to merge distinct agent capabilities into high-performance Super-Agents. "
            "You create new Python class files that combine multiple tools into a cohesive whole, "
            "optimizing for reduced inter-agent communication overhead."
        )

    @as_tool
    def fuse_agents(
        self, agent_names: list[str], new_agent_name: str
    ) -> dict[str, Any]:
        """Creates a new agent that combines functionalities of multiple source agents.

        Args:
            agent_names: List of existing agent class names to fuse.
            new_agent_name: The name of the new fused agent class.

        """
        logging.info(f"SynthesisAgent: Fusing {agent_names} into {new_agent_name}")

        # Step 1: Analyze the source agents (simulated)
        # We would normally read their files and extract tools.

        # Step 2: Use LLM to generate fused agent code
        prompt = (
            f"I want to create a new agent named {new_agent_name} that combines the features "
            f"of these source agents: {', '.join(agent_names)}.\n"
            "The new agent should inherit from BaseAgent and use the @as_tool decorator for all combined capabilities.\n"
            "Generate the full Python code for this new agent class. include all necessary imports.\n"
            "Make sure the class name is exactly " + new_agent_name + "."
        )

        agent_code = self.think(prompt)

        # Clean up code markup if present
        if "```python" in agent_code:
            agent_code = agent_code.split("```python")[1].split("```")[0].strip()
        elif "```" in agent_code:
            agent_code = agent_code.split("```")[1].split("```")[0].strip()

        # Step 3: Save the new agent file
        target_dir = os.path.join(self.workspace_root, "src/agents")
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, f"{new_agent_name}.py")

        try:
            with open(file_path, "w") as f:
                f.write(agent_code)

            logging.info(f"SynthesisAgent: Successfully created {file_path}")

            return {
                "status": "success",
                "new_agent": new_agent_name,
                "file_path": file_path,
                "components_fused": agent_names,
            }
        except Exception as e:
            logging.error(f"SynthesisAgent: Failed to save fused agent: {e}")
            return {"status": "error", "message": str(e)}

    @as_tool
    def analyze_fusion_candidates(
        self, fleet_agents: list[str]
    ) -> list[dict[str, Any]]:
        """Analyzes the fleet to suggest which agents should be fused based on usage patterns.
        """
        logging.info("SynthesisAgent: Analyzing fleet for fusion candidates.")
        # This would typically use telemetry to find agents that frequently call each other.
        # For now, we suggest a logical fusion.
        return [
            {
                "agents": ["ReasoningAgent", "ReflectionAgent"],
                "target": "CognitiveSuperAgent",
                "reason": "High frequency of sequential calling in reasoning loops",
            }
        ]
