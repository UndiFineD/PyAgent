#!/usr/bin/env python3

"""Attribution Engine for PyAgent.
Tracks the lineage and provenance of every generated piece of content or code.
"""

from __future__ import annotations

import hashlib
import time
import json
from pathlib import Path
from typing import Dict, List, Any

class AttributionEngine:
    """Records the 'who, when, and how' for all system outputs."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.log_file = self.workspace_root / "attribution_log.json"
        self.records: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if self.log_file.exists():
            with open(self.log_file, "r") as f:
                return json.load(f)
        return []

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
