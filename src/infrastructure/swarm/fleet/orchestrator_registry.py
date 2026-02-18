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


"""
LazyOrchestratorMap
- A lazy-loading registry that maps orchestrator names to their instances.
Orchestrator registry.py module.
"""
# Import local version for gatekeeping

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.version import SDK_VERSION, VERSION

from src.infrastructure.swarm.fleet.bootstrap_configs import BOOTSTRAP_ORCHESTRATORS
from src.infrastructure.swarm.fleet.orchestrator_registry_core import OrchestratorRegistryCore
from src.infrastructure.swarm.fleet.resilient_stubs import ResilientStub

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

__version__ = VERSION



class LazyOrchestratorMap:
    """A dictionary-like object that instantiates orchestrators only when accessed."""

    def __init__(self, fleet_instance: FleetManager) -> None:
        """Initializes the lazy orchestrator map 
        with a reference to the fleet 
        and loads configurations from manifests and discovery.
        """
        self.fleet = fleet_instance
        self.workspace_root = Path(fleet_instance.workspace_root)
        self._instances: dict[Any, Any] = {}
        self._registry_core = OrchestratorRegistryCore(SDK_VERSION)

        # 1. Manifest
        self._manifest_configs = self._load_manifests()

        # 2. Dynamic Discovery
        discovered_files = self._scan_workspace_for_orchestrators()
        self._discovered_configs = self._registry_core.process_discovered_files(discovered_files)
        logging.info(f"Registry: Discovered {len(self._discovered_configs)} orchestrators.")
        # Combined map: Bootstrap > Manifest > Discovery
        # Convert BOOTSTRAP_ORCHESTRATORS to the 4-tuple format (module, class, needs_fleet, arg)
        boot_configs = {k: (v[0], v[1], True, None) for k, v in BOOTSTRAP_ORCHESTRATORS.items()}
        self._configs = {
            **self._discovered_configs,
            **self._manifest_configs,
            **boot_configs,
        }


    def _scan_workspace_for_orchestrators(self) -> list[str]:
        """Performs the I/O-bound scanning of the workspace."""
        subdirs = [
            "src/infrastructure/swarm/orchestration",
            "src/infrastructure/orchestration",
            "src/logic/agents/cognitive",
            "src/infrastructure/fleet",
            "src/logic/agents/swarm",
            "src/logic/agents/security",
            "src/logic/agents/management",]
        found_paths = []
        for subdir in subdirs:
            search_root = self.workspace_root / subdir
            if not search_root.exists():
                continue
            # Phase 116: Performance Optimization
            for root, _, files in os.walk(search_root):
                for file in files:
                    if "orchestrator" in file.lower():
                        full_path = Path(root) / file
                        rel_path = full_path.relative_to(self.workspace_root)
                        found_paths.append(str(rel_path))
        return found_paths


    def _load_manifests(self) -> dict[str, tuple]:
        """Loads orchestrator configurations from plugin manifests."""
        manifest_configs = {}
        manifest_paths = [
            self.workspace_root / "plugins" / "orchestrator_manifest.json",
            self.workspace_root / "plugins" / "manifest.json",
        ]
        for m_path in manifest_paths:
            if m_path.exists():
                try:
                    with open(m_path, encoding='utf-8') as f:
                        data = json.load(f)
                        configs = self._registry_core.parse_manifest(data)
                        manifest_configs.update(configs)
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logging.error(f"Failed to load orchestrator manifest {m_path}: {e}")
        return manifest_configs


    def __getattr__(self, name: str) -> Any:
        if name in self.__dict__:
            return self.__dict__[name]

        if name in self._instances:
            return self._instances[name]

        if name in self._configs:
            return self._instantiate(name, self._configs[name])

        # Case-insensitive and underscore-tolerant fallback
        n_low = name.lower().replace("_", "")
        for k, cfg in self._configs.items():
            if k.lower().replace("_", "") == n_low:
                return self._instantiate(name, cfg)

        raise AttributeError(f"Orchestrator '{name}' not found.")


    def try_reload(self, name: str) -> bool:
        """Attempts to reload/re-instantiate a specific orchestrator."""
        if name in self._instances:
            del self._instances[name]

        try:
            instance = getattr(self, name)
            # Check if it's still a stub'            return not isinstance(instance, ResilientStub)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to reload orchestrator '{name}': {e}")
            return False

    def _instantiate(self, key: str, config: tuple[str, str, bool, str | None]) -> Any:
        module_path, class_name, needs_fleet, arg_path_suffix = config
        try:
            import importlib

            module = importlib.import_module(module_path)

            # Version Gatekeeping
            min_sdk = getattr(module, "SDK_REQUIRED", getattr(module, "__min_sdk__", "1.0.0"))
            if not self._registry_core.is_compatible(min_sdk):
                error_msg = f"Orchestrator '{key}' requires SDK {min_sdk}, but current is {SDK_VERSION}."
                logging.warning(error_msg)
                stub = ResilientStub(key, error_msg)
                self._instances[key] = stub
                return stub

            orchestrator_class = getattr(module, class_name)

            # Phase 125: Enhanced Instantiation with Agent Compatibility
            # Some orchestrators (e.g. WeightOrchestrator) inherit from BaseAgent
            # and require a workspace_root string as the first argument.
            instance = None
            try:
                from src.core.base.lifecycle.base_agent import BaseAgent

                is_agent = issubclass(orchestrator_class, BaseAgent)
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                is_agent = False

            if is_agent:
                path_arg = str(self.workspace_root)
                if arg_path_suffix:
                    path_arg = str(self.workspace_root / arg_path_suffix)
                try:
                    instance = orchestrator_class(path_arg)
                    if hasattr(instance, "fleet"):
                        instance.fleet = self.fleet
                except TypeError:
                    instance = None  # Fallback to standard logic

            if instance is None:
                if needs_fleet:
                    try:
                        instance = orchestrator_class(fleet=self.fleet)
                    except TypeError:
                        try:
                            instance = orchestrator_class(self.fleet)
                        except TypeError:
                            try:
                                # Fallback for Engines/Managers that expect workspace_root string
                                instance = orchestrator_class(str(self.workspace_root))
                                if hasattr(instance, "fleet"):
                                    instance.fleet = self.fleet
                            except TypeError:
                                try:
                                    instance = orchestrator_class(fleet_manager=self.fleet)
                                except TypeError:
                                    instance = orchestrator_class()
                elif arg_path_suffix is not None:
                    base_path = self.workspace_root / arg_path_suffix
                    instance = (
                        orchestrator_class(str(base_path))
                        if base_path.exists()
                        else orchestrator_class(arg_path_suffix)
                    )
                else:
                    instance = orchestrator_class()

            self._instances[key] = instance
            return instance
        except (ImportError, SyntaxError) as e:
            logging.error(f"Critical load error for orchestrator {key} from {module_path}: {e}")
            stub = ResilientStub(key, str(e))
            self._instances[key] = stub
            return stub
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to lazy-load orchestrator {key} from {module_path}: {e}")
            return None

    def keys(self) -> list[str]:
        """Returns list of available orchestrators."""
        return list(self._configs.keys())

    def __contains__(self, key: object) -> bool:
        """Checks if a given key is in the orchestrator registry."""
        return key in self._configs


class OrchestratorRegistry:
    """Registry for mapping agent types to their corresponding orchestrators."""

    @staticmethod
    def get_orchestrator_map(fleet_instance: FleetManager) -> LazyOrchestratorMap:
        """Factory method to create a new live orchestrator map for a fleet."""
        return LazyOrchestratorMap(fleet_instance)
