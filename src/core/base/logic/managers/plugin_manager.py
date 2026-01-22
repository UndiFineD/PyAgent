"""
Manager for plugin discovery, loading, and registration.
(Facade for src.core.base.common.plugin_core)
"""

"""
Manager for plugin discovery, loading, and registration.
(Facade for src.core.base.common.plugin_core)
"""

from __future__ import annotations
<<<<<<< HEAD

from src.core.base.common.plugin_core import \
    PluginCore as StandardPluginManager
from src.core.base.common.plugin_core import \
    PluginMetadata as StandardPluginMetadata


=======
from src.core.base.common.plugin_core import (
    PluginCore as StandardPluginManager,
    PluginMetadata as StandardPluginMetadata
)

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class PluginMetadata(StandardPluginMetadata):
    """
    Facade for StandardPluginMetadata to maintain backward compatibility.
    """
    pass

<<<<<<< HEAD

class PluginManager(StandardPluginManager):
    """
    Facade for PluginCore to maintain backward compatibility.
    Plugin management is now centralized in the Infrastructure/Common tier.
    """
=======
class PluginManager(StandardPluginManager):
    """
    Facade for PluginCore to maintain backward compatibility.
    Plugin management is now centralized in the Infrastructure/Common tier.
    """
    pass

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
