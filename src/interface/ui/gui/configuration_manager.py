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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Configuration management for PyAgent GUI settings."""

from __future__ import annotations

import os

from src.core.base.common.storage_core import StorageCore
from src.core.base.lifecycle.version import VERSION

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
        disk_settings = StorageCore.load_json(self.config_file)
        if disk_settings:
            self.settings.update(disk_settings)

    def save(self) -> None:
        StorageCore.save_json(self.config_file, self.settings)
        # Also update environment variable for backend compatibility
        if "github_token_file" in self.settings:
            os.environ["DV_GITHUB_TOKEN_FILE"] = self.settings["github_token_file"]
