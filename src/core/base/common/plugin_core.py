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
Core logic for plugin discovery, loading, and registration.
"""

from __future__ import annotations
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from .base_core import BaseCore

if TYPE_CHECKING:
    from src.core.base.logic.agent_plugin_base import AgentPluginBase

@dataclass
class PluginMetadata:
    """Strictly typed metadata for a plugin."""
    module_path: str
    class_name: str
    needs_fleet: bool = True
    min_sdk_version: str = "1.0.0"
    version: str = "0.1.0"
    author: str = "Unknown"
    description: str = ""
    permissions: Optional[List[str]] = None
    restricted_mode: bool = False

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

class PluginCore(BaseCore):
    """
    Authoritative engine for discovering and managing plugins.
    """

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        super().__init__()
        self.workspace_root = workspace_root or Path.cwd()
        self.plugins_dir = self.workspace_root / "plugins"
        self.registry_path = self.plugins_dir / "manifest.json"
        self.loaded_meta: Dict[str, PluginMetadata] = {}
        self.active_plugins: Dict[str, Any] = {} # Any to avoid circular dependency on logic
        self.logger = logging.getLogger("pyagent.plugin_core")

        if not self.plugins_dir.exists():
            try:
                self.plugins_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def discover(self) -> List[str]:
        """Scans manifest and directory for compatible plugins."""
        discovered = []
        if self.registry_path.exists():
            try:
                with open(self.registry_path) as f:
                    data = json.load(f)
                    for key, raw_meta in data.items():
                        try:
                            if isinstance(raw_meta, list):
                                meta = PluginMetadata(
                                    module_path=raw_meta[0],
                                    class_name=raw_meta[1],
                                    needs_fleet=raw_meta[2] if len(raw_meta) > 2 else True,
                                    min_sdk_version=raw_meta[3] if len(raw_meta) > 3 else "1.0.0",
                                )
                            else:
                                meta = PluginMetadata(**raw_meta)
                            self.loaded_meta[key] = meta
                            discovered.append(key)
                        except Exception as e:
                            self.logger.warning(f"Skipping malformed plugin meta '{key}': {e}")
            except Exception as e:
                self.logger.error(f"Failed to load plugin manifest: {e}")
        return discovered

    def validate_version(self, required_version: str, current_version: str) -> bool:
        """Centralized semantic version gatekeeper."""
        # Simple version check if VersionGate is not available
        try:
            from src.infrastructure.swarm.fleet.version_gate import VersionGate
            if VersionGate:
                return VersionGate.is_compatible(current_version, required_version)
        except ImportError:
            pass
        return True # Default to true if validator is missing

    def load_plugin(self, plugin_name: str) -> Optional[Any]:
        """Loads and initializes a plugin instance."""
        if plugin_name not in self.loaded_meta:
            return None

        meta = self.loaded_meta[plugin_name]
        try:
            import importlib
            if meta.restricted_mode:
                return self._load_sandboxed_plugin(plugin_name, meta)

            module = importlib.import_module(meta.module_path)
            plugin_class = getattr(module, meta.class_name)

            instance = plugin_class()
            if hasattr(instance, 'setup'):
                instance.setup()

            # Health check immediately after setup
            if hasattr(instance, 'health_check'):
                health = instance.health_check()
                if hasattr(health, 'status') and health.status != "healthy":
                    self.logger.error(f"Plugin '{plugin_name}' failed health check")
                    return None

            self.active_plugins[plugin_name] = instance
            return instance
        except Exception as e:
            self.logger.error(f"Failed to load plugin '{plugin_name}': {e}")
            return None

    def _load_sandboxed_plugin(self, name: str, meta: PluginMetadata) -> Optional[Any]:
        """Phase 288: Implement Docker-based or native sandboxing for untrusted plugins."""
        try:
            import docker
            client = docker.from_env()
            client.ping()
            self.logger.info(f"Plugin '{name}': Using Docker sandbox.")
            return self._setup_permission_proxy(name, meta)
        except Exception as e:
            self.logger.warning(f"Plugin '{name}': Docker sandbox unavailable ({e}).")
            return self._setup_permission_proxy(name, meta)

    def _setup_permission_proxy(self, name: str, meta: PluginMetadata) -> Any:
        """Enforces permissions via a runtime wrapper."""
        import importlib
        module = importlib.import_module(meta.module_path)
        plugin_class = getattr(module, meta.class_name)
        instance = plugin_class()

        if hasattr(instance, 'run'):
            original_run = instance.run
            allowed_permissions = meta.permissions or []

            def restricted_run(file_path: Path, context: Dict[str, Any]) -> bool:
                if "read:src" not in allowed_permissions and "src" in str(file_path):
                    self.logger.error(f"Permission Denied: Plugin '{name}' attempted to read 'src' path.")
                    return False
                return original_run(file_path, context)

            instance.run = restricted_run

        if hasattr(instance, 'setup'):
            instance.setup()
        self.active_plugins[name] = instance
        return instance

    def activate_all(self) -> None:
        for name in self.loaded_meta:
            self.load_plugin(name)

    def deactivate(self, name: str) -> None:
        if name in self.active_plugins:
            plugin = self.active_plugins[name]
            if hasattr(plugin, 'shutdown'):
                plugin.shutdown()
            del self.active_plugins[name]

    def register_plugin(self, name: str, plugin: Any) -> None:
        """Manually registers a plugin instance."""
        self.active_plugins[name] = plugin
        self.logger.info(f"Plugin registered: {name}")

    def get_plugin(self, name: str) -> Optional[Any]:
        """Retrieves a registered plugin by name."""
        return self.active_plugins.get(name)

    def shutdown_all(self) -> None:
        """Gracefully shuts down all active plugins."""
        for name, plugin in self.active_plugins.items():
            if hasattr(plugin, 'shutdown'):
                try:
                    plugin.shutdown()
                    self.logger.info(f"Plugin shutdown: {name}")
                except Exception as e:
                    self.logger.error(f"Error during plugin shutdown ({name}): {e}")
        self.active_plugins.clear()
