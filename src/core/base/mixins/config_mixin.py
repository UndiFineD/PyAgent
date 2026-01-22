# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Mixin for agent configuration access."""

from typing import Any
from src.core.base.configuration.config_manager import config

class ConfigMixin:
    """Provides configuration access to agents."""
    
    @property
    def config(self):
        """Access the global configuration manager."""
        return config

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return config.get(key, default)
