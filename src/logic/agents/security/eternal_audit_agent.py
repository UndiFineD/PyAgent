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


from __future__ import annotations
from src.core.base.version import VERSION
import logging
import json
import time
import hashlib
import os
from typing import Any
from src.core.base.base_agent import BaseAgent
from src.core.base.base_utilities import as_tool

__version__ = VERSION


class EternalAuditAgent(BaseAgent):
    """
    Agent that maintains an append-only verifiable audit trail of all swarm activities.
    Uses hashing to ensure temporal integrity (simulated blockchain).
    """

    # User requirement: Only record errors, failure, mistakes in general logs
    CRITICAL_ACTIONS = [
        "error",
        "failure",
        "mistake",
        "security_violation",
        "vulnerability_found",
        "exception",
        "unauthorized_access",
        "quota_exceeded",
        "blocklist_hit",
        "safety_violation",
    ]

    def __init__(self, file_path: str, selective_logging: bool = True) -> None:
        super().__init__(file_path)
        self.logs_dir = "data/logs/audit_trail"
        self.selective_logging = selective_logging
        os.makedirs(self.logs_dir, exist_ok=True)
        self.current_shard = os.path.join(self.logs_dir, "current_audit.jsonl")
        self.last_hash = "0" * 64
        self._initialize_last_hash()

    def _initialize_last_hash(self) -> str:
        """Finds the last hash in the audit trail to maintain the chain."""
        if os.path.exists(self.current_shard):
            try:
                with open(self.current_shard, "rb") as f:
                    f.seek(
                        -min(1024, os.path.getsize(self.current_shard)), 2
                    )  # Go to end
                    last_line = f.readlines()[-1].decode("utf-8")
                    last_entry = json.loads(last_line)
                    self.last_hash = last_entry.get("hash", self.last_hash)
            except Exception:
                pass

    @as_tool
    def log_event(self, agent_name: str, action: str, details: dict[str, Any]) -> str:
        """
        Records an event in the verifiable audit trail.
        """
        # Selective pruning: check if action or details contain critical keywords
        is_critical = any(
            kw in action.lower() for kw in self.CRITICAL_ACTIONS
        ) or details.get("severity") in ["HIGH", "CRITICAL"]

        if self.selective_logging and not is_critical:
            return "Event skipped (routine/success)."

        timestamp = time.time()
        payload = {
            "timestamp": timestamp,
            "agent": agent_name,
            "action": action,
            "details": details,
            "previous_hash": self.last_hash,
        }

        # Generate hash for current entry
        payload_str = json.dumps(payload, sort_keys=True)
        current_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        payload["hash"] = current_hash
        self.last_hash = current_hash

        # Write to append-only log
        with open(self.current_shard, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

        # Phase 108: Intelligence Recording
        self._record(
            action,
            json.dumps(details),
            provider="EternalAudit",
            model="AuditTrail",
            meta={"agent": agent_name},
        )

        logging.info(f"AUDIT LOG: {agent_name} -> {action} [{current_hash[:8]}]")
        return f"Event logged and verified. Hash: {current_hash[:16]}"

    @as_tool
    def verify_audit_trail(self) -> dict[str, Any]:
        """
        Verifies the integrity of the audit trail by re-calculating hashes.
        """
        if not os.path.exists(self.current_shard):
            return {"status": "error", "message": "No audit trail found."}

        errors = []
        expected_prev_hash = "0" * 64
        count = 0

        with open(self.current_shard, encoding="utf-8") as f:
            for line in f:
                count += 1
                entry = json.loads(line)
                actual_hash = entry.pop("hash")

                # Check previous hash chain
                if entry.get("previous_hash") != expected_prev_hash:
                    errors.append(
                        f"Line {count}: Chain broken. Expected {expected_prev_hash}, found {entry.get('previous_hash')}"
                    )

                # Verify content hash
                entry_str = json.dumps(entry, sort_keys=True)
                recalculated_hash = hashlib.sha256(
                    entry_str.encode("utf-8")
                ).hexdigest()
                if recalculated_hash != actual_hash:
                    errors.append(f"Line {count}: Hash mismatch.")

                expected_prev_hash = actual_hash

        return {
            "status": "success" if not errors else "tampered",
            "entries_processed": count,
            "errors": errors,
        }
