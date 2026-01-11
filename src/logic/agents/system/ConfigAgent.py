#!/usr/bin/env python3

"""Agent specializing in configuration validation, secrets checking, and environment setup.
Inspired by external-secrets and infrastructure-as-code patterns.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import VERSION

__version__ = VERSION

class ConfigAgent(BaseAgent):
    """Ensures the agent fleet has all necessary configurations and API keys."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
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
        missing = [key for key in required if key not in os.environ]
        
        report = ["## ⚙️ Environment Validation\n"]
        if not missing:
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
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
            
            # Simple structure check
            if "models" in data and isinstance(data["models"], list):
                return f"✅ `models.yaml` is valid. Detected {len(data['models'])} models."
            else:
                return "❌ `models.yaml` has invalid structure (missing 'models' list)."
        except Exception as e:
            return f"❌ Error parsing `models.yaml`: {e}"

    def improve_content(self, prompt: str) -> str:
        return self.validate_env()
