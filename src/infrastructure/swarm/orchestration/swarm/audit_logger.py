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

<<<<<<< HEAD
<<<<<<< HEAD
import json
import logging
import os
import time
from typing import Any, Dict, List

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import logging
import json
import time
import os
from typing import List, Dict, Any, Optional
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from src.core.base.common.models.communication_models import SwarmAuditTrail

logger = logging.getLogger(__name__)

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class SwarmAuditLogger:
    """
    Centralized logger for swarm consensus and routing decisions.
    Allows for post-hoc analysis of agent fleet behavior.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, storage_path: str = "data/logs/swarm_audit.jsonl", log_to_file: bool = True) -> None:
        self.trails: Dict[str, List[SwarmAuditTrail]] = {}
        self.storage_path = storage_path
        self.log_to_file = log_to_file

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    
    def __init__(self, storage_path: str = "data/logs/swarm_audit.jsonl", log_to_file: bool = True):
        self.trails: Dict[str, List[SwarmAuditTrail]] = {}
        self.storage_path = storage_path
        self.log_to_file = log_to_file
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Ensure directory exists
        if self.log_to_file:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

<<<<<<< HEAD
<<<<<<< HEAD
    def log_event(
        self, task_id: str, event_type: str, description: str, data: Dict[str, Any], duration_ms: float = 0.0
    ):
=======
    def log_event(self, task_id: str, event_type: str, description: str, data: Dict[str, Any], duration_ms: float = 0.0):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def log_event(self, task_id: str, event_type: str, description: str, data: Dict[str, Any], duration_ms: float = 0.0):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Records a specific step in a swarm task."""
        trail = SwarmAuditTrail(
            request_id=task_id,
            step=event_type,
            decision_summary=description,
            raw_data=data,
            timestamp=time.time(),
<<<<<<< HEAD
<<<<<<< HEAD
            duration_ms=duration_ms,
        )

        if task_id not in self.trails:
            self.trails[task_id] = []
        self.trails[task_id].append(trail)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            duration_ms=duration_ms
        )
        
        if task_id not in self.trails:
            self.trails[task_id] = []
        self.trails[task_id].append(trail)
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if self.log_to_file:
            self._persist_event(trail)

    def _persist_event(self, event: SwarmAuditTrail):
        """Appends a single audit event to the JSONL log file."""
        try:
<<<<<<< HEAD
<<<<<<< HEAD
            with open(self.storage_path, 'a', encoding='utf-8') as f:
                f.write(
                    json.dumps(
                        {
                            "task_id": event.request_id,
                            "event_type": event.step,
                            "description": event.decision_summary,
                            "data": event.raw_data,
                            "timestamp": event.timestamp,
                            "duration_ms": event.duration_ms,
                        }
                    )
                    + "\n"
                )
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            logger.error(f"Failed to persist audit event: {e}")

    def get_trail(self, task_id: str) -> List[SwarmAuditTrail]:
        """Retrieves the full decision trail for a specific task."""
        return self.trails.get(task_id, [])
