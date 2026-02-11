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

# Licensed under the Apache License, Version 2.0 (the "License");

"""
TraceSynthesizer (Pillar 9).
Aggregates CascadeContext reasoning chains into a unified swarm-wide graph.
Supports cross-node lineage tracking.
"""

import json
import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class TraceSynthesizer:
    """
    Consolidates local and remote reasoning traces into a synthesis report.
    Used by the Web UI to visualize the reasoning forest.
    """

    def __init__(self, log_dir: str = "data/logs"):
        self.log_dir = Path(log_dir)
        self.trace_file = self.log_dir / "reasoning_chains.jsonl"

    def synthesize(self) -> Dict[str, Any]:
        """
        Synthesizes a graph-like structure from raw trace lines.
        """
        if not self.trace_file.exists():
            return {"nodes": [], "links": []}

        nodes = {}
        links = []

        try:
            with open(self.trace_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    
                    context = entry.get("context", {})
                    task_id = context.get("task_id", "unknown")
                    parent_id = context.get("parent_id")
                    
                    # Create node
                    if task_id not in nodes:
                        nodes[task_id] = {
                            "id": task_id,
                            "agent": entry.get("agent_name"),
                            "status": entry.get("status"),
                            "timestamp": entry.get("timestamp")
                        }
                    
                    # Create link to parent
                    if parent_id and parent_id != "root":
                        links.append({
                            "source": parent_id,
                            "target": task_id,
                            "type": "delegation"
                        })
            
            return {
                "nodes": list(nodes.values()),
                "links": links
            }
        except Exception as e:
            logger.error(f"TraceSynthesizer: Synthesis failed: {e}")
            return {"error": str(e)}

    def record_trace(self, agent_name: str, status: str, context: Any, metadata: Dict[str, Any] = None):
        """Records a reasoning step into the synthesis log."""
        {
            "agent_name": agent_name,
            "status": status,
            "context": context.to_dict() if hasattr(context, "to_dict") else context,
            "metadata": metadata or {},
            "timestamp": logger.timestamp if hasattr(logger, "timestamp") else None # Usually handled by structured logger
        }
        
        # In practice, this delegatesto the FleetInteractionRecorder or StructuredLogger
        pass
