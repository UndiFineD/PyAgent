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
Core storage utilities for PyAgent.
"""

import json
import logging
from pathlib import Path
from typing import Any, Union

import yaml

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
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:  # pylint: disable=broad-exception-caught
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
                if rc.save_json_atomic_rust(str(p), content):  # pylint: disable=no-member
                    return

            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to save JSON to %s: %s", p, e)

    @staticmethod
    def load_yaml(path: Union[str, Path], default: Any = None) -> Any:
        """Safely load YAML data from a file."""
        p = Path(path)
        if not p.exists():
            return default
        try:
            with open(p, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to load YAML from %s: %s", p, e)
            return default

    @staticmethod
    def save_yaml(path: Union[str, Path], data: Any):
        """Safely save data to a YAML file, creating directories if needed."""
        p = Path(path)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to save YAML to %s: %s", p, e)

    @staticmethod
    def to_json(data: Any, indent: int = 4) -> str:
        """Convert data to a JSON formatted string."""
        return json.dumps(data, indent=indent)

    @staticmethod
    def to_yaml(data: Any) -> str:
        """Convert data to a YAML formatted string."""
        return yaml.dump(data, default_flow_style=False)
