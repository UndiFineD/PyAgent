#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

from __future__ import annotations
import hashlib
import json
import logging
import os
import sys
import time
import subprocess
import importlib.util
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from src.core.base.models import (
    FilePriority, FilePriorityConfig, AgentEvent, ConfigProfile, HealthStatus,
    AgentHealthCheck, ExecutionProfile,
    _empty_dict_str_str, _empty_agent_event_handlers, _empty_dict_str_health_checks,
    _empty_dict_str_any, _empty_dict_str_configprofile
)
from src.core.base.version import SDK_VERSION

# Optional import for PluginManager
try:
    from src.infrastructure.fleet.VersionGate import VersionGate
except ImportError:
    VersionGate = None

# Phase 108: Multi-Agent Logic Harvesting. 
# Intelligence operations are recorded via record_interaction in Agent classes.

class FilePriorityManager:
    """Manager for file priority and request ordering."""
    def __init__(self, config: Optional[FilePriorityConfig] = None) -> None:
        self.config = config or FilePriorityConfig()
        self._default_extensions = {
            ".py": FilePriority.HIGH, ".js": FilePriority.HIGH, ".ts": FilePriority.HIGH,
            ".md": FilePriority.NORMAL, ".json": FilePriority.LOW, ".txt": FilePriority.LOW,
        }
    def set_pattern_priority(self, pattern: str, priority: FilePriority) -> None:
        self.config.path_patterns[pattern] = priority
    def set_extension_priority(self, extension: str, priority: FilePriority) -> None:
        self.config.extension_priorities[extension] = priority
    def get_priority(self, path: Path) -> FilePriority:
        import fnmatch
        path_str = str(path)
        for pattern, priority in self.config.path_patterns.items():
            if fnmatch.fnmatch(path_str, pattern): return priority
        ext = path.suffix.lower()
        if ext in self.config.extension_priorities: return self.config.extension_priorities[ext]
        if ext in self._default_extensions: return self._default_extensions[ext]
        return self.config.default_priority
    def sort_by_priority(self, paths: List[Path]) -> List[Path]:
        return sorted(paths, key=lambda p: self.get_priority(p).value, reverse=True)
    def filter_by_priority(self, paths: List[Path], min_priority: FilePriority = FilePriority.LOW) -> List[Path]:
        return [p for p in paths if self.get_priority(p).value >= min_priority.value]

@dataclass
class ResponseCache:
    """
    Caches responses based on prompts. 
    Supports Prompt Caching (Phase 128) by identifying prefix reusable contexts.
    """
    cache_dir: Path
    cache_data: Dict[str, str] = field(default_factory=_empty_dict_str_str)
    prefix_map: Dict[str, str] = field(default_factory=_empty_dict_str_str)

    def __post_init__(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode()).hexdigest()

    def set(self, prompt: str, response: str) -> None:
        key = self._get_cache_key(prompt)
        self.cache_data[key] = response
        
        # Support prefix caching: Index the first 500 chars (approx. context window prefix)
        if len(prompt) > 500:
            prefix_key = hashlib.md5(prompt[:500].encode()).hexdigest()
            self.prefix_map[prefix_key] = key

        (self.cache_dir / f"{key}.json").write_text(json.dumps({
            "prompt": prompt, 
            "response": response,
            "timestamp": "2026-01-11"
        }))

    def get(self, prompt: str) -> Optional[str]:
        key = self._get_cache_key(prompt)
        if key in self.cache_data: return self.cache_data[key]
        
        # Check prefix map for partial hits (simulation of provider-side prompt caching)
        if len(prompt) > 500:
            prefix_key = hashlib.md5(prompt[:500].encode()).hexdigest()
            if prefix_key in self.prefix_map:
                logging.info("ResponseCache: Prompt Prefix hit - internal cache redirection triggered.")
                # We still want the full key for safety, but this flags reuse potential
        
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            data = json.loads(cache_file.read_text())
            self.cache_data[key] = data["response"]
            return data["response"]
        return None
    def invalidate(self, prompt: str) -> None:
        key = self._get_cache_key(prompt)
        self.cache_data.pop(key, None)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists(): cache_file.unlink()

