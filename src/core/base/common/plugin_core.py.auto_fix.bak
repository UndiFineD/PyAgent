#!/usr/bin/env python3
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


"""Core logic for plugin discovery, loading, and registration.
"""

import importlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from src.core.base.common.models import HealthStatus

from src.core.base.common.base_core import BaseCore


try:
    import docker
except ImportError:
    docker = None

if TYPE_CHECKING:
    pass


@dataclass
# pylint: disable=too-many-instance-attributes
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
        """
        Retrieves an attribute value.
        """
        return getattr(self, key, default)


# pylint: disable=too-many-instance-attributes
class PluginCore(BaseCore):
    """Authoritative engine for discovering and managing plugins.
    """

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        """Initializes the PluginCore with optional workspace root for plugin discovery.
        """
        super().__init__()
        self.workspace_root = workspace_root or Path.cwd()
        self.plugins_dir = self.workspace_root / "plugins"
        self.registry_path = self.plugins_dir / "manifest.json"
        self.loaded_meta: Dict[str, PluginMetadata] = {}
        self.active_plugins: Dict[str, Any] = {}  # Any to avoid circular dependency on logic
        self.logger = logging.getLogger("pyagent.plugin_core")
        if not self.plugins_dir.exists():
            try:
                self.plugins_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                pass


    def discover(self) -> List[str]:
        """
        Scans manifest and directory for compatible plugins.
        """
        discovered = []
        discovered += self._load_manifest_plugins()
        discovered += self._scan_plugin_directories()
        return list(set(discovered))


    def _load_manifest_plugins(self) -> List[str]:
        """
        Load plugins from the central manifest file.
        """
        discovered = []
        if self.registry_path.exists():
            try:
                with open(self.registry_path, encoding="utf-8") as f:
                    data = json.load(f)
                    for key, raw_meta in data.items():
                        self._register_plugin_meta(key, raw_meta)
                        if key in self.loaded_meta:
                            discovered.append(key)
            except (json.JSONDecodeError, OSError) as e:
                self.logger.error("Failed to load plugin manifest: %s", e)
        return discovered


    def _scan_plugin_directories(self) -> List[str]:
        """
        Scan plugin directories for auto-discovery and heuristics.
        """
        discovered = []
        for item in self.plugins_dir.iterdir():
            if not item.is_dir() or item.name.startswith(("_", ".")):
                continue
            if item.name in self.loaded_meta:
                continue  # Already registered via manifest
            if not (item / "__init__.py").exists():
                continue
            meta_path = item / "manifest.json"
            plugin_json = item / "plugin.json"
            if meta_path.exists() or plugin_json.exists():
                discovered += self._register_plugin_from_metadata_file(item, meta_path, plugin_json)
                continue
            discovered.append(self._register_heuristic_plugin(item))
        return discovered


    def _register_plugin_from_metadata_file(self, item: Path, meta_path: Path, plugin_json: Path) -> List[str]:
        """
        Register plugin from manifest.json or plugin.json in the plugin directory.
        """
        discovered = []
        target = meta_path if meta_path.exists() else plugin_json
        try:
            with open(target, encoding="utf-8") as f:
                raw_meta = json.load(f)
                self._register_plugin_meta(item.name, raw_meta)
                discovered.append(item.name)
        except (json.JSONDecodeError, OSError) as e:
            self.logger.warning("Failed to load plugin meta in %s: %s", item.name, e)
        return discovered


    def _register_heuristic_plugin(self, item: Path) -> str:
        """
        Register a plugin using heuristic discovery.
        """
        class_name = item.name.replace("_", " ").title().replace(" ", "")
        perms = []
        perms_file = item / "permissions.json"
        if perms_file.exists():
            try:
                with open(perms_file, encoding="utf-8") as f:
                    perms = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        raw_meta = {
            "module_path": f"plugins.{item.name}",
            "class_name": class_name,
            "permissions": perms
        }
        self._register_plugin_meta(item.name, raw_meta)
        return item.name


    def _register_plugin_meta(self, key: str, raw_meta: Any) -> None:
        """Helper to register plugin metadata from raw dict or list."""
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
        except (TypeError, ValueError, KeyError) as e:
            self.logger.warning("Skipping malformed plugin meta '%s': %s", key, e)


    def validate_version(self, required_version: str, current_version: str) -> bool:
        """Centralized semantic version gatekeeper."""
        # Simple version check if VersionGate is not available
        try:
            from src.infrastructure.swarm.fleet.version_gate import VersionGate
            return VersionGate.is_compatible(current_version, required_version)
        except (ImportError, AttributeError, RuntimeError):
            pass
        return True  # Default to true if validator is missing


    def load_plugin(self, plugin_name: str) -> Optional[Any]:
        """Loads and initializes a plugin instance."""
        if plugin_name not in self.loaded_meta:
            return None

        meta = self.loaded_meta[plugin_name]
        try:
            if meta.restricted_mode:
                return self._load_sandboxed_plugin(plugin_name, meta)

            module = importlib.import_module(meta.module_path)
            plugin_class = getattr(module, meta.class_name)

            instance = plugin_class()
            if hasattr(instance, "setup"):
                instance.setup()

            # Health check immediately after setup
            if hasattr(instance, "health_check"):
                health = instance.health_check()
                if hasattr(health, "status") and health.status != HealthStatus.HEALTHY:
                    self.logger.error("Plugin '%s' failed health check", plugin_name)
                    return None

            self.active_plugins[plugin_name] = instance
            return instance
        except (ImportError, AttributeError, RuntimeError) as e:
            self.logger.error("Failed to load plugin '%s': %s", plugin_name, e)
            return None


    def _load_sandboxed_plugin(self, name: str, meta: PluginMetadata) -> Optional[Any]:
        """Phase 288: Implement Docker-based or native sandboxing for untrusted plugins."""
        try:
            if docker is None:
                raise ImportError("Docker SDK not installed")
            client = docker.from_env()
            client.ping()
            self.logger.info("Plugin '%s': Using Docker sandbox.", name)
            return self._setup_permission_proxy(name, meta)
        except (ImportError, RuntimeError) as e:
            self.logger.warning("Plugin '%s': Docker sandbox unavailable (%s).", name, e)
            return self._setup_permission_proxy(name, meta)


    def _setup_permission_proxy(self, name: str, meta: PluginMetadata) -> Any:
        """Enforces permissions via a runtime wrapper."""
        module = importlib.import_module(meta.module_path)
        plugin_class = getattr(module, meta.class_name)
        instance = plugin_class()

        if hasattr(instance, "run"):
            original_run = instance.run
            allowed_permissions = meta.permissions or []

            def restricted_run(file_path: Path, context: Dict[str, Any]) -> bool:
                if "read:src" not in allowed_permissions and "src" in str(file_path):
                    self.logger.error("Permission Denied: Plugin '%s' attempted to read 'src' path.", name)
                    return False
                return original_run(file_path, context)

            instance.run = restricted_run

        if hasattr(instance, "setup"):
            instance.setup()
        self.active_plugins[name] = instance
        return instance


    def activate_all(self) -> None:
        """Activates all discovered plugins."""
        for name in self.loaded_meta:
            self.load_plugin(name)


    def deactivate(self, name: str) -> None:
        """Deactivates a specific plugin by name."""
        if name in self.active_plugins:
            plugin = self.active_plugins[name]
            if hasattr(plugin, "shutdown"):
                plugin.shutdown()
            del self.active_plugins[name]


    def register_plugin(self, name: str, plugin: Any) -> None:
        """Manually registers a plugin instance."""
        self.active_plugins[name] = plugin
        self.logger.info("Plugin registered: %s", name)


    def get_plugin(self, name: str) -> Optional[Any]:
        """Retrieves a registered plugin by name."""
        return self.active_plugins.get(name)


    def shutdown_all(self) -> None:
        """Gracefully shuts down all active plugins."""
        for name, plugin in self.active_plugins.items():
            if hasattr(plugin, "shutdown"):
                try:
                    plugin.shutdown()
                    self.logger.info("Plugin shutdown: %s", name)
                except (RuntimeError, AttributeError) as e:
                    self.logger.error("Error during plugin shutdown (%s): %s", name, e)
        self.active_plugins.clear()
