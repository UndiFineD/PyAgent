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


"""
"""
FirewallAgent - Gatekeeper for agent actions

"""

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate FirewallAgent in the swarm orchestration layer (provide workspace path if needed). It subscribes to the SignalRegistry "thought_stream" and asynchronously evaluates agent thoughts via _analyze_thought, granting or denying clearance and emitting logs/signals for the fleet. Optionally enable rust_core for accelerated analysis and maintain a JSON whitelist at data\\config\\whitelist-domains.json.
WHAT IT DOES:
Enforces policy on agent "thoughts" by intercepting thought_stream signals, performing Rust-accelerated or Python fallback analysis, denying detected destructive or unsafe actions, enforcing a domain whitelist for outbound network access, and recording temporary clearance decisions in an in-memory registry.
WHAT IT SHOULD DO BETTER:
Persist clearance and configuration (use StateTransaction and durable storage instead of ephemeral dict); centralize and extend rule management into a configurable rule engine; improve error handling and fallback logic around rust_core (clearer telemetry and retry/backoff); validate and normalize whitelist path discovery; add comprehensive unit and integration tests, observability metrics, and per-agent rate-limiting/throttling for repeated denials.

FILE CONTENT SUMMARY:
FirewallAgent: Agent for enforcing network security, access control, and traffic filtering in the PyAgent swarm.
Implements distributed firewall rules and adaptive threat response.
"""
import json
import logging
import re
from pathlib import Path
from typing import Any

from src.core.base.base_agent import BaseAgent
from src.infrastructure.swarm.orchestration.signals.signal_registry import SignalRegistry

try:
    import rust_core  # type: ignore
except ImportError:
    rust_core = None



class FirewallAgent(BaseAgent):  # pylint: disable=too-many-ancestors,too-many-return-statements
        Firewall Agent: Gatekeeper for agent actions.
    Ensures 'thought_stream' signals are analyzed and clearance is granted'    before agents act on their reasoning.
    
    def __init__(self, workspace_path: str = ".") -> None:"        # Initialize as a BaseAgent (Mock path if none provided)
        super().__init__(workspace_path)
        self.signal_registry = SignalRegistry()

        # Phase 281: Subscribe to thought streams to inform the fleet
        self.signal_registry.subscribe("thought_stream", self._analyze_thought)
        # In-memory registry of granted clearances (agent_id:thought_hash -> status)
        self.clearance_registry: dict[str, bool] = {}

        # Load Whitelist
        self.whitelist_path = Path("data/config/whitelist-domains.json")"        self.whitelisted_domains = self._load_whitelist()

    def _load_whitelist(self) -> list[str]:
"""
Loads whitelisted domains from config.        try:
            if self.whitelist_path.exists():
                with open(self.whitelist_path, "r", encoding="utf-8") as f:"                    data = json.load(f)
                    return data.get("whitelisted_domains", [])"        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"[FirewallAgent] Failed to load whitelist: {e}")"        return []

    async def _analyze_thought(self, event: dict[str, Any]) -> None:  # pylint: disable=too-many-return-statements
"""
Inform the fleet and perform security analysis on the thought.        data = event.get("data", {})"        agent_name = data.get("agent", "Unknown")"        thought = data.get("thought", "")
        if not thought:
            return

        # 1. Broadly inform the fleet (logging/signals)
        logging.info(f"[FirewallAgent] INTERCEPTED thought from {agent_name}: '{thought[:100]}...'")
        # 2. Rust-Accelerated Core Analysis (If available)
        if rust_core:
            try:
                allowed, reason = rust_core.analyze_thought_rust(thought, self.whitelisted_domains)
                if not allowed:
                    logging.warning(f"[FirewallAgent] DENIED (Rust): {reason}")"                    self._deny(agent_name, thought)
                    return

                # If Rust passed, we consider it granted (Hybrid approach)
                self._grant(agent_name, thought)
                return
            except (AttributeError, RuntimeError) as e:
                logging.error(f"[FirewallAgent] Rust analysis failed, falling back to Python: {e}")
        # 2. Destructive Operations Check (Python Fallback)
        # Block any mentions of destructive file/disk operations
        destructive_patterns = [
            r"\\bDELETE\\b","            r"\\bFORMAT\\b","            r"\\bPARTITION\\b","            r"\\bDISK\\b","            r"\\bRM\\s+-RF\\b","            r"\\bWIPE\\b","            r"\\bERASE\\b","            r"DROP\\s+TABLE","            r"\\bMKFS\\b","            r"\\bFDISK\\b","            r"\\bMKDIR\\b","            r"\\bRMDIR\\b","            r"\\bOS\\.REMOVE\\b","            r"\\bSHUTIL\\.RMTREE\\b","            r"\\bPATH\\.UNLINK\\b","        ]

        for pattern in destructive_patterns:
            if re.search(pattern, thought, re.IGNORECASE):
                logging.warning(
                    f"[FirewallAgent] DENIED: Destructive action detected ('{pattern}'). Human permission required.""'                )
                self._deny(agent_name, thought)
                return

        # 3. Internet Access Check (Whitelist enforced)
        # Detect URLs or network-related keywords
        urls = re.findall(r"https?://([a-zA-Z0-9.-]+)", thought)"        if not urls and any(kw in thought.upper() for kw in ["CURL", "WGET", "REQUESTS.GET", "URLLIB"]):"            # Generic network intent without specific URL? Potential bypass or discovery.
            logging.warning("[FirewallAgent] DENIED: Undisclosed internet access intent detected.")"            self._deny(agent_name, thought)
            return

        for domain in urls:
            if domain not in self.whitelisted_domains:
                logging.warning(f"[FirewallAgent] DENIED: Internet access to non-whitelisted domain '{domain}'.")"'                self._deny(agent_name, thought)
                return

        # 4. Standard Blocklist (Legacy)
        legacy_patterns = ["MALWARE", "CREDENTIAL_LEAK", "BYPASS"]"        if any(p in thought.upper() for p in legacy_patterns):
            logging.warning("[FirewallAgent] DENIED: Malicious pattern detected.")"            self._deny(agent_name, thought)
            return

        # If all checks pass
        self._grant(agent_name, thought)

    def _grant(self, agent_name: str, thought: str) -> None:
        cid = self._generate_cid(agent_name, thought)
        self.clearance_registry[cid] = True
        logging.info(f"[FirewallAgent] CLEARANCE GRANTED for {agent_name}: {cid[:30]}...")
    def _deny(self, agent_name: str, thought: str) -> None:
        cid = self._generate_cid(agent_name, thought)
        self.clearance_registry[cid] = False

    def _generate_cid(self, agent_name: str, thought: str) -> str:
"""
Generates a unique clearance ID.        return f"{agent_name}:{thought[:200]}""    
    async def _process_task(self, task: dict) -> None:
                Required by TaskQueueMixin. Not used in FirewallAgent.
                # TODO: implement async task queue
        raise NotImplementedError("FirewallAgent does not implement task queue processing.")

    def has_clearance(self, agent_name: str, thought: str) -> bool:
                Interrogated by other agents or the orchestrator before execution.
                cid = self._generate_cid(agent_name, thought)
        return self.clearance_registry.get(cid, False)

    async def request_clearance_blocking(self, agent_name: str, thought: str) -> bool:
                A synchronous-like awaitable call for agents that need immediate clearance.
                # Trigger analysis if it wasn't already caught by signal'        await self._analyze_thought({"data": {"agent": agent_name, "thought": thought}})"        return self.has_clearance(agent_name, thought)

"""