@dataclass
class StatePersistence:
    """Persists agent state to disk."""
    state_file: Path
    backup: bool = False
    backup_count: int = 0
    def save(self, state: Dict[str, Any]) -> None:
        if self.backup and self.state_file.exists():
            self.state_file.rename(self.state_file.parent / f"{self.state_file.stem}.{self.backup_count}.bak")
            self.backup_count += 1
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(state))
    def load(self, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self.state_file.exists(): return json.loads(self.state_file.read_text())
        return default or {}

@dataclass
class EventManager:
    """Manages agent events."""
    handlers: Dict[AgentEvent, List[Callable[..., None]]] = field(default_factory=_empty_agent_event_handlers)
    def on(self, event: AgentEvent, handler: Callable[..., None]) -> None:
        if event not in self.handlers: self.handlers[event] = []
        self.handlers[event].append(handler)
    def emit(self, event: AgentEvent, data: Any = None) -> None:
        if event in self.handlers:
            for handler in self.handlers[event]:
                if data is not None: handler(data)
                else: handler()

class PluginManager:
    """
    Modernized PluginManager.
    Handles discovery, version gatekeeping, and lazy loading for community extensions.
    """
    
    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()
        self.plugins_dir = self.workspace_root / "plugins"
        self.registry_path = self.plugins_dir / "manifest.json"
        self.loaded_meta: Dict[str, Any] = {}
        self.plugins: Dict[str, Any] = {} # Stub compatibility
        
        if not self.plugins_dir.exists():
            try:
                self.plugins_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def register(self, plugin: Any) -> None:
        """Stub compatibility."""
        self.plugins[getattr(plugin, 'name', 'unknown')] = plugin

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
                        True, 
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
        if not VersionGate:
            return True # Fallback if VersionGate isn't available
        return VersionGate.is_compatible(SDK_VERSION, required_version)

    def load_resource(self, plugin_name: str) -> Optional[Any]:
        """Dynamically loads the resource (Agent class, Core, etc) from the plugin."""
        if plugin_name not in self.loaded_meta:
            return None
        
        meta = self.loaded_meta[plugin_name]
        module_path, class_name, needs_fleet, min_sdk = meta if len(meta) >= 4 else (meta[0], meta[1], False, "1.0.0")

        try:
            module = importlib.import_module(module_path)
            resource_class = getattr(module, class_name)
            
            if needs_fleet:
                return resource_class
            return resource_class()
        except Exception as e:
            logging.error(f"PluginManager: Failed to load '{plugin_name}': {e}")
            return None

    def activate_all(self) -> None:
        """Stub compatibility."""
        for plugin in self.plugins.values():
            if hasattr(plugin, 'activate'): plugin.activate()

    def deactivate(self, name: str) -> None:
        """Stub compatibility."""
        if name in self.plugins:
            plugin = self.plugins[name]
            if hasattr(plugin, 'deactivate'): plugin.deactivate()

class HealthChecker:
    """Performs health checks on agent components."""

    def __init__(self, repo_root: Optional[Path] = None, recorder: Any = None) -> None:
        self.repo_root = repo_root or Path.cwd()
        self.recorder = recorder
        self.results: Dict[str, AgentHealthCheck] = {}
        # Stub compatibility
        self.checks: Dict[str, Callable[[], Dict[str, Any]]] = {}
        self.request_count: int = 0
        self.error_count: int = 0
        self.total_latency: int = 0

    def add_check(self, name: str, check_func: Callable[[], Dict[str, Any]]) -> None:
        """Stub compatibility."""
        self.checks[name] = check_func

    def record_request(self, success: bool, latency_ms: int) -> None:
        """Stub compatibility."""
        self.request_count += 1
        self.total_latency += latency_ms
        if not success: self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Stub compatibility."""
        error_rate = self.error_count / self.request_count if self.request_count > 0 else 0
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0
        return {"total_requests": self.request_count, "error_count": self.error_count, "error_rate": error_rate, "avg_latency_ms": avg_latency}

    def check(self) -> Dict[str, Any]:
        """Stub compatibility mixed with real check if results exist."""
        components = {name: func() for name, func in self.checks.items()}
        base_status = {"status": "healthy", "components": components}
        if self.results:
            base_status["details"] = {k: v.status.name for k, v in self.results.items()}
        return base_status

    def check_agent_script(self, agent_name: str) -> AgentHealthCheck:
        """Check if an agent script exists and is valid."""
        start_time = time.time()
        # Look for script in src/ directory
        script_path = self.repo_root / f'src/agent_{agent_name}.py'

        if not script_path.exists():
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Script not found: {script_path}"
            )

        try:
            import ast
            content = script_path.read_text(encoding='utf-8', errors='ignore')
            ast.parse(content)
            response_time = (time.time() - start_time) * 1000
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.HEALTHY,
                response_time_ms=response_time,
                details={'script_path': str(script_path)}
            )
        except SyntaxError as e:
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Syntax error: {e}"
            )

    def check_git(self) -> AgentHealthCheck:
        """Check if git is available."""
        start_time = time.time()
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=5)
            response_time = (time.time() - start_time) * 1000
            if result.returncode == 0:
                return AgentHealthCheck(agent_name='git', status=HealthStatus.HEALTHY, response_time_ms=response_time, details={'version': result.stdout.strip()})
            return AgentHealthCheck(agent_name='git', status=HealthStatus.UNHEALTHY, error_message=result.stderr)
        except Exception as e:
            return AgentHealthCheck(agent_name='git', status=HealthStatus.UNHEALTHY, error_message=str(e))

    def check_python(self) -> AgentHealthCheck:
        """Check Python environment."""
        start_time = time.time()
        return AgentHealthCheck(
            agent_name='python',
            status=HealthStatus.HEALTHY,
            response_time_ms=(time.time() - start_time) * 1000,
            details={'version': sys.version, 'executable': sys.executable}
        )

    def run_all_checks(self) -> Dict[str, AgentHealthCheck]:
        """Run all health checks."""
        agent_names = ['coder', 'tests', 'changes', 'context', 'errors', 'improvements', 'stats']
        self.results['python'] = self.check_python()
        self.results['git'] = self.check_git()
        for name in agent_names:
            self.results[name] = self.check_agent_script(name)
        return self.results

    def is_healthy(self) -> bool:
        """Check if all components are healthy."""
        if not self.results: self.run_all_checks()
        return all(r.status == HealthStatus.HEALTHY for r in self.results.values())

class ProfileManager:
    """Manages configuration profiles and execution profiles."""
    
    def __init__(self) -> None:
        self._profiles: Dict[str, ExecutionProfile] = {}
        self.profiles: Dict[str, ConfigProfile] = {} # Stub compatibility
        self._active: Optional[str] = None
        self.active_name: Optional[str] = None # Stub compatibility
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default execution profiles."""
        self._profiles["default"] = ExecutionProfile(
            name="default",
            timeout=120,
            parallel=False,
        )

        self._profiles["fast"] = ExecutionProfile(
            name="fast",
            max_files=10,
            timeout=60,
            parallel=True,
            workers=4,
        )

        self._profiles["ci"] = ExecutionProfile(
            name="ci",
            timeout=300,
            parallel=True,
            workers=2,
            dry_run=True,
        )

    def add_profile(self, profile: Any) -> None:
        """Add a profile (either ExecutionProfile or ConfigProfile)."""
        if hasattr(profile, 'name'):
            if isinstance(profile, ExecutionProfile):
                self._profiles[profile.name] = profile
            else:
                self.profiles[profile.name] = profile

    def activate(self, name: str) -> None:
        """Activate a profile by name."""
        if name in self._profiles:
            self._active = name
        if name in self.profiles:
            self.active_name = name

    def set_active(self, name: str) -> None:
        """Stub compatibility."""
        self.activate(name)

    def get_active_config(self) -> Optional[ExecutionProfile]:
        """Get active execution profile."""
        if self._active:
            return self._profiles[self._active]
        return None

    @property
    def active(self) -> Optional[Any]:
        """Get active profile (ConfigProfile takes priority for stub compatibility)."""
        if self.active_name and self.active_name in self.profiles:
            return self.profiles[self.active_name]
        return self.get_active_config()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Stub compatibility for ConfigProfile settings."""
        active_p = self.active
        if not active_p or not hasattr(active_p, 'settings'):
            return default
        
        if key in active_p.settings:
            return active_p.settings[key]
            
        if hasattr(active_p, 'parent') and active_p.parent and active_p.parent in self.profiles:
            parent = self.profiles[active_p.parent]
            if key in parent.settings:
                return parent.settings[key]
        return default


