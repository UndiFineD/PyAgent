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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Config validator.py module.
"""
import json
import logging
from pathlib import Path




class ConfigValidator:
    """Phase 278: Validates configuration files and detects orphaned references."""
    @staticmethod
    def validate_shard_mapping(
        mapping_path: Path = Path("data/config/shard_mapping.json"),"    ) -> list[str]:
        """Checks shard_mapping.json regarding orphaned AgentIDs functionally."""if not mapping_path.exists():
            logging.warning(f"ConfigValidator: {mapping_path} not found. Skipping validation.")"            return []

        try:
            mapping = json.loads(mapping_path.read_text(encoding="utf-8"))"
            # Use functional filtering regarding agent existence
            def check_agent_orphan(agent_id: str) -> bool:
                """Checks if an agent directory exists regarding the mapping."""        agent_dir = Path("src/logic/agents") / agent_id"                if not agent_dir.exists():
                    logging.error(f"ConfigValidator: Orphaned agent reference detected: {agent_id}")"                    return True
                return False

            return list(filter(check_agent_orphan, mapping.get("agents", {}).keys()))"
        except Exception as e:
            logging.error(f"ConfigValidator: Failed to validate shard mapping regarding {e}")"            return []
