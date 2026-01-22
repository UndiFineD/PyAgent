# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Core storage utilities for PyAgent."""

import json
import yaml
import logging
import os
from pathlib import Path
from typing import Any, Optional, Union

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.storage")

class StorageCore:
    """
    Centralized I/O logic for JSON and YAML.
    Reduces redundancy across the codebase.
    """

    @staticmethod
    def load_json(path: Union[str, Path], default: Any = None) -> Any:
        """Safely load JSON data from a file."""
        p = Path(path)
        if not p.exists():
            return default
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error("Failed to load JSON from %s: %s", p, e)
            return default

    @staticmethod
    def save_json(path: Union[str, Path], data: Any, indent: int = 4):
        """Safely save data to a JSON file, creating directories if needed."""
        p = Path(path)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            
            # Use Rust acceleration for atomic, high-speed write if available
            if rc and hasattr(rc, "save_json_atomic_rust"):
                content = json.dumps(data, indent=indent)
                if rc.save_json_atomic_rust(str(p), content):
                    return

            with open(p, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent)
        except Exception as e:
            logger.error("Failed to save JSON to %s: %s", p, e)

    @staticmethod
    def load_yaml(path: Union[str, Path], default: Any = None) -> Any:
        """Safely load YAML data from a file."""
        p = Path(path)
        if not p.exists():
            return default
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error("Failed to load YAML from %s: %s", p, e)
            return default

    @staticmethod
    def save_yaml(path: Union[str, Path], data: Any):
        """Safely save data to a YAML file, creating directories if needed."""
        p = Path(path)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False)
        except Exception as e:
            logger.error("Failed to save YAML to %s: %s", p, e)

    @staticmethod
    def to_json(data: Any, indent: int = 4) -> str:
        """Convert data to a JSON formatted string."""
        return json.dumps(data, indent=indent)

    @staticmethod
    def to_yaml(data: Any) -> str:
        """Convert data to a YAML formatted string."""
        return yaml.dump(data, default_flow_style=False)
