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
"""Plugin management for PyAgent.

Provides :class:`PluginManager` for dynamic registration and lifecycle
management of :class:`Plugin` instances.

Usage::

    from plugins import Plugin, PluginManager

    class MyPlugin(Plugin):
        @property
        def name(self) -> str:
            return "my_plugin"

        def execute(self, **kwargs):
            return {"result": "ok"}

    pm = PluginManager()
    pm.register(MyPlugin())
    result = pm.execute("my_plugin", key="value")
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PluginMetadata:
    """Descriptive metadata attached to a plugin.

    Attributes
    ----------
    name:
        Unique plugin name used as the registration key.
    version:
        Semantic version string (e.g. ``"1.0.0"``).
    description:
        Human readable description of what the plugin does.
    author:
        Plugin author identifier.
    tags:
        Optional list of capability tags for discovery.

    """

    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    tags: list[str] = field(default_factory=list)


class Plugin(ABC):
    """Abstract base class for all PyAgent plugins.

    Subclasses must implement :meth:`name` and :meth:`execute`.
    Optionally override :meth:`setup` and :meth:`teardown` for lifecycle hooks.

    Notes
    -----
    * Plugins are identified by their :attr:`name` property.
    * :meth:`setup` is called once when registered with a :class:`PluginManager`.
    * :meth:`teardown` is called when the plugin is unregistered or the manager
      is shut down.

    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique plugin name (used as registration key)."""

    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata.  Defaults to minimal metadata from :attr:`name`."""
        return PluginMetadata(name=self.name)

    def setup(self) -> None:  # noqa: B027
        """Called once after the plugin is registered.  Override as needed."""

    def teardown(self) -> None:  # noqa: B027
        """Called when the plugin is removed or the manager shuts down."""

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute plugin logic with the provided keyword arguments.

        Parameters
        ----------
        **kwargs:
            Arbitrary keyword arguments forwarded from the caller.

        Returns
        -------
        Any
            Plugin-defined return value.

        """


class PluginManager:
    """Registry and lifecycle manager for :class:`Plugin` instances.

    Plugins are stored by name.  Registering a second plugin with the same
    name replaces the existing one (after calling its :meth:`~Plugin.teardown`).

    Example:
    -------
    >>> pm = PluginManager()
    >>> pm.register(my_plugin)
    >>> result = pm.execute("my_plugin", foo="bar")

    """

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, plugin: Plugin) -> None:
        """Register *plugin*, calling its :meth:`~Plugin.setup` hook.

        If a plugin with the same name already exists its :meth:`~Plugin.teardown`
        is called before replacement.
        """
        name = plugin.name
        if name in self._plugins:
            logger.info("Replacing plugin %r; calling teardown on old instance.", name)
            self._plugins[name].teardown()
        self._plugins[name] = plugin
        plugin.setup()
        logger.debug("Registered plugin %r (version=%s).", name, plugin.metadata.version)

    def unregister(self, name: str) -> None:
        """Remove the plugin identified by *name*, calling its teardown hook.

        Raises
        ------
        KeyError
            If no plugin with *name* is registered.

        """
        plugin = self._plugins.pop(name)
        plugin.teardown()
        logger.debug("Unregistered plugin %r.", name)

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def get(self, name: str) -> Plugin:
        """Return the plugin registered under *name*.

        Raises
        ------
        KeyError
            If no plugin with *name* is registered.

        """
        try:
            return self._plugins[name]
        except KeyError:
            raise KeyError(f"No plugin registered with name {name!r}") from None

    def list_plugins(self) -> list[PluginMetadata]:
        """Return metadata for all registered plugins, sorted by name."""
        return [p.metadata for p in sorted(self._plugins.values(), key=lambda p: p.name)]

    def has(self, name: str) -> bool:
        """Return True if a plugin named *name* is registered."""
        return name in self._plugins

    def find_by_tag(self, tag: str) -> list[Plugin]:
        """Return all plugins whose metadata includes *tag*."""
        return [p for p in self._plugins.values() if tag in p.metadata.tags]

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self, name: str, **kwargs: Any) -> Any:
        """Execute the plugin identified by *name* with *kwargs*.

        Parameters
        ----------
        name:
            Registered plugin name.
        **kwargs:
            Forwarded to :meth:`Plugin.execute`.

        Raises
        ------
        KeyError
            If no plugin with *name* is registered.

        """
        return self.get(name).execute(**kwargs)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _teardown_one(self, name: str, plugin: "Plugin") -> None:
        """Teardown a single plugin, logging any exception."""
        try:
            plugin.teardown()
        except Exception:  # noqa: BLE001
            logger.exception("Error during teardown of plugin %r.", name)

    def shutdown(self) -> None:
        """Call :meth:`~Plugin.teardown` on all registered plugins and clear registry."""
        _ = [self._teardown_one(name, plugin) for name, plugin in list(self._plugins.items())]
        self._plugins.clear()

    def __len__(self) -> int:
        return len(self._plugins)

    def __repr__(self) -> str:
        names = sorted(self._plugins)
        return f"PluginManager(plugins={names!r})"
