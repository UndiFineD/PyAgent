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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Configuration management for PyAgent GUI settings."""

from __future__ import annotations
from src.core.base.Version import VERSION
from typing import Any
import json
import os

__version__ = VERSION


class ConfigurationManager:
    """Handles loading and saving global configuration settings."""

    def __init__(self, config_file="config/gui_settings.json") -> None:
        self.config_file: str = config_file
        self.settings = {
            "github_token_file": r"C:\DEV\github-gat.txt",
            "default_model": "gpt-4o",
            "cache_enabled": True,
            "monitor_scaling": 1.0,
        }
        self.load()

    def load(self) -> None:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file) as f:
                    disk_settings = json.load(f)
                    self.settings.update(disk_settings)
            except Exception:
                pass

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self.save()
        # Also update environment variable for backend compatibility
        if key == "github_token_file":
            os.environ["DV_GITHUB_TOKEN_FILE"] = value
