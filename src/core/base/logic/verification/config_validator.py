
"""
Config validator.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import json
import logging
from pathlib import Path


class ConfigValidator:
    """Phase 278: Validates configuration files and detects orphaned references."""

    @staticmethod
    def validate_shard_mapping(
        mapping_path: Path = Path("data/config/shard_mapping.json"),
    ) -> list[str]:
        """Checks shard_mapping.json for orphaned AgentIDs."""
        if not mapping_path.exists():
            logging.warning(f"ConfigValidator: {mapping_path} not found. Skipping validation.")
            return []

        orphans = []
        try:
            mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
            # Heuristic: Check if the agent folder exists in src/ (just a demo check)

            for agent_id in mapping.get("agents", {}).keys():
                agent_dir = Path("src/logic/agents") / agent_id
                if not agent_dir.exists():
                    orphans.append(agent_id)
                    logging.error(f"ConfigValidator: Orphaned agent reference detected: {agent_id}")

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"ConfigValidator: Failed to validate shard mapping: {e}")

        return orphans
