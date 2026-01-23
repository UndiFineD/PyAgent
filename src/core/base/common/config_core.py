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

"""
Unified Configuration Core for PyAgent.
Combines loading, merging, and dot-notation access logic.
"""

from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any, Dict
from .base_core import BaseCore
from .models import ConfigFormat

try:
    import rust_core as rc
except ImportError:
    rc = None

class ConfigObject: # pylint: disable=too-few-public-methods
    """A dictionary wrapper that allows dot-notation access."""
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigObject(value))
            elif isinstance(value, list):
                setattr(self, key, [ConfigObject(v) if isinstance(v, dict) else v for v in value])
            else:
                setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Standard getter for dot-notation keys."""
        try:
            val = self
            for part in key.split("."):
                val = getattr(val, part)
            return val
        except (AttributeError, TypeError):
            return default

class ConfigCore(BaseCore):
    """
    Standard implementation for configuration management.
    Handles multi-format loading and hierarchical merging.
    """

    SUPPORTED_EXTENSIONS = {
        ".yaml": ConfigFormat.YAML,
        ".yml": ConfigFormat.YAML,
        ".toml": ConfigFormat.TOML,
        ".json": ConfigFormat.JSON,
        ".ini": ConfigFormat.INI,
    }

    def __init__(self, workspace_root: Path | None = None):
        super().__init__()
        self.workspace_root = workspace_root or Path(".")
        self.configs: Dict[str, ConfigObject] = {}

    def load_config(self, path: Path) -> ConfigObject:
        """Load and return a configuration object."""
        if not path.exists():
            return ConfigObject({})

        # Try Rust-accelerated fast loading for flat configs
        if rc and hasattr(rc, "load_config_rust") and path.suffix in [".ini", ".conf"]: # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                data = rc.load_config_rust(str(path)) # type: ignore
                return ConfigObject(data)
            except Exception: # pylint: disable=broad-exception-caught
                pass

        ext = path.suffix.lower()
        fmt = self.SUPPORTED_EXTENSIONS.get(ext, ConfigFormat.JSON)

        try:
            content = path.read_text()
            data = self._parse(content, fmt)
            cfg = ConfigObject(data)
            self.configs[path.name] = cfg
            return cfg
        except Exception as e: # pylint: disable=broad-exception-caught
            logging.error("ConfigCore: Failed to load %s: %s", path, e)
            return ConfigObject({})

    def merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two config dicts. Rust-accelerated for large trees."""
        if rc and hasattr(rc, "merge_configs_rust"): # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.merge_configs_rust(base, override) # type: ignore
            except Exception: # pylint: disable=broad-exception-caught
                pass

        # Python fallback
        merged = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _parse(self, content: str, fmt: ConfigFormat) -> Dict[str, Any]:
        """Parses configuration content based on format."""
        if fmt == ConfigFormat.JSON:
            return json.loads(content)
        # Add YAML/TOML fallbacks here
        return {}
