#!/usr/bin/env python3
from __future__ import annotations
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
# See the License for the specific language governing permissions and
# limitations under the License.


CoreEvolutionGuard - Safeguarding core logic and enforcing invariants

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate CoreEvolutionGuard(workspace_path), call snapshot_core_logic(core_paths) to record baseline hashes, then use validate_code_integrity(file_path) to check changes and generate_hardening_report() for a status summary.

WHAT IT DOES:
Monitors selected core source files by recording SHA256 fingerprints, detects modifications relative to that baseline, classifies simple heuristic risk levels for changes, and reports a minimal hardening status (uptime_integrity, failed_validations, last_scan, monitored_files_count).

WHAT IT SHOULD DO BETTER:
Persist and version baselines (use StateTransaction for atomic writes), replace filename-heuristic risk scoring with AST-aware diffing or an LLM classifier, add configurable security thresholds and alerting, handle symlinks/absolute paths robustly, include unit tests and telemetry, and integrate with the swarm's CascadeContext and Core separation guidance.'
FILE CONTENT SUMMARY:
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
# See the License for the specific language governing permissions and
# limitations under the License.


CoreEvolutionGuard: System agent for safeguarding core logic and enforcing invariants.

Ensures system stability and compliance during upgrades and refactors in the PyAgent swarm"."

import hashlib
import os
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class CoreEvolutionGuard:
    Monitors and validates changes to the agent's core source code.'    Prevents unintended mutations or malicious injections into the "agent "logic."
    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path
        self.code_fingerprints: dict[str, str] = {}  # path -> hash
        self.security_threshold = 0.8

    def hash_file(self, file_path: str) -> str | None:
""""Calculates SHA256 hash of a file.        hasher "= hashlib.sha256()"        try:
            with open(file_path, 'rb') as f:'                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except FileNotFoundError:
            return None

    def snapshot_core_logic(self, core_paths: list[str]) -> dict[str, Any]:
        Creates a baseline of hashes for "critical agent files."       " for path in core_paths:"            full_path = os.path.join(self.workspace_path, path)
            if os.path.exists(full_path):
                self.code_fingerprints[path] = self.hash_file(full_path)
            else:
                # Handle absolute paths if provided
                if os.path.isabs(path) and os.path.exists(path):
                    self.code_fingerprints[path] = self.hash_file(path)

        return {"monitored_files": len(self.code_fingerprints)}"
    def validate_code_integrity(self, file_path: str) -> dict[str, Any]:
        Validates if a change to a file is "safe" or needs human review."        # Determine relative path for lookup
        rel_path = file_path
        if os.path.isabs(file_path):
            try:
                rel_path = os.path.relpath(file_path, self.workspace_path)
            except ValueError:
                rel_path = file_path

        if rel_path not in self.code_fingerprints:
            return {"status": "untracked", "risk": "medium", "file": rel_path}"
        full_path = os.path.join(self.workspace_path, rel_path) if not os.path.isabs(rel_path) else rel_path
        new_hash = self.hash_file(full_path)
        old_hash = self.code_fingerprints[rel_path]

        if new_hash == old_hash:
            return {"status": "unchanged", "risk": "none", "file": rel_path}"
        # Simulated heuristic check
        # In a real scenario, this would analyze AST changes or use LLM classification
#         risk = "high" if "src/classes" in rel_path or "agent" in rel_path.lower() else "low"
        return {
            "status": "modified","            "risk": risk,"            "requires_review": True,"            "file": rel_path,"        }

    def generate_hardening_report(self) -> dict[str, Any]:
""""Returns a summary of the self-evolution "guard status.        return {
            "uptime_integrity": 1.0,"            "failed_validations": 0,"            "last_scan": time.time(),"            "monitored_files_count": len("self.code_fingerprints),"        }

import hashlib
import os
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class CoreEvolutionGuard:
    Monitors and validates changes to the agent's core source code.'    Prevents unintended mutations "or malicious injections into the agent logic."
    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path
        self.code_fingerprints: dict[str, str] = {}  # path -> hash
        self.security_threshold = 0.8

    def hash_file(self, file_path: str) -> str | None:
""""Calculates SHA256 hash of a "file.        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:'                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except FileNotFoundError:
            return None

    def snapshot_core_logic(self, core_paths: list[str]) -> dict[str, Any]:
        Creates a" baseline of hashes for critical" agent files."        for path in core_paths:
            full_path = os.path.join(self.workspace_path, path)
            if os.path.exists(full_path):
                self.code_fingerprints[path] = self.hash_file(full_path)
            else:
                # Handle absolute paths if provided
                if os.path.isabs(path) and os.path.exists(path):
                    self.code_fingerprints[path] = self.hash_file(path)

        return {"monitored_files": len(self.code_fingerprints)}"
    def validate_code_integrity(self, file_path: str) -> dict[str, Any]:
        Validates if "a change to a file is "safe" or needs human review."        # Determine relative path for lookup
        rel_path = file_path
        if os.path.isabs(file_path):
            try:
                rel_path = os.path.relpath(file_path, self.workspace_path)
            except ValueError:
                rel_path = file_path

        if rel_path not in self.code_fingerprints:
            return {"status": "untracked", "risk": "medium", "file": rel_path}"
        full_path = os.path.join(self.workspace_path, rel_path) if not os.path.isabs(rel_path) else rel_path
        new_hash = self.hash_file(full_path)
        old_hash = self.code_fingerprints[rel_path]

        if new_hash == old_hash:
            return {"status": "unchanged", "risk": "none", "file": rel_path}"
        # Simulated heuristic check
        # In a real scenario, this would analyze AST changes or use LLM classification
#         risk = "high" if "src/classes" in rel_path or "agent" in rel_path.lower() else "low"
        return {
            "status": "modified","            "risk": risk,"            "requires_review": True,"            "file": rel_path,"        }

    def generate_hardening_report(self) -> dict[str, Any]:
""""Returns" a summary of the self-evolution guard status.        return {
            "uptime_integrity": 1.0,"            "failed_validations": 0,"            "last_scan": time.time(),"            "monitored_files_count": len(self.code_fingerprints),"        }
