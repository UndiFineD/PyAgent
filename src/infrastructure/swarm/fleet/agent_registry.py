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


"""Registry for mapping agent names to their implementations and initialization logic."""

from __future__ import annotations

import importlib
import json
import logging
import os
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.version import SDK_VERSION, VERSION
from src.logic.agents.system.mcp_agent import MCPAgent

from .agent_registry_core import AgentRegistryCore
from .bootstrap_configs import BOOTSTRAP_AGENTS
from .resilient_stubs import ResilientStub

if TYPE_CHECKING:
    from .fleet_manager import FleetManager

# Import local version for gatekeeping
__version__ = VERSION


class LazyAgentMap(dict):
    """A dictionary that instantiates agents only when they are first accessed."""

    def __init__(
        self,
        workspace_root: Path,
        registry_configs: dict[str, tuple] | None = None,
        fleet_instance: FleetManager | None = None,
    ) -> None:
        super().__init__()
        self.workspace_root: Path = workspace_root
        self.registry_configs = registry_configs or BOOTSTRAP_AGENTS
        self.fleet = fleet_instance
        self._instances: dict[str, Any] = {}
        # Refactored: Logic delegated to Core (Rust-ready)
        self.core = AgentRegistryCore(SDK_VERSION)

        # 1. Load Manifest (Plugins)
        self._manifest_configs = self._load_manifests()

        # 2. Dynamic Discovery (The most lazy/flexible)
        # Pre-scan ensures we know what's available without guessing inside __getitem__
        discovered_files = self._scan_workspace_for_agents()
        self._discovered_configs: dict[str, tuple[str, str, str | None]] = self.core.process_discovered_files(
            discovered_files
        )
        logging.info(f"Registry: Discovered {len(self._discovered_configs)} agents dynamically.")

    def _scan_workspace_for_agents(self) -> list[str]:
        """Performs the I/O-bound scanning of the workspace."""
        subdirs = [
            "src/logic/agents/cognitive",
            "src/logic/agents/development",
            "src/logic/agents/infrastructure",
            "src/logic/agents/security",
            "src/logic/agents/swarm",
            "src/logic/agents/system",
            "src/logic/agents/specialized",
            "src/logic/agents/intelligence",
            "src/logic/agents/compliance",
            "src/logic/agents/documentation",
            "plugins",
        ]
        found_paths = []
        for subdir in subdirs:
            search_root = self.workspace_root / subdir
            if not search_root.exists():
                continue
            # Optimization: Only list files to avoid deep recursion if not needed,
            # but keep os.walk for legacy plugin support.
            for root, _, files in os.walk(search_root):
                # Phase 117: Exclude non-agent directories
                if (
                    "context" in Path(root).parts
                    or "models" in Path(root).parts
                    or "utils" in Path(root).parts
                    or "mixins" in Path(root).parts
                ):
                    continue

                for file in files:
                    # Phase 130: Exclude known data classes/enums/utilities
                    if file in [
                        "validation_rule.py",
                        "changelog_entry.py",
                        "changelog_template.py",
                        "versioning_strategy.py",
                        "ValidationRule.py",
                        "ChangelogEntry.py",
                        "VersioningStrategy.py",
                    ]:
                        continue

                    if file.endswith(".py") and not file.startswith("__") and not file.endswith("_mixin.py"):
                        full_path = Path(root) / file
                        rel_path = full_path.relative_to(self.workspace_root)
                        found_paths.append(str(rel_path))
        return found_paths

    def _load_manifests(self) -> dict[str, tuple]:
        """Loads additional configurations from plugins/manifest.json or similar."""
        manifest_configs = {}
        # Support both manifest.json and agent_manifest.json
        manifest_paths: list[Path] = [
            self.workspace_root / "plugins" / "manifest.json",
            self.workspace_root / "plugins" / "agent_manifest.json",
        ]
        for m_path in manifest_paths:
            if m_path.exists():
                try:
                    with open(m_path) as f:
                        data = json.load(f)
                        configs: dict[str, tuple[str, str, str | None]] = self.core.parse_manifest(data)
                        manifest_configs.update(configs)
                except Exception as e:
                    logging.error(f"Failed to load plugin manifest {m_path}: {e}")
        return manifest_configs

    def try_reload(self, key: str) -> bool:
        """Attempts to re-instantiate a failed agent or stub."""
        if key in self._instances:
            logging.info(f"Self-Healing: Attempting reload for {key}...")
            del self._instances[key]
            try:
                instance = self[key]
                if not isinstance(instance, ResilientStub):
                    logging.info(f"Self-Healing: {key} successfully reloaded.")
                    return True
            except Exception:
                pass
        return False

    def check_for_registry_cycles(self) -> None:
        """
        Uses Core logic to ensure no circular dependencies exist in the registry's
        known configurations.
        """
        # Build dependency graph from all configs
        all_configs = {
            **self.registry_configs,
            **self._manifest_configs,
            **self._discovered_configs,
        }
        dep_graph: dict[str, list[str]] = {}

        # Simple heuristic: look for agent names in the config string/list
        for agent_name, cfg in all_configs.items():
            deps = []
            cfg_str = str(cfg).lower()
            for other_name in all_configs:
                if other_name.lower() in cfg_str and other_name != agent_name:
                    deps.append(other_name)
            dep_graph[agent_name] = deps

        cycles = self.core.detect_circular_dependencies(dep_graph)
        if cycles:
            for cycle in cycles:
                logging.error(f"REGISTRY CRITICAL: Circular dependency detected: {' -> '.join(cycle)}")
            raise RecursionError(f"Circular dependencies detected in Agent Registry: {cycles[0]}")

    def keys(self) -> list[str]:
        # Combine all potential keys
        all_ks = set(super().keys())
        all_ks.update(self.registry_configs.keys())
        all_ks.update(self._manifest_configs.keys())
        all_ks.update(self._discovered_configs.keys())
        return list(all_ks)

    def __iter__(self) -> Iterable[str]:
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self.keys())

    def items(self) -> list[tuple[str, Any]]:
        return [(k, self[k]) for k in self.keys()]

    def values(self) -> list[Any]:
        return [self[k] for k in self.keys()]

    def __contains__(self, key: Any) -> bool:
        if super().__contains__(key):
            return True
        if key in self._instances:
            return True
        if key in self.registry_configs:
            return True
        if key in self._manifest_configs:
            return True
        if key in self._discovered_configs:
            return True

        # Case-insensitive check (Phase 104)
        k_norm = str(key).lower().replace("_", "")
        for d_key in self._discovered_configs:
            if d_key.lower().replace("_", "") == k_norm:
                return True
        for d_key in self.registry_configs:
            if d_key.lower().replace("_", "") == k_norm:
                return True

        return False

    def __getitem__(self, key: str) -> Any:
        # 0. Check for manual overrides/instances first
        if key in self._instances:
            return self._instances[key]

        # Also check dict itself (if manually assigned)
        if super().__contains__(key):
            return super().__getitem__(key)

        # 1. Priority 1: Hardcoded configs (Essential bootstrap functions)
        if key in self.registry_configs:
            return self._instantiate(key, self.registry_configs[key])

        # Priority 2: Manifest configs (Registered plugins)
        if key in self._manifest_configs:
            return self._instantiate(key, self._manifest_configs[key])

        # Priority 3: Discovered from File System (Dynamic/Flexible)
        if key in self._discovered_configs:
            return self._instantiate(key, self._discovered_configs[key])

        # Priority 4: Case-insensitive fallback for discovered agents (Phase 104: underscore tolerant)
        k_norm = key.lower().replace("_", "")
        for d_key, d_cfg in self._discovered_configs.items():
            if d_key.lower().replace("_", "") == k_norm:
                return self._instantiate(key, d_cfg)

        raise KeyError(f"Agent '{key}' not found in registry (including dynamic scans).")

    def _instantiate(self, key: str, config: tuple[str, str, str | None]) -> Any:
        """Standard instantiation logic with dependency injection and version checks."""
        module_path, class_name, arg_path_suffix = config

        if module_path == "mcp":
            return self._handle_mcp_agent(key, class_name)

        try:
            module = importlib.import_module(module_path)
            if not self._check_compatibility(key, module):
                return self._instances[key]

            agent_class = self._resolve_agent_class(module, class_name)
            arg = self._get_agent_argument(arg_path_suffix)

            try:
                instance = agent_class(arg)
            except TypeError:
                instance = agent_class()

            self._inject_fleet_and_tools(key, instance)
            self._instances[key] = instance
            return instance

        except (ImportError, SyntaxError) as e:
            logging.error(f"Critical load error for agent {key} from {module_path}: {e}")
            stub = ResilientStub(key, str(e))
            self._instances[key] = stub
            return stub
        except Exception as e:
            logging.error(f"Failed to lazy-load agent {key} from {module_path}: {e}")
            return None

    def _handle_mcp_agent(self, key: str, class_name: str) -> Any:
        """Handles initialization for MCP agents."""
        try:
            instance = MCPAgent(class_name)
            self._instances[key] = instance
            return instance
        except Exception as e:
            logging.error(f"Failed to start MCP Agent {key}: {e}")
            stub = ResilientStub(key, str(e))
            self._instances[key] = stub
            return stub

    def _check_compatibility(self, key: str, module: Any) -> bool:
        """Checks if the agent module is compatible with current SDK version."""
        min_sdk = getattr(module, "SDK_REQUIRED", getattr(module, "__min_sdk__", "1.0.0"))
        if not self.core.is_compatible(min_sdk):
            error_msg = f"Agent '{key}' requires SDK {min_sdk}, but current is {SDK_VERSION}."
            logging.warning(error_msg)
            self._instances[key] = ResilientStub(key, error_msg)
            return False
        return True

    def _resolve_agent_class(self, module: Any, class_name: str) -> type:
        """Finds the agent class within a module using multiple naming conventions."""
        for name in [class_name, f"{class_name}Agent", "Agent"]:
            cls = getattr(module, name, None)
            if cls:
                return cls
        raise AttributeError(f"Module '{module.__name__}' has no attribute matching '{class_name}'.")

    def _get_agent_argument(self, arg_path_suffix: str | None) -> str:
        """Determines the workspace or specific path argument for agent initialization."""
        if arg_path_suffix:
            potential_p = self.workspace_root / arg_path_suffix
            return str(potential_p) if potential_p.exists() else arg_path_suffix
        return str(self.workspace_root)

    def _inject_fleet_and_tools(self, key: str, instance: Any) -> None:
        """Injects fleet reference and registers tools if supported."""
        if not self.fleet:
            return

        if hasattr(instance, "fleet") and getattr(instance, "fleet", None) is None:
            instance.fleet = self.fleet

        if hasattr(instance, "register_tools") and hasattr(self.fleet, "registry"):
            try:
                instance.register_tools(self.fleet.registry)
                logging.debug(f"Registered tools for {key}")
            except Exception as e:
                logging.warning(f"Failed to register tools for {key}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, other: dict[str, Any]) -> None:
        # Allow manual overrides or additions (like SignalBus)
        self._instances.update(other)


class AgentRegistry:
    """Registry for mapping agent names to their implementations via lazy loading."""

    @staticmethod
    def get_agent_map(workspace_root: Path, fleet_instance: FleetManager | None = None) -> LazyAgentMap:
        """
        Returns the initial map of agents.
        Most agents are now dynamically discovered via AgentRegistryCore.scan_directory_for_agents().
        Only bootstrap-critical agents in BootstrapConfigs.py remain relatively static.
        """
        return LazyAgentMap(workspace_root, BOOTSTRAP_AGENTS, fleet_instance)
