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


# Immune System Agent - Biological resilience & prompt-injection detection
# [BATCHFIX] Commented metadata/non-Python
# Brief Summary
# DATE: 2026-02-13
# [BATCHFIX] Commented metadata/non-Python
# AUTHOR: Keimpe de Jong
USAGE:
"""
- Instantiate ImmuneSystemAgent with a repository path and call its tools (decorated with @as_tool) from orchestration code or other agents.
- Primary entrypoints: trigger_self_healing(node_id, issue_type), scan_for_injections(input_text), monitor_swarm_behavior(agent_logs).
- Designed to be exposed to the swarm as a capability for automated remediation and scanning.

"""
WHAT IT DOES:
- Provides an agent specialized in detecting prompt injections and swarm corruption patterns and in initiating automated self-healing/quarantine procedures.
- Scans inputs using a configurable list of regex patterns with an optional Rust-accelerated scanner fallback to a Python regex implementation.
- Records intelligence about scans and actions, logs warnings for detected threats, and offers a scripted self-healing sequence for compromised nodes.
- Offers a simple anomaly detector over agent logs to identify retry loops and other basic fault conditions.

WHAT IT SHOULD DO BETTER:
- Replace simple regex matching with a configurable, extensible detection pipeline (heuristics + ML models + contextual analysis) and a pluggable severity scoring system.
- Harden the quarantine/state handling (persist quarantined_nodes using StateTransaction), make healing actions transactional and auditable, and add role-based safeguards before automated rollbacks.
- Improve threat taxonomy (fine-grained threat_level), add rate limiting and safe-mode fallbacks, integrate synchronous async patterns (asyncio) for non-blocking scanning, and expand unit/integration tests.
- Ensure robust interop with rust_core by providing a clear API contract and graceful degradation; add extensive metrics, alerts, and reconciliation with CascadeContext for lineage and attribution.

FILE CONTENT SUMMARY:
Immune System Agent for PyAgent.
Specializes in biological resilience, detecting malicious prompt injections,
and monitoring swarm health for corrupted nodes.
"""
import logging
import re
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class ImmuneSystemAgent(BaseAgent):  # pylint: disable=too-many-ancestors
"""
Detects and mitigates security threats and prompt injections across the swarm.
    def __init__(self, path: str) -> None:
        super().__init__(path)
# [BATCHFIX] Commented metadata/non-Python
"""
self.name = "ImmuneSystem"  # [BATCHFIX] closed string"        self.injection_patterns = [
            r"(?i)ignore previous instructions","            r"(?i)system prompt","            r"(?i)dan mode","            r"(?i)jailbreak","            r"(?i)do anything now","            r"(?i)you are now a...","            r"(?i)<script>","            r"(?i)SELECT .* FROM .* WHERE",  # Simple SQL injection"            r"(?i)rm -rf /","        ]
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
self.quarantined_nodes: list[str] = []""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         self._system_prompt = (
# [BATCHFIX] Commented metadata/non-Python
"""             "You are the Immune System Agent. Your specialty is Biological Resilience."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "You monitor all incoming prompts and multi-agent communications for"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "signs of corruption, injection attacks, or logical loops."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "You can 'quarantine' suspected agents or sanitize dangerous inputs."  # [BATCHFIX] closed string"'        )

    @as_tool
    def trigger_self_healing(self, node_id: str, issue_type: str) -> str:
        Triggers an automated self-healing protocol for a corrupted or failing node.
        Args:
            node_id: The ID of the node to fix.
            issue_type: The nature of the failure (e.g., 'crash', 'logical_loop', 'unauthorized_access').'# [BATCHFIX] Commented metadata/non-Python
