#!/usr/bin/env python3

"""Attribution Engine for PyAgent.
Tracks the lineage and provenance of every generated piece of content or code.
"""

import hashlib
import time
import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any
from src.infrastructure.fleet.core.AttributionCore import AttributionCore

class AttributionEngine:
    """Records the 'who, when, and how' for all system outputs (Phase 185)."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.log_file = self.workspace_root / "data/fleet/attribution_log.json"
        self.core = AttributionCore()
        os.makedirs(self.log_file.parent, exist_ok=True)
        self.records: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if self.log_file.exists():
            with open(self.log_file, "r") as f:
                return json.load(f)
        return []

    def apply_licensing(self, file_path: str):
        """Ensures the file has the correct license header (Phase 185)."""
        path = Path(file_path)
        if not path.exists():
            return
            
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = self.core.ensure_license_header(content)
        
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            logging.info(f"AttributionEngine: Applied license header to {file_path}")

    def record_attribution(self, agent_id: str, content: str, task_context: str) -> None:
        """Creates a record of content generation."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        record = {
            "timestamp": time.time(),
            "agent": agent_id,
            "hash": content_hash,
            "task": task_context,
            "metadata": {
                "chars": len(content),
                "words": len(content.split())
            }
        }
        self.records.append(record)
        self._save()

    def _save(self) -> None:
        with open(self.log_file, "w") as f:
            json.dump(self.records, f, indent=2)

    def get_lineage(self, content_hash: str) -> List[Dict[str, Any]]:
        """Retrieves the history of a specific piece of content based on its hash."""
        return [r for r in self.records if r["hash"] == content_hash]

    def get_summary(self) -> Dict[str, Any]:
        """Provides a summary of total attributions."""
        summary = {}
        for r in self.records:
            agent = r["agent"]
            summary[agent] = summary.get(agent, 0) + 1
        return summary
