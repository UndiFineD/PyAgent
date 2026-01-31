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


class ConfigObject:  # pylint: disable=too-few-public-methods
    """A dictionary wrapper that allows dot-notation access."""

    def __init__(self, data: Dict[str, Any]) -> None:
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

    def __init__(self, workspace_root: Path | str | None = None) -> None:
        super().__init__()
        # Use repo_root from BaseCore if available
        root = workspace_root or self.repo_root or Path.cwd()
        if isinstance(root, str):
            root = Path(root)

        if root.is_file() or (isinstance(root, Path) and root.suffix in self.SUPPORTED_EXTENSIONS):
            self.config_path = root
            self.workspace_root = root.parent
            # Auto-detect format from path
            ext = root.suffix.lower()
            self.format = self.SUPPORTED_EXTENSIONS.get(ext, ConfigFormat.JSON)
        else:
            self.workspace_root = root
            self.config_path = None
            self.format = ConfigFormat.JSON

        self.root_dir = self.workspace_root  # Alias for compatibility
        self.config_dir = self.workspace_root / "data" / "config"
        self.configs: Dict[str, ConfigObject] = {}

    def load(self, path: Path | None = None) -> ConfigObject:
        """Legacy alias for load_config, using self.config_path if none provided."""
        target = path or self.config_path
        if not target:
            return ConfigObject({})
        return self.load_config(target)

    @staticmethod
    def find_config_file(directory: Path) -> Path | None:
        """Find the primary config file in a directory."""
        for ext in [".json", ".yaml", ".yml", ".toml"]:
            # Added 'agent' for compatibility
            for name in ["config", "settings", "pyagent", "agent"]:
                path = directory / f"{name}{ext}"
                if path.exists():
                    return path
        return None

    def refresh(self) -> None:
        """Reload all configurations from disk."""
        if self.config_dir.exists():
            for file_path in self.config_dir.glob("*.*"):
                if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    self.load_config(file_path)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Global getter with environment variable override support.
        Prefix: PYAGENT_ (e.g. models.coder.temperature -> PYAGENT_MODELS__CODER__TEMPERATURE)
        """
        import os
        # 1. Check environment variables (support double underscores for nesting)
        env_key = f"PYAGENT_{key.upper().replace('.', '__')}"
        if env_key in os.environ:
            env_val = os.environ[env_key]
            try:
                if "." in env_val:
                    return float(env_val)
                return int(env_val)
            except ValueError:
                return env_val

        # 2. Check loaded configs
        for cfg in self.configs.values():
            val = cfg.get(key)
            if val is not None:
                return val
        return default

    def load_config(self, path: Path) -> ConfigObject:
        """Load and return a configuration object."""
        if not path.exists():
            return ConfigObject({})
        if self._can_use_rust_loader(path):
            data = self._try_rust_load_config(path)
            if data is not None:
                return ConfigObject(data)
        ext = path.suffix.lower()
        fmt = self.SUPPORTED_EXTENSIONS.get(ext, ConfigFormat.JSON)
        return self._try_python_load_config(path, fmt)

    def _can_use_rust_loader(self, path: Path) -> bool:
        return rc and hasattr(rc, "load_config_rust") and path.suffix in [".ini", ".conf"]

    def _try_rust_load_config(self, path: Path) -> dict[str, Any] | None:
        try:
            return rc.load_config_rust(str(path))  # type: ignore
        except RuntimeError as e:
            logging.error("ConfigCore: Rust load_config_rust failed for %s: %s", path, e)
            return None

    def _try_python_load_config(self, path: Path, fmt: ConfigFormat) -> ConfigObject:
        try:
            content = path.read_text()
            data = self._parse(content, fmt)
            cfg = ConfigObject(data)
            self.configs[path.name] = cfg
            return cfg
        except (OSError, ValueError) as e:
            logging.error("ConfigCore: Failed to load %s: %s", path, e)
            return ConfigObject({})

    def merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two config dicts. Rust-accelerated for large trees."""
        if self._can_use_rust_merge():
            merged = self._try_rust_merge_configs(base, override)
            if merged is not None:
                return merged
        return self._python_merge_configs(base, override)

    def _can_use_rust_merge(self) -> bool:
        return rc and hasattr(rc, "merge_configs_rust")

    def _try_rust_merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any] | None:
        try:
            return rc.merge_configs_rust(base, override)  # type: ignore
        except RuntimeError as e:
            logging.error("ConfigCore: Rust merge_configs_rust failed: %s", e)
            return None

    def _python_merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        merged = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _parse(self, content: str, fmt: ConfigFormat) -> Dict[str, Any]:
        """Parses configuration content based on format."""
        data: Any = {}
        try:
            data = self._parse_by_format(content, fmt)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            logging.error("ConfigCore: Failed to parse config content: %s", e)
            return {}
        if isinstance(data, list):
            return {"items": data}
        return data if isinstance(data, dict) else {}

    def _parse_by_format(self, content: str, fmt: ConfigFormat) -> Any:
        if fmt == ConfigFormat.JSON:
            return json.loads(content)
        elif fmt == ConfigFormat.YAML:
            try:
                import yaml  # type: ignore
                return yaml.safe_load(content)
            except ImportError:
                logging.warning("ConfigCore: YAML import failed.")
                return {}
        elif fmt == ConfigFormat.TOML:
            try:
                import tomllib as toml  # type: ignore
                return toml.loads(content)
            except ImportError:
                logging.warning("ConfigCore: TOML import failed.")
                return {}
        elif fmt in (ConfigFormat.INI, ConfigFormat.CONF):
            # Basic INI parsing if needed, but RC usually handles it
            return {}
        return {}
