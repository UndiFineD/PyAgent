#!/usr/bin/env python3

import importlib
import logging
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from .ResilientStubs import ResilientStub
from .OrchestratorRegistryCore import OrchestratorRegistryCore
from .BootstrapConfigs import BOOTSTRAP_ORCHESTRATORS

# Import local version for gatekeeping
try:
    from src.version import SDK_VERSION
except ImportError:
    SDK_VERSION = "1.0.0"

class LazyOrchestratorMap:
    """A dictionary-like object that instantiates orchestrators only when accessed."""
    def __init__(self, fleet_instance) -> None:
        self.fleet = fleet_instance
        self.workspace_root = Path(fleet_instance.workspace_root)
        self._instances = {}
        self.core = OrchestratorRegistryCore(SDK_VERSION)
        
        # 1. Manifest
        self._manifest_configs = self._load_manifests()
        
        # 2. Dynamic Discovery
        self._discovered_configs = self.core.scan_for_orchestrators(str(self.workspace_root))
        logging.info(f"Registry: Discovered {len(self._discovered_configs)} orchestrators.")

        # Combined map: Bootstrap > Manifest > Discovery
        # Convert BOOTSTRAP_ORCHESTRATORS to the 4-tuple format (module, class, needs_fleet, arg)
        boot_configs = {k: (v[0], v[1], True, None) for k, v in BOOTSTRAP_ORCHESTRATORS.items()}
        self._configs = {**self._discovered_configs, **self._manifest_configs, **boot_configs}

    def _load_manifests(self) -> Dict[str, tuple]:
        """Loads orchestrator configurations from plugin manifests."""
        manifest_configs = {}
        manifest_paths = [
            self.workspace_root / "plugins" / "orchestrator_manifest.json",
            self.workspace_root / "plugins" / "manifest.json"
        ]
        for m_path in manifest_paths:
            if m_path.exists():
                try:
                    with open(m_path, 'r') as f:
                        data = json.load(f)
                        configs = self.core.parse_manifest(data)
                        manifest_configs.update(configs)
                except Exception as e:
                    logging.error(f"Failed to load orchestrator manifest {m_path}: {e}")
        return manifest_configs

    def __getattr__(self, name):
        if name in self._instances:
            return self._instances[name]
        
        if name in self._configs:
            return self._instantiate(name, self._configs[name])
            
        # Case-insensitive fallback
        n_low = name.lower()
        for k, cfg in self._configs.items():
            if k.lower() == n_low:
                return self._instantiate(name, cfg)

        raise AttributeError(f"Orchestrator '{name}' not found.")

    def _instantiate(self, key, config):
        module_path, class_name, needs_fleet, arg_path_suffix = config
        try:
            import importlib
            module = importlib.import_module(module_path)
            
            # Version Gatekeeping
            min_sdk = getattr(module, "SDK_REQUIRED", getattr(module, "__min_sdk__", "1.0.0"))
            if not self.core.is_compatible(min_sdk):
                error_msg = f"Orchestrator '{key}' requires SDK {min_sdk}, but current is {SDK_VERSION}."
                logging.warning(error_msg)
                stub = ResilientStub(key, error_msg)
                self._instances[key] = stub
                return stub

            orchestrator_class = getattr(module, class_name)
            
            # Complex Instantiation Logic
            if needs_fleet:
                try:
                   instance = orchestrator_class(fleet=self.fleet)
                except TypeError:
                   try:
                       instance = orchestrator_class(self.fleet)
                   except TypeError:
                       try:
                           instance = orchestrator_class(fleet_manager=self.fleet)
                       except TypeError:
                           instance = orchestrator_class()
            elif arg_path_suffix is not None:
                base_path = self.workspace_root / arg_path_suffix
                instance = orchestrator_class(str(base_path)) if base_path.exists() else orchestrator_class(arg_path_suffix)
            else:
                instance = orchestrator_class()
                
            self._instances[key] = instance
            return instance
        except (ImportError, SyntaxError) as e:
            logging.error(f"Critical load error for orchestrator {key} from {module_path}: {e}")
            stub = ResilientStub(key, str(e))
            self._instances[key] = stub
            return stub
        except Exception as e:
            logging.error(f"Failed to lazy-load orchestrator {key} from {module_path}: {e}")
            return None

    def keys(self):
        """Returns list of available orchestrators."""
        return list(self._configs.keys())

    def __contains__(self, key):
        return key in self._configs

class OrchestratorRegistry:
    @staticmethod
    def get_orchestrator_map(fleet_instance):
        return LazyOrchestratorMap(fleet_instance)
