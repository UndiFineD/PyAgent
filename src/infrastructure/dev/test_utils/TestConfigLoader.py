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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from pathlib import Path
from typing import Any
import json

__version__ = VERSION


class TestConfigLoader:
    """Loads test configuration from files."""

    __test__ = False

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize config loader."""
        self.config_path = config_path or Path("test_config.json")
        self.config: dict[str, Any] = {}

    def load(
        self, path: Path | None = None, defaults: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Load configuration.

        Compatibility:
        - Tests pass a `Path` to load.
        - Tests may pass `defaults=` to be merged.
        """
        if path is not None:
            self.config_path = Path(path)

        loaded: dict[str, Any] = {}
        if self.config_path.exists():
            with open(self.config_path, encoding="utf-8") as f:
                loaded = json.load(f)

        if defaults:
            merged = dict(defaults)
            merged.update(loaded)
            self.config = merged
        else:
            self.config = loaded

        return self.config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
