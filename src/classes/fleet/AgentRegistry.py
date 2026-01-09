#!/usr/bin/env python3

"""Registry for mapping agent names to their implementations and initialization logic."""

import importlib
import logging
import os
import json
from typing import Dict, Any, Type, Optional, Callable
from pathlib import Path
from .ResilientStubs import ResilientStub
from src.classes.specialized.MCPAgent import MCPAgent
from .AgentRegistryCore import AgentRegistryCore
from .BootstrapConfigs import BOOTSTRAP_AGENTS

# Import local version for gatekeeping
try:
    from src.version import SDK_VERSION
except ImportError:
    SDK_VERSION = "1.0.0"

class LazyAgentMap(dict):
    """A dictionary that instantiates agents only when they are first accessed."""
    def __init__(self, workspace_root: Path, registry_configs: Dict[str, tuple] = None, fleet_instance=None) -> None:
        super().__init__()
        self.workspace_root = workspace_root
        self.registry_configs = registry_configs or BOOTSTRAP_AGENTS
        self.fleet = fleet_instance
        self._instances: Dict[str, Any] = {}
        # Refactored: Logic delegated to Core (Rust-ready)
        self.core = AgentRegistryCore(SDK_VERSION)
        
        # 1. Load Manifest (Plugins)
        self._manifest_configs = self._load_manifests()
        
        # 2. Dynamic Discovery (The most lazy/flexible)
        # Pre-scan ensures we know what's available without guessing inside __getitem__
        self._discovered_configs = self.core.scan_directory_for_agents(str(self.workspace_root))
        logging.info(f"Registry: Discovered {len(self._discovered_configs)} agents dynamically.")

    def _load_manifests(self) -> Dict[str, tuple]:
        """Loads additional configurations from plugins/manifest.json or similar."""
        manifest_configs = {}
        # Support both manifest.json and agent_manifest.json
        manifest_paths = [
            self.workspace_root / "plugins" / "manifest.json",
            self.workspace_root / "plugins" / "agent_manifest.json"
        ]
        for m_path in manifest_paths:
            if m_path.exists():
                try:
                    with open(m_path, 'r') as f:
                        data = json.load(f)
                        configs = self.core.parse_manifest(data)
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

    def __getitem__(self, key):
        if key in self._instances:
            return self._instances[key]
        
        # Priority 1: Hardcoded configs (Essential bootstrap functions)
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

    def _instantiate(self, key, config):
        """Standard instantiation logic with dependency injection and version checks."""
        module_path, class_name, arg_path_suffix = config
        
        # Special Logic for MCP Bridge
        if module_path == "mcp":
            try:
                instance = MCPAgent(class_name)
                self._instances[key] = instance
                return instance
            except Exception as e:
                logging.error(f"Failed to start MCP Agent {key}: {e}")
                stub = ResilientStub(key, str(e))
                self._instances[key] = stub
                return stub

        try:
            module = importlib.import_module(module_path)
            
            # Version Gatekeeping (Shell layer check using Core logic)
            min_sdk = getattr(module, "SDK_REQUIRED", getattr(module, "__min_sdk__", "1.0.0"))
            if not self.core.is_compatible(min_sdk):
                error_msg = f"Agent '{key}' requires SDK {min_sdk}, but current is {SDK_VERSION}."
                logging.warning(error_msg)
                stub = ResilientStub(key, error_msg)
                self._instances[key] = stub
                return stub

            agent_class = getattr(module, class_name)
            
            # Phase 105: Default to workspace root if no specific arg provided (BaseAgent compatibility)
            arg = None
            if arg_path_suffix:
                potential_p = self.workspace_root / arg_path_suffix
                arg = str(potential_p) if potential_p.exists() else arg_path_suffix
            else:
                arg = str(self.workspace_root)
            
            # Attempt instantiation with arg, fallback to no-arg if it fails (not all are BaseAgents)
            try:
                instance = agent_class(arg)
            except TypeError:
                instance = agent_class()
            
            # Fleet Injection and Tool Registration
            if self.fleet:
                if hasattr(instance, 'fleet') and getattr(instance, 'fleet', None) is None:
                    instance.fleet = self.fleet
                
                # Check for tool registration capability
                if hasattr(instance, 'register_tools') and hasattr(self.fleet, 'registry'):
                    try:
                        instance.register_tools(self.fleet.registry)
                        logging.debug(f"Registered tools for {key}")
                    except Exception as e:
                        logging.warning(f"Failed to register tools for {key}: {e}")

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

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
            
            # Version Gatekeeping
            min_sdk = getattr(module, "SDK_REQUIRED", getattr(module, "__min_sdk__", "1.0.0"))
            if hasattr(self.core, 'is_compatible') and not self.core.is_compatible(min_sdk):
                error_msg = f"Agent '{key}' requires SDK {min_sdk}, but current is {SDK_VERSION}."
                logging.warning(error_msg)
                stub = ResilientStub(key, error_msg)
                self._instances[key] = stub
                return stub

            agent_class = getattr(module, class_name)
            
            # Construct the argument path if provided
            arg = None
            if arg_path_suffix:
                if (self.workspace_root / arg_path_suffix).exists():
                    arg = str(self.workspace_root / arg_path_suffix)
                else:
                    # Might be an absolute path or relative to python path
                    arg = arg_path_suffix
            
            instance = agent_class(arg) if arg else agent_class()
            
            # Inject fleet reference and register tools if possible
            if self.fleet:
                if hasattr(instance, 'fleet') and instance.fleet is None:
                    instance.fleet = self.fleet
                
                if hasattr(instance, 'register_tools') and self.fleet.registry:
                    try:
                        instance.register_tools(self.fleet.registry)
                        logging.debug(f"Registered tools for {key}")
                    except Exception as e:
                        logging.warning(f"Failed to register tools for {key}: {e}")

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

    def update(self, other):
        # Allow manual overrides or additions (like SignalBus)
        self._instances.update(other)

    def __contains__(self, key):
        return (key in self._instances or 
                key in self.registry_configs or 
                key in self._manifest_configs or 
                key in self._discovered_configs)

class AgentRegistry:
    """Registry for mapping agent names to their implementations via lazy loading."""
    
    @staticmethod
    def get_agent_map(workspace_root: Path, fleet_instance=None) -> LazyAgentMap:
        """
        Returns the initial map of agents.
        Most agents are now dynamically discovered via AgentRegistryCore.scan_directory_for_agents().
        Only bootstrap-critical agents in BootstrapConfigs.py remain relatively static.
        """
        return LazyAgentMap(workspace_root, BOOTSTRAP_AGENTS, fleet_instance)
