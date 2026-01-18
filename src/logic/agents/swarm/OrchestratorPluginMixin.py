#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import logging
import importlib.util
from pathlib import Path
from typing import Any
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from src.core.base.AgentPluginBase import AgentPluginBase
from src.core.base.models import AgentPluginConfig


class OrchestratorPluginMixin:
    """Plugin system methods for OrchestratorAgent."""

    def register_plugin(self, plugin: AgentPluginBase) -> None:
        """Register a custom agent plugin."""
        if not hasattr(self, "plugins"):
            self.plugins: dict[str, AgentPluginBase] = {}

        plugin.setup()
        self.plugins[plugin.name] = plugin
        logging.info(
            f"Registered plugin: {plugin.name} (priority: {plugin.priority.name})"
        )

    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin by name."""
        if not hasattr(self, "plugins") or plugin_name not in self.plugins:
            return False

        plugin = self.plugins[plugin_name]
        plugin.teardown()
        del self.plugins[plugin_name]
        logging.info(f"Unregistered plugin: {plugin_name}")
        return True

    def get_plugin(self, plugin_name: str) -> AgentPluginBase | None:
        """Get a registered plugin by name."""
        if not hasattr(self, "plugins"):
            return None
        return self.plugins.get(plugin_name)

    def run_plugins(self, file_path: Path) -> dict[str, bool]:
        """Run all registered plugins on a file."""
        if not hasattr(self, "plugins") or not self.plugins:
            return {}

        results: dict[str, bool] = {}
        context: dict[str, Any] = {
            "agent": self,
            "repo_root": getattr(self, "repo_root", Path(".")),
            "dry_run": getattr(self, "dry_run", False),
            "metrics": getattr(self, "metrics", {}),
        }

        # Sort plugins by priority
        sorted_plugins = sorted(self.plugins.values(), key=lambda p: p.priority.value)

        for plugin in sorted_plugins:
            if not plugin.config.get("enabled", True):
                continue

            try:
                if hasattr(self, "rate_limiter"):
                    self.rate_limiter.acquire(timeout=30.0)

                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(plugin.run, file_path, context)
                    try:
                        result = future.result(timeout=5.0)
                    except TimeoutError:
                        logging.warning(f"Plugin {plugin.name} timed out. Skipping.")
                        result = False

                results[plugin.name] = result
                if result and hasattr(self, "metrics"):
                    if "agents_applied" not in self.metrics:
                        self.metrics["agents_applied"] = {}
                    self.metrics["agents_applied"][plugin.name] = (
                        self.metrics["agents_applied"].get(plugin.name, 0) + 1
                    )

            except Exception as e:
                logging.error(f"Plugin {plugin.name} failed: {e}")
                results[plugin.name] = False

        return results

    def load_plugins_from_config(self, plugin_configs: list[AgentPluginConfig]) -> None:
        """Load plugins from configuration."""
        for config in plugin_configs:
            if not config.enabled:
                continue

            try:
                spec = importlib.util.spec_from_file_location(
                    config.name, config.module_path
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugin_class = getattr(module, config.entry_point, None)
                    if plugin_class and issubclass(plugin_class, AgentPluginBase):
                        plugin = plugin_class(
                            config.name, config.priority, config.config
                        )
                        self.register_plugin(plugin)
            except Exception as e:
                logging.error(f"Failed to load plugin {config.name}: {e}")
