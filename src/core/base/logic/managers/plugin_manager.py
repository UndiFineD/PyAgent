"""
Manager for plugin discovery, loading, and registration.
(Facade for src.core.base.common.plugin_core)
"""

from __future__ import annotations
from src.core.base.common.plugin_core import (
    PluginCore as StandardPluginManager,
    PluginMetadata as StandardPluginMetadata
)

class PluginMetadata(StandardPluginMetadata):
    """
    Facade for StandardPluginMetadata to maintain backward compatibility.
    """
    pass

class PluginManager(StandardPluginManager):
    """
    Facade for PluginCore to maintain backward compatibility.
    Plugin management is now centralized in the Infrastructure/Common tier.
    """
    pass

