
"""
Core logic for Config Hygiene (Phase 174).
Handles JSON Schema validation for configuration files.
"""

import json
import os
from typing import Dict, Any

class ConfigHygieneCore:
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
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            with open(schema_path, "r", encoding="utf-8") as f:
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
    def extract_env_vars(config_data: Dict[str, Any], prefix: str = "PYAGENT_") -> Dict[str, str]:
        """
        Helper to flatten nested config into env-style key-value pairs.
        """
        env_vars = {}
        for k, v in config_data.items():
            if isinstance(v, (str, int, float, bool)):
                env_vars[f"{prefix}{k.upper()}"] = str(v)
            elif isinstance(v, dict):
                sub = ConfigHygieneCore.extract_env_vars(v, f"{prefix}{k.upper()}_")
                env_vars.update(sub)
        return env_vars