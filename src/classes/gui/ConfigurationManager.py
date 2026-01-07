#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration management for PyAgent GUI settings."""

import json
import os

class ConfigurationManager:
    """Handles loading and saving global configuration settings."""
    def __init__(self, config_file="config/gui_settings.json"):
        self.config_file = config_file
        self.settings = {
            "github_token_file": r"C:\DEV\github-gat.txt",
            "default_model": "gpt-4o",
            "cache_enabled": True,
            "monitor_scaling": 1.0
        }
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    disk_settings = json.load(f)
                    self.settings.update(disk_settings)
            except Exception:
                pass

    def save(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()
        # Also update environment variable for backend compatibility
        if key == "github_token_file":
            os.environ["DV_GITHUB_TOKEN_FILE"] = value
