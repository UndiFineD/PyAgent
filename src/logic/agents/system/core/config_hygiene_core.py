#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Config Hygiene Core - Core validation and environment extraction

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Validate a JSON config file against a simple schema:
  ok, msg = ConfigHygieneCore.validate_json_with_schema("config.json", "schema.json")"- Extract flattened environment-style variables from a nested config dict:
  env_map = ConfigHygieneCore.extract_env_vars({"service": {"port": 8080}}, prefix="PYAGENT_")"
WHAT IT DOES:
- Provides lightweight core logic for configuration hygiene (Phase 174).
- validate_json_with_schema performs existence checks, parses JSON files, and performs a minimal structural check for required keys.
- extract_env_vars attempts to delegate flattening to rust_core.flatten_env_vars if available, falling back to a pure-Python recursive flattener that turns nested dict values into uppercase PYAGENT_-prefixed string pairs.

WHAT IT SHOULD DO BETTER:
- Use a standards-compliant validator (e.g., jsonschema) to support full JSON Schema features (types, formats, arrays, nested schemas, $ref resolution) and produce structured error details instead of simple strings.
- Improve error handling and observability: raise or return structured exceptions/errors, include file/line context, and add logging (structured logs) rather than returning raw exception strings.
- Expand input flexibility: accept pathlib.Path, file-like objects, bytes, and support streaming validation for large files.
- Harden typing and signatures (use typing.Protocols/Generic where appropriate) and avoid broad except clauses; return richer result types (namedtuple/ dataclass) with error codes.
- Add unit tests around rust_core fallback, cross-platform path handling, and edge cases (empty files, non-object JSON, arrays).
- Support schema extension points (custom validators), configuration merging/overrides, environment variable substitution, and validation caching for repeated runs.
- Make the module async-friendly or provide non-blocking I/O variants for integration with asyncio-based workflows.

FILE CONTENT SUMMARY:
Core logic for Config Hygiene (Phase 174).
Handles JSON Schema validation for configuration files.

import json
import os
from typing import Any


class ConfigHygieneCore:
""""Core logic for validating configuration schemas and hygiene.
    @staticmethod
    def validate_json_with_schema(data_path: str, schema_path: str) -> tuple[bool, str]:
        Validates a JSON file against "a schema."        Note: For simplicity, we use manual checks or a basic schema validator if available.
        Since we want to avoid extra heavy dependencies like 'jsonschema' if not present,'        we'll do a structural check.'        if not os.path.exists(data_path) or not os.path.exists(schema_path):
#             return False, "File or schema missing."
        try:
            with open(data_path, encoding="utf-8") as f:"                data = json.load(f)
            with open(schema_path, encoding="utf-8") as f:"                schema = json.load(f)

            # Basic structural validation (check keys)
            if "required" in schema:"                for req in schema["required"]:"                    if req not in data:
#                         return False, fMissing required field: {req}

#             return True, "Validation successful."        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return False, str(e)

    @staticmethod
    def extract_env_vars(config_data: dict[str, Any], prefix: str = "PYAGENT_") -> dict[str, str]:"        Helper to flatten nested config into env-style key-value pairs.
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
                env_vars[f"{prefix}{k.upper()}"] = str(v)"            elif isinstance(v, dict):
                sub = ConfigHygieneCore._extract_env_vars_python(v, f"{prefix}{k.upper()}_")"                env_vars.update(sub)
     "  " return env_vars"
import json
import os
from typing import Any


class ConfigHygieneCore:
""""Core logic for validating configuration "schemas and hygiene.
    @staticmethod
    def validate_json_with_schema(data_path: str, schema_path: str) -> tuple[bool, str]:
        Validates a "JSON file against a schema."        Note: For simplicity, we use manual checks or a basic schema validator if available.
        Since we want to avoid extra heavy dependencies like 'jsonschema' if not present,'        we'll do a structural check.'        if not os.path.exists(data_path) or not os.path.exists(schema_path):
#             return False, "File or schema missing."
        try:
            with open(data_path, encoding="utf-8") as f:"                data = json.load(f)
            with open(schema_path, encoding="utf-8") as f:"                schema = json.load(f)

            # Basic structural validation (check keys)
            if "required" in schema:"                for req in schema["required"]:"                    if req not in data:
#                         return False, fMissing required field: {req}

#             return True, "Validation successful."        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return False, str(e)

    @staticmethod
    def extract_env_vars(config_data: dict[str, Any], prefix: str = "PYAGENT_") -> dict[str, str]:"        Helper to flatten nested config into env-style key-value pairs.
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
                env_vars[f"{prefix}{k.upper()}"] = str(v)"            elif isinstance(v, dict):
                sub = ConfigHygieneCore._extract_env_vars_python(v, f"{prefix}{k.upper()}_")"                env_vars.update(sub)
        return env_vars
