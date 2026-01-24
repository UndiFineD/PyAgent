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
Core logic for Config Hygiene (Phase 174).
Handles JSON Schema validation for configuration files.
"""

import json
import os
from typing import Any


class ConfigHygieneCore:
    """Core logic for validating configuration schemas and hygiene."""

    @staticmethod
    def validate_json_with_schema(data_path: str, schema_path: str) -> tuple[bool, str]:
        """
        Validates a JSON file against a schema.
        Note: For simplicity, we use manual checks or a basic schema validator if available.
        Since we want to avoid extra heavy dependencies like 'jsonschema' if not present,
        we'll do a structural check.
        """
        if not os.path.exists(data_path) or not os.path.exists(schema_path):
            return False, "File or schema missing."

        try:
            with open(data_path, encoding="utf-8") as f:
                data = json.load(f)
            with open(schema_path, encoding="utf-8") as f:
                schema = json.load(f)

            # Basic structural validation (check keys)
            if "required" in schema:
                for req in schema["required"]:
                    if req not in data:
                        return False, f"Missing required field: {req}"

            return True, "Validation successful."
        except Exception as e:
            return False, str(e)

    @staticmethod
    def extract_env_vars(config_data: dict[str, Any], prefix: str = "PYAGENT_") -> dict[str, str]:
        """
        Helper to flatten nested config into env-style key-value pairs.
        """
        try:
            import rust_core

            return rust_core.flatten_env_vars(config_data, prefix)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        return ConfigHygieneCore._extract_env_vars_python(config_data, prefix)

    @staticmethod
    def _extract_env_vars_python(config_data: dict[str, Any], prefix: str) -> dict[str, str]:
        env_vars = {}
        for k, v in config_data.items():
            if isinstance(v, (str, int, float, bool)):
                env_vars[f"{prefix}{k.upper()}"] = str(v)
            elif isinstance(v, dict):
                sub = ConfigHygieneCore._extract_env_vars_python(v, f"{prefix}{k.upper()}_")
                env_vars.update(sub)
        return env_vars
