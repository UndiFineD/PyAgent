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
Swarm Audit Service (Phase 69).
Captures and persists decision-making trails for the MoE Swarm.
"""

import logging
import json
import time
import os
from typing import List, Dict, Any, Optional
from src.core.base.common.models.communication_models import SwarmAuditTrail

logger = logging.getLogger(__name__)

class SwarmAuditLogger:
    """
    Centralized logger for swarm consensus and routing decisions.
    Allows for post-hoc analysis of agent fleet behavior.
    """
    
    def __init__(self, storage_path: str = "data/logs/swarm_audit.jsonl", log_to_file: bool = True):
        self.trails: Dict[str, List[SwarmAuditTrail]] = {}
        self.storage_path = storage_path
        self.log_to_file = log_to_file
        
        # Ensure directory exists
        if self.log_to_file:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def log_event(self, task_id: str, event_type: str, description: str, data: Dict[str, Any], duration_ms: float = 0.0):
        """Records a specific step in a swarm task."""
        trail = SwarmAuditTrail(
            request_id=task_id,
            step=event_type,
            decision_summary=description,
            raw_data=data,
            timestamp=time.time(),
            duration_ms=duration_ms
        )
        
        if task_id not in self.trails:
            self.trails[task_id] = []
        self.trails[task_id].append(trail)
        
        if self.log_to_file:
            self._persist_event(trail)

    def _persist_event(self, event: SwarmAuditTrail):
        """Appends a single audit event to the JSONL log file."""
        try:
            with open(self.storage_path, "a") as f:
                f.write(json.dumps({
                    "task_id": event.request_id,
                    "event_type": event.step,
                    "description": event.decision_summary,
                    "data": event.raw_data,
                    "timestamp": event.timestamp,
                    "duration_ms": event.duration_ms
                }) + "\n")
        except Exception as e:
            logger.error(f"Failed to persist audit event: {e}")

    def get_trail(self, task_id: str) -> List[SwarmAuditTrail]:
        """Retrieves the full decision trail for a specific task."""
        return self.trails.get(task_id, [])
