#!/usr/bin/env python3

"""Manager for loading 3rd party agent extensions dynamically.
Scans the 'plugins' directory for agent implementations.
"""

import os
import json
import logging
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
from .VersionGate import VersionGate

# Import local version for gatekeeping
try:
    from src.version import SDK_VERSION
except ImportError:
    SDK_VERSION = "1.0.0"

class PluginManager:
    """
    Modernized PluginManager.
    Handles discovery, version gatekeeping, and lazy loading for community extensions.
    """
    
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.plugins_dir = workspace_root / "plugins"
        self.registry_path = self.plugins_dir / "manifest.json"
        self.loaded_meta: Dict[str, Any] = {}
        
        if not self.plugins_dir.exists():
            self.plugins_dir.mkdir(parents=True)

    def discover(self) -> List[str]:
        """Scans manifest and directory for available plugins with lazy loading."""
        discovered = []
        
        # 1. Manifest (Priority)
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = json.load(f)
                    for key, meta in data.items():
                        # Use version gate logic
                        min_sdk = meta[3] if isinstance(meta, list) and len(meta) > 3 else "1.0.0"
                        if self.validate_version(min_sdk):
                            self.loaded_meta[key] = meta
                            discovered.append(key)
                        else:
                            logging.warning(f"PluginManager: Ignoring '{key}' (Incompatible SDK {min_sdk})")
            except Exception as e:
                logging.error(f"PluginManager: Manifest error: {e}")
        
        # 2. Dynamic Directory Scan (Flexible Fallback)
        if self.plugins_dir.exists():
            for item in self.plugins_dir.iterdir():
                if item.name == "manifest.json" or item.stem in discovered or item.name.startswith("__"):
                    continue
                
                # Check for .py files
                if item.is_file() and item.suffix == ".py":
                    plugin_name = item.stem
                    discovered.append(plugin_name)
                    # Heuristic meta: [module_path, class_name, needs_fleet, min_sdk]
                    self.loaded_meta[plugin_name] = [
                        f"plugins.{plugin_name}", 
                        plugin_name, 
                        True, # Default to True for plugins to allow fleet injection
                        "1.0.0"
                    ]
                    logging.debug(f"PluginManager: Dynamically discovered '{plugin_name}'")

                elif item.is_dir() and (item / "__init__.py").exists():
                    plugin_name = item.name
                    discovered.append(plugin_name)
                    self.loaded_meta[plugin_name] = [
                        f"plugins.{plugin_name}",
                        plugin_name,
                        True,
                        "1.0.0"
                    ]
                    logging.debug(f"PluginManager: Dynamically discovered package '{plugin_name}'")
                
        return discovered

    def validate_version(self, required_version: str) -> bool:
        """Centralized semantic version gatekeeper."""
        return VersionGate.is_compatible(SDK_VERSION, required_version)

    def load_resource(self, plugin_name: str) -> Optional[Any]:
        """Dynamically loads the resource (Agent class, Core, etc) from the plugin."""
        if plugin_name not in self.loaded_meta:
            return None
        
        meta = self.loaded_meta[plugin_name]
        # Heuristic: [module_path, class_name, needs_fleet, min_sdk]
        module_path, class_name, needs_fleet, min_sdk = meta if len(meta) >= 4 else (meta[0], meta[1], False, "1.0.0")

        try:
            module = importlib.import_module(module_path)
            resource_class = getattr(module, class_name)
            
            # Simple instantiation
            if needs_fleet:
                return resource_class # Return class itself, caller (FleetManager) will instantiate
            return resource_class()
        except Exception as e:
            logging.error(f"PluginManager: Failed to load '{plugin_name}': {e}")
            return None
