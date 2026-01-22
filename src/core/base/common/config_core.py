<<<<<<< HEAD
<<<<<<< HEAD
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

=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Configuration Core for PyAgent.
Combines loading, merging, and dot-notation access logic.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

import json
import logging
from pathlib import Path
from typing import Any, Dict

from .base_core import BaseCore
from .models import ConfigFormat
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
<<<<<<< HEAD
<<<<<<< HEAD
from src.core.base.common.base_core import BaseCore
from src.core.base.common.models import ConfigFormat
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from .base_core import BaseCore
from .models import ConfigFormat
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
=======
from .base_core import BaseCore
from .models import ConfigFormat
>>>>>>> 2a6f2626e (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
<<<<<<< HEAD

class ConfigObject:  # pylint: disable=too-few-public-methods
    """A dictionary wrapper that allows dot-notation access."""

    def __init__(self, data: Dict[str, Any]) -> None:
=======
class ConfigObject:
    """A dictionary wrapper that allows dot-notation access."""
    def __init__(self, data: Dict[str, Any]):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
class ConfigObject:
    """A dictionary wrapper that allows dot-notation access."""
    def __init__(self, data: Dict[str, Any]):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigObject(value))
            elif isinstance(value, list):
                setattr(self, key, [ConfigObject(v) if isinstance(v, dict) else v for v in value])
            else:
                setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
<<<<<<< HEAD
<<<<<<< HEAD
        """Standard getter for dot-notation keys."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        try:
            val = self
            for part in key.split("."):
                val = getattr(val, part)
            return val
        except (AttributeError, TypeError):
            return default

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class ConfigCore(BaseCore):
    """
    Standard implementation for configuration management.
    Handles multi-format loading and hierarchical merging.
    """
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    SUPPORTED_EXTENSIONS = {
        ".yaml": ConfigFormat.YAML,
        ".yml": ConfigFormat.YAML,
        ".toml": ConfigFormat.TOML,
        ".json": ConfigFormat.JSON,
        ".ini": ConfigFormat.INI,
    }

<<<<<<< HEAD
<<<<<<< HEAD
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

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def __init__(self, workspace_root: Path | None = None):
        super().__init__()
        self.workspace_root = workspace_root or Path(".")
        self.configs: Dict[str, ConfigObject] = {}

<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def load_config(self, path: Path) -> ConfigObject:
        """Load and return a configuration object."""
        if not path.exists():
            return ConfigObject({})
<<<<<<< HEAD
<<<<<<< HEAD

        # Try Rust-accelerated fast loading for flat configs
        if rc and hasattr(rc, "load_config_rust") and path.suffix in [".ini", ".conf"]:  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                data = rc.load_config_rust(str(path))  # type: ignore
                return ConfigObject(data)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        
        # Try Rust-accelerated fast loading for flat configs
        if rc and hasattr(rc, "load_config_rust") and path.suffix in [".ini", ".conf"]:
            try:
                data = rc.load_config_rust(str(path))
                return ConfigObject(data)
            except Exception:
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                pass

        ext = path.suffix.lower()
        fmt = self.SUPPORTED_EXTENSIONS.get(ext, ConfigFormat.JSON)
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        try:
            content = path.read_text()
            data = self._parse(content, fmt)
            cfg = ConfigObject(data)
            self.configs[path.name] = cfg
            return cfg
<<<<<<< HEAD
<<<<<<< HEAD
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("ConfigCore: Failed to load %s: %s", path, e)
=======
        except Exception as e:
            logging.error(f"ConfigCore: Failed to load {path}: {e}")
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        except Exception as e:
            logging.error(f"ConfigCore: Failed to load {path}: {e}")
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return ConfigObject({})

    def merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two config dicts. Rust-accelerated for large trees."""
<<<<<<< HEAD
<<<<<<< HEAD
        if rc and hasattr(rc, "merge_configs_rust"):  # pylint: disable=no-member
            try:
                # pylint: disable=no-member
                return rc.merge_configs_rust(base, override)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if rc and hasattr(rc, "merge_configs_rust"):
            try:
                return rc.merge_configs_rust(base, override)
            except Exception:
                pass
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Python fallback
        merged = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _parse(self, content: str, fmt: ConfigFormat) -> Dict[str, Any]:
<<<<<<< HEAD
<<<<<<< HEAD
        """Parses configuration content based on format."""
        data: Any = {}
        try:
            if fmt == ConfigFormat.JSON:
                data = json.loads(content)
            elif fmt == ConfigFormat.YAML:
                try:
                    import yaml  # type: ignore
                    data = yaml.safe_load(content)
                except ImportError:
                    pass
            elif fmt == ConfigFormat.TOML:
                try:
                    import tomllib as toml  # type: ignore
                    data = toml.loads(content)
                except ImportError:
                    pass
            elif fmt in (ConfigFormat.INI, ConfigFormat.CONF):
                # Basic INI parsing if needed, but RC usually handles it
                pass
        except Exception as e:  # pylint: disable=broad-exception-caught
            return {}

        if isinstance(data, list):
            return {"items": data}
        return data if isinstance(data, dict) else {}
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if fmt == ConfigFormat.JSON:
            return json.loads(content)
        # Add YAML/TOML fallbacks here
        return {}
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