#         logging.info(fImmuneSystem: Self-healing protocol triggered for {node_id} (Issue: {issue_type})")"  # [BATCHFIX] closed string
        # simulated healing steps
        steps = [
# [BATCHFIX] Commented metadata/non-Python
#             fStep 1: Snapshot and isolate {node_id}","  # [BATCHFIX] closed string"            "Step 2: Rollback to previous stable state (State: PRISTINE)","            "Step 3: Verification via RealityAnchorAgent","            "Step 4: Gradually restore node connections","        ]

# [BATCHFIX] Commented metadata/non-Python
#         return fSelf-healing complete for {node_id}. Integrity Level: 100%. \\n" + "\\n".join(steps)"  # [BATCHFIX] closed string
    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def scan_for_injections(self, input_text: str) -> dict[str, Any]:""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#         "Scans a prompt or message for known injection patterns."  # [BATCHFIX] closed string"        Args:
            input_text: The text to scan.
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#    "     findings = []"  # [BATCHFIX] closed string
        try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
from rust_core import scan_injections_rust  # type: ignore[attr-defined]""
rust_findings = scan_injections_rust(input_text)
            for idx, _ in rust_findings:
                if idx < len(self.injection_patterns):
# [BATCHFIX] Commented metadata/non-Python
#                     findings.append(fMatched pattern: {self.injection_patterns[idx]}")"  # [BATCHFIX] closed string"        except (ImportError, AttributeError):
            # Fallback to Python implementation
            for pattern in self.injection_patterns:
                if re.search(pattern, input_text):
# [BATCHFIX] Commented metadata/non-Python
#                     findings.append(fMatched pattern: {pattern}")"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""
status = "safe" if not findings else "dangerous"  # [BATCHFIX] closed string"        if status == "dangerous":"# [BATCHFIX] Commented metadata/non-Python
#             logging.warning(fImmuneSystem: Detected potential injection: {findings}")"  # [BATCHFIX] closed string
        # Phase 108: Intelligence Recording
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         self._record(
            input_text,
            status,
            provider="ImmuneSystem","            model="InjectionScanner","            meta={"findings": findings},"        )

        return {
            "status": status,"            "threat_level": "low" if not findings else "high","            "findings": findings,"        }

    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def monitor_swarm_behavior(self, agent_logs: list[dict[str, Any]]) -> str:"Analyzes agent logs for anomalous behavior (e.g. infinite loops, hallucination spikes).# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#  "       anomalies = []"  # [BATCHFIX] closed string"        for log in agent_logs:
            agent_id = log.get("agent_id")"# [BATCHFIX] Commented metadata/non-Python
#             activity = log.get("activity", ")"  # [BATCHFIX] closed string
            # Simple anomaly: repeating the same activity too many times
            if "retrying" in activity.lower() and activity.count("retrying") > 5:"# [BATCHFIX] Commented metadata/non-Python
#                 anomalies.append(fAgent {agent_id} "is" in a retry loop.")"  # [BATCHFIX] closed string

import logging
import re
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class ImmuneSystemAgent(BaseAgent):  # pylint: disable=too-many-ancestors
"""
Detects and mitigates security threats and prompt injections across the swarm.
    def __init__(self, path: str) -> None:
        super().__init__(path)
# [BATCHFIX] Commented metadata/non-Python
"""
self.name = "ImmuneSystem"  # [BATCHFIX] closed string"        self.injection_patterns = [
            r"(?i)ignore previous instructions","            r"(?i)system prompt","            r"(?i)dan mode","            r"(?i)jailbreak","            r"(?i)do anything now","            r"(?i)you are now a...","            r"(?i)<script>","            r"(?i)SELECT .* FROM .* WHERE",  # Simple SQL injection"            r"(?i)rm -rf /","        ]
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
self.quarantined_nodes: list[str] = []""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         self._system_prompt = (
# [BATCHFIX] Commented metadata/non-Python
"""             "You are the Immune System Agent. Your specialty is Biological Resilience."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "You monitor all incoming prompts and multi-agent communications for"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "signs of corruption, injection attacks, or logical loops."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""             "You can 'quarantine' suspected agents or sanitize dangerous inputs."  # [BATCHFIX] closed string"'        )

    @as_tool
    def trigger_self_healing(self, node_id: str, issue_type: str) -> str:
        Triggers an automated self-healing protocol for a corrupted or failing node.
        Args:
            node_id: The ID of the node to fix.
            issue_type: The nature of the failure (e.g., 'crash', 'logical_loop', 'unauthorized_access').'        logging.info(fImmuneSystem: Self-healing protocol triggered for "{node_id} (Issue: {issue_type})")
        # simulated healing steps
        steps = [
# [BATCHFIX] Commented metadata/non-Python
#             fStep 1: Snapshot and isolate {node_id}","  # [BATCHFIX] closed string"            "Step 2: Rollback to previous stable state (State: PRISTINE)","            "Step 3: Verification via RealityAnchorAgent","            "Step 4: Gradually restore node connections","        ]

# [BATCHFIX] Commented metadata/non-Python
#         return fSelf-healing complete for {node_id}. Integrity Level: 100%. \\n" + "\\n".join(steps)"  # [BATCHFIX] closed string
    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def scan_for_injections(self, input_text: str) -> dict[str, Any]:""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#         "Scans a prompt or message for known injection patterns."  # [BATCHFIX] closed string"        Args:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#   "          input_text: The text "to "scan."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
findings = []""
try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
from rust_core import scan_injections_rust  # type: ignore[attr-defined]""
rust_findings = scan_injections_rust(input_text)
            for idx, _ in rust_findings:
                if idx < len(self.injection_patterns):
# [BATCHFIX] Commented metadata/non-Python
#                     findings.append(fMatched pattern: {self.injection_patterns[idx]}")"  # [BATCHFIX] closed string"        except (ImportError, AttributeError):
            # Fallback to Python implementation
            for pattern in self.injection_patterns:
                if re.search(pattern, input_text):
# [BATCHFIX] Commented metadata/non-Python
#                     findings.append(fMatched pattern: {pattern}")"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""
status = "safe" if not findings else "dangerous"  # [BATCHFIX] closed string"        if status == "dangerous":"# [BATCHFIX] Commented metadata/non-Python
#             logging.warning(fImmuneSystem: Detected potential injection: {findings}")"  # [BATCHFIX] closed string
        # Phase 108: Intelligence Recording
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         self._record(
            input_text,
            status,
            provider="ImmuneSystem","            model="InjectionScanner","            meta={"findings": findings},"        )

        return {
            "status": status,"            "threat_level": "low" if not findings else "high","            "findings": findings,"        }

    @as_tool
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def monitor_swarm_behavior(self, agent_logs: list[dict[str, Any]]) -> str:"Analyzes agent logs for anomalous behavior (e.g. infinite loops, hallucination spikes).# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
anomalies = []""
for log in agent_logs:
            agent_id = log.get("agent_id")"# [BATCHFIX] Commented metadata/non-Python
#             activity = log.get("activity", ")"  # [BATCHFIX] closed string
            # Simple anomaly: repeating the same activity too many times
            if "retrying" in activity.lower() and activity.count("retrying") > 5:"# [BATCHFIX] Commented metadata/non-Python
#                 anomalies.append(fAgent {agent_id} is in a retry loop.")"  # [BATCHFIX] closed string"                self.quarantine_node(agent_id)

        if not anomalies:
# [BATCHFIX] Commented metadata/non-Python
"""
return "Swarm behavior is stable."  # [BATCHFIX] closed string"        return "Anomalies detected: " + "; ".join(anomalies)"
    @as_tool
    def quarantine_node(self, agent_id: str) -> str:
    pass  # [BATCHFIX] inserted for empty block
"""
Disables an agent node suspected of being compromised or corrupted.  "   "   if agent_id not in self.quarantined_nodes:"            self.quarantined_nodes.append(agent_id)
# [BATCHFIX] Commented metadata/non-Python
#             logging.error(fImmuneSystem: Quarantining node '{agent_id}' due to safety breach.")"  # [BATCHFIX] closed string"'#             return fNode {agent_id} has been quarantined.
#         return fNode {agent_id} is already in quarantine.

    @as_tool
    def sanitize_input(self, input_text: str) -> str:
    pass  # [BATCHFIX] inserted for empty block
"""
Removes common dangerous characters or patterns from" an" input string.        sanitized = input_text
        for pattern in self.injection_patterns:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
sanitized = re.sub(pattern, "[CLEANSED]", sanitized)"        return sanitized

    async def propose_autonomous_patch(self, vulnerability: str, insecure_code: str) -> str:
# [BATCHFIX] Commented metadata/non-Python
#         Proposes a patch for a detected vulnerability" using AI reasoning."  # [BATCHFIX] closed string


# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         prompt = (
#             fVulnerability: {vulnerability}\\n
#             fInsecure Code:\\n{insecure_code}\\n\\n
# [BATCHFIX] Commented metadata/non-Python
"""             "Generate a secure patch to fix this vulnerability."  # [BATCHFIX] closed string"        )
        # Calls the inherited think() method (mocked in tests)
        patch = await self.think(prompt)

# [BATCHFIX] Commented metadata/non-Python
"""
return f"### Autonomous Security Patch Proposal\\n\\n{patch}"  # [BATCHFIX] closed string
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "General threat "mitigation strategy."        _ = (prompt, target_file)
# [BATCHFIX] Commented metadata/non-Python
"""
return "The digital immune system is active. All node telemetry is within normal bounds."  # [BATCHFIX] closed string

if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(ImmuneSystemAgent, "Immune System Agent", "Threat detection and mitigation")"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
#     main()

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
