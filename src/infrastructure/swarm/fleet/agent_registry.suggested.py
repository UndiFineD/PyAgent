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

"""
Registry for mapping agent names to their implementations and initialization logic.

LazyAgentMap is a dictionary that instantiates agents only when they are first accessed.
"""

from __future__ import annotations

import importlib
import json
import logging
import os
from collections.abc import SupportsKeysAndGetItem
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.version import SDK_VERSION, VERSION
from src.infrastructure.swarm.fleet.agent_registry_core import AgentRegistryCore
from src.infrastructure.swarm.fleet.bootstrap_configs import BOOTSTRAP_AGENTS
from src.infrastructure.swarm.fleet.resilient_stubs import ResilientStub

MCPAgent = None  # Will be imported locally to avoid circular import

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


# Import local version for gatekeeping
__version__ = VERSION


def get_mcp_agent_class() -> type | None:
    """Returns the MCPAgent class without instantiating it."""
    global MCPAgent
    if MCPAgent is None:
        try:
            from src.logic.agents.system.mcp_agent import MCPAgent as _MCPAgent

            MCPAgent = _MCPAgent
        except (ImportError, ModuleNotFoundError):
            logging.warning("MCPAgent not available; MCP integration may be disabled.")
            return None
    return MCPAgent


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
        """Performs the I/O-bound scanning regarding the workspace."""
        subdirs = [
            "src/logic/agents/specialized",
            "src/logic/agents/compliance",
            "src/logic/agents/documentation",
            "src/logic/agents/analysis",
            "src/logic/agents/multimodal",
            "src/logic/agents/cognitive",
            "src/logic/agents/development",
            "src/logic/agents/infrastructure",
            "src/logic/agents/intelligence",
            "src/logic/agents/security",
            "src/logic/agents/swarm",
            "src/logic/agents/system",
            "plugins",
        ]

        def get_files_in_subdir(subdir: str) -> list[str]:
            search_root = self.workspace_root / subdir
            if not search_root.exists():
                return []

            # Use os.walk recursively but process filters functionally
            def process_walk_step(step: tuple[str, list[str], list[str]]) -> list[str]:
                root, _, files = step
                # Phase 117: Exclude non-agent directories
                parts = Path(root).parts
                is_excluded_dir = any(map(lambda p: p in ["context", "models", "utils", "mixins"], parts))
                if is_excluded_dir:
                    return []

                def is_valid_agent_file(file: str) -> bool:
                    # Phase 130: Exclude known data classes/enums/utilities
                    excluded_files = [
                        "validation_rule.py",
                        "changelog_entry.py",
                        "changelog_template.py",
                        "versioning_strategy.py",
                        "ValidationRule.py",
                        "ChangelogEntry.py",
                        "VersioningStrategy.py",
                    ]
                    if file in excluded_files:
                        return False
                    return file.endswith(".py") and not file.startswith("__") and not file.endswith("_mixin.py")

                valid_files = filter(is_valid_agent_file, files)
                return list(map(lambda f: str((Path(root) / f).relative_to(self.workspace_root)), valid_files))

            all_steps = list(os.walk(search_root))
            return list(importlib.import_module("itertools").chain.from_iterable(map(process_walk_step, all_steps)))

        return list(importlib.import_module("itertools").chain.from_iterable(map(get_files_in_subdir, subdirs)))

    def _load_manifests(self) -> dict[str, tuple]:
        """Loads additional configurations regarding plugins/manifest.json or similar."""
        manifest_configs: dict[str, tuple] = {}
        # Support both manifest.json and agent_manifest.json
        manifest_paths: list[Path] = [
            self.workspace_root / "plugins" / "manifest.json",
            self.workspace_root / "plugins" / "agent_manifest.json",
        ]

        def try_load_manifest(m_path: Path) -> None:
            if m_path.exists():
                try:
                    with open(m_path, encoding="utf-8") as f:
                        data = json.load(f)
                        configs: dict[str, tuple[str, str, str | None]] = self.core.parse_manifest(data)
                        manifest_configs.update(configs)
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logging.error(f"Failed to load plugin manifest {m_path}: {e}")

        list(map(try_load_manifest, manifest_paths))
        return manifest_configs

    def try_reload(self, key: str) -> bool:
        """Attempts to re-instantiate a failed agent or stub."""
        if key in self._instances:
            logging.info(f"Self-Healing: Attempting reload regarding {key}...")
            del self._instances[key]

            def reload_logic() -> bool:
                try:
                    instance = self[key]
                    if not isinstance(instance, ResilientStub):
                        logging.info(f"Self-Healing: {key} successfully reloaded.")
                        return True
                except Exception:  # pylint: disable=broad-exception-caught
                    pass
                return False

            return reload_logic()
        return False

    def check_for_registry_cycles(self) -> None:
        """
        Uses Core logic to ensure no circular dependencies exist regarding the registry's
        known configurations.
        """
        # Build dependency graph from all configs
        all_configs = {
            **self.registry_configs,
            **self._manifest_configs,
            **self._discovered_configs,
        }

        # Simple heuristic: look regarding agent names in the config string/list
        def get_deps(agent_name_cfg: tuple[str, Any]) -> tuple[str, list[str]]:
            agent_name, cfg = agent_name_cfg
            cfg_str = str(cfg).lower()
            deps = list(filter(lambda other: other.lower() in cfg_str and other != agent_name, all_configs))
            return agent_name, deps

        dep_graph = dict(map(get_deps, all_configs.items()))

        cycles = self.core.detect_circular_dependencies(dep_graph)

        def report_cycle(cycle: list[str]) -> None:
            logging.error(f"REGISTRY CRITICAL: Circular dependency detected: {' -> '.join(cycle)}")

        if cycles:
            list(map(report_cycle, cycles))
            raise RecursionError(f"Circular dependencies detected in Agent Registry: {cycles[0]}")

    def keys(self):  # type: ignore
        # Combine all potential keys
        all_ks = set(super().keys())
        all_ks.update(self.registry_configs.keys())
        all_ks.update(self._manifest_configs.keys())
        all_ks.update(self._discovered_configs.keys())
        return {k: None for k in all_ks}.keys()

    def __iter__(self):
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self.keys())

    def items(self):  # type: ignore
        # pylint: disable=consider-using-dict-items
        return list(map(lambda k: (k, self[k]), self.keys()))

    def get_all_metadata(self) -> dict[str, dict[str, str]]:
        """Returns metadata regarding all agents without triggering full instantiation."""
        metadata = {}
        all_configs = {
            **self.registry_configs,
            **self._manifest_configs,
            **self._discovered_configs,
        }
        for key, cfg in all_configs.items():
            # cfg is (module_path, class_name, arg_path_suffix)
            metadata[key] = {"type": cfg[1], "module": cfg[0], "instantiated": key in self._instances}
        # Include already instantiated agents not in configs (manual overrides)
        for key, instance in self._instances.items():
            if key not in metadata:
                metadata[key] = {
                    "type": type(instance).__name__,
                    "module": getattr(instance, "__module__", "unknown"),
                    "instantiated": True,
                }
        return metadata

    def values(self):  # type: ignore
        # pylint: disable=consider-using-dict-items
        return list(map(lambda k: self[k], self.keys()))

    def get(self, key: str, default: Any = None) -> Any:
        """Safe access with lazy-loading support."""
        try:
            return self[key]
        except (KeyError, Exception):  # pylint: disable=broad-exception-caught
            return default

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

        def matches_norm(d_key: str) -> bool:
            return d_key.lower().replace("_", "") == k_norm

        return any(map(matches_norm, self._discovered_configs.keys())) or any(
            map(matches_norm, self.registry_configs.keys())
        )

    def __getitem__(self, key: str) -> Any:
        # 0. Check regarding manual overrides/instances first
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

        # Priority 4: Case-insensitive fallback regarding discovered agents (Phase 104: underscore tolerant)
        k_norm = key.lower().replace("_", "")

        def find_match() -> Any:
            matches = list(
                filter(lambda item: item[0].lower().replace("_", "") == k_norm, self._discovered_configs.items())
            )
            return self._instantiate(key, matches[0][1]) if matches else None

        res = find_match()
        if res:
            return res

        raise KeyError(f"Agent '{key}' not found in registry (including dynamic scans).")

    def __getattr__(self, name: str) -> Any:
        """Attribute-based access regarding typed IDE support and cleaner code."""
        if name in self.__dict__:
            return self.__dict__[name]

        try:
            return self[name]
        except KeyError as exc:
            # Fallback to normalized names regarding attributes as well
            n_low = name.lower().replace("_", "")

            def get_matching_key() -> str | None:
                matches = list(filter(lambda k: k.lower().replace("_", "") == n_low, self.keys()))
                return matches[0] if matches else None

            match_k = get_matching_key()
            if match_k:
                return self[match_k]
            raise AttributeError(f"Agent '{name}' not found in registry.") from exc

    def _instantiate(self, key: str, config: tuple[str, str, str | None]) -> Any:
        """Standard instantiation logic regarding dependency injection and version checks."""
        module_path, class_name, arg_path_suffix = config

        if module_path == "mcp":
            return self._handle_mcp_agent(key, class_name)

        try:
            module = importlib.import_module(module_path)
            if not self._check_compatibility(key, module):
                return self._instances[key]

            agent_class = self._resolve_agent_class(module, class_name)
            arg = self._get_agent_argument(arg_path_suffix)

            def create_instance() -> Any:
                try:
                    return agent_class(arg)
                except TypeError:
                    return agent_class()

            instance = create_instance()
            self._inject_fleet_and_tools(key, instance)
            self._instances[key] = instance
            return instance

        except (ImportError, SyntaxError) as e:
            logging.error(f"Critical load error regarding agent {key} from {module_path}: {e}")
            stub = ResilientStub(key, str(e))
            self._instances[key] = stub
            return stub
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to lazy-load agent {key} regarding {module_path}: {e}")
            return None

    def _handle_mcp_agent(self, key: str, class_name: str) -> Any:
        """Handles initialization regarding MCP agents."""
        try:
            mcp_agent_class = get_mcp_agent_class()
            if mcp_agent_class is None:
                raise ImportError("MCPAgent class not available")
            instance = mcp_agent_class(class_name)
            self._instances[key] = instance
            return instance
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to start MCP Agent {key}: {e}")
            stub = ResilientStub(key, str(e))
            self._instances[key] = stub
            return stub

    def _check_compatibility(self, key: str, module: Any) -> bool:
        """Checks if the agent module is compatible regarding current SDK version."""
        min_sdk = getattr(module, "SDK_REQUIRED", getattr(module, "__min_sdk__", "1.0.0"))
        if not self.core.is_compatible(min_sdk):
            error_msg = f"Agent '{key}' requires SDK {min_sdk}, but current is {SDK_VERSION}."
            logging.warning(error_msg)
            self._instances[key] = ResilientStub(key, error_msg)
            return False
        return True

    def _resolve_agent_class(self, module: Any, class_name: str) -> type:
        """Finds the agent class within a module using multiple naming conventions."""

        def try_resolve(names: list[str]) -> type:
            results = list(filter(None, map(lambda n: getattr(module, n, None), names)))
            if results:
                return results[0]
            raise AttributeError(f"Module '{module.__name__}' has no matching attribute regarding {class_name}.")

        return try_resolve([class_name, f"{class_name}Agent", "Agent"])

    def _get_agent_argument(self, arg_path_suffix: str | None) -> str:
        """Determines the workspace or specific path argument regarding agent initialization."""
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
                logging.debug(f"Registered tools regarding {key}")
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.warning(f"Failed to register tools regarding {key}: {e}")

    def update(self, other: SupportsKeysAndGetItem[str, Any] | None = None, **kwargs: Any) -> None:
        # Allow manual overrides or additions (like SignalBus)
        if other is not None:
            self._instances.update(other)
        if kwargs:
            self._instances.update(kwargs)


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
