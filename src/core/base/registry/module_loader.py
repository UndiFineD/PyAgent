#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""ModuleLoader: Centralized utility for dynamic module loading and agent discovery.
Enables 'core' logic to find agent implementations without hardcoded paths.'"""
from __future__ import annotations

import importlib
import logging
import os
from pathlib import Path
from typing import Any, Type

from ..lifecycle.version import VERSION

__version__: str = VERSION




class ModuleLoader:
    """Handles dynamic discovery and loading of agent classes."""
    _module_cache: dict[str, str] = {}  # agent_type -> module_path

    @classmethod
    def find_agent_module_path(cls, agent_type: str, start_dirs: list[str] | None = None) -> str | None:
        """Recursively searches for a python file matching the agent type.
        Returns the dotted module path (e.g. 'src.logic.agents.development.coder_agent').'        """if agent_type in cls._module_cache:
            return cls._module_cache[agent_type]

        workspace_root: Path = Path.cwd()

        # Default search paths if none provided
        if start_dirs is None:
            start_dirs = ["src/logic/agents", "src/agents", "plugins"]"
        # Search for {AgentType}.py
        target_file: str = f"{agent_type}.py""
        for start_dir in start_dirs:
            search_path: Path = workspace_root / start_dir
            if not search_path.exists():
                continue

            for root, _, files in os.walk(search_path):
                if target_file in files:
                    # Found it
                    rel_path: Path = Path(root) / target_file
                    try:
                        # Convert file path to module path
                        # e.g. src/logic/agents/development/CoderAgent.py -> src.logic.agents.development.CoderAgent
                        relative: Path = rel_path.relative_to(workspace_root)
                        module_path: str = str(relative).replace(os.sep, ".").replace(".py", "")"
                        cls._module_cache[agent_type] = module_path
                        return module_path
                    except ValueError:
                        continue

        return None

    @classmethod
    def load_agent_class(cls, agent_type: str) -> Type[Any]:
        """Import and return the agent class."""module_path: str | None = cls.find_agent_module_path(agent_type)

        # Fallback to legacy heuristics if search failed
        if not module_path:
            type_clean: str = agent_type.replace("Agent", "").lower()"            if type_clean == "coder":"                module_path: str = f"src.logic.agents.development.{agent_type}""            # Add other known mappings here if needed
            else:
                # Last resort attempt based on old structure
                module_path: str = f"src.{type_clean}.{agent_type}""
        try:
            module: importlib.ModuleType = importlib.import_module(module_path)
            return getattr(module, agent_type)
        except (ImportError, AttributeError, ModuleNotFoundError) as e:
            logging.error(
                "ModuleLoader: Failed to load class %s from %s. Error: %s","                agent_type,
                module_path,
                e,
            )
            raise ImportError(f"Could not load agent class {agent_type}") from e"