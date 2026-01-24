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


"""Agent specializing in configuration validation, secrets checking, and environment setup.
Inspired by external-secrets and infrastructure-as-code patterns.
"""

from __future__ import annotations

import yaml

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.core.validation import ValidationCore

__version__ = VERSION


class ConfigAgent(BaseAgent):
    """Ensures the agent fleet has all necessary configurations and API keys."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.validator = ValidationCore()
        self.workspace_root = self.file_path.parent.parent.parent
        self._system_prompt = (
            "You are the Config Agent. "
            "Your role is to verify the environment and project settings. "
            "Check for missing API keys, invalid YAML configs, and environment contradictions. "
            "Never display secret values in your output."
        )

    @as_tool
    def validate_env(self) -> str:
        """Checks for required environment variables."""
        required = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "WORKSPACE_ROOT"]
        success, missing = self.validator.validate_env_vars(required)

        report = ["## ⚙️ Environment Validation\n"]
        if success:
            report.append("✅ All required environment variables are set.")
        else:
            report.append(f"❌ **Missing variables**: {', '.join(missing)}")

        return "\n".join(report)

    @as_tool
    def validate_models_yaml(self) -> str:
        """Verifies the integrity of models.yaml."""
        config_path = self.workspace_root / "config" / "models.yaml"
        if not config_path.exists():
            return "❌ `config/models.yaml` not found."

        try:
            with open(config_path) as f:
                data = yaml.safe_load(f)

            # Simple structure check
            if "models" in data and isinstance(data["models"], list):
                return f"✅ `models.yaml` is valid. Detected {len(data['models'])} models."
            else:
                return "❌ `models.yaml` has invalid structure (missing 'models' list)."
        except Exception as e:
            return f"❌ Error parsing `models.yaml`: {e}"

    def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        return self.validate_env()
