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
SelfImprovementCoordinator module.

This module defines the SelfImprovementCoordinator class, which automates the monitoring,
parsing, and implementation of improvements, healing, and research synthesis for the PyAgent fleet.
It loads strategic directives from context.txt and prompt.txt, manages cloud and LAN peer discovery,
and coordinates self-healing and research synthesis cycles.
"""
# Copyright 2026 PyAgent Authors
# SelfImprovementCoordinator: Automates the monitoring and implementation of improvements.

import asyncio
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class SelfImprovementCoordinator:
    """
    Monitors improvements.md, roadmap.txt, context.txt, and prompt.txt.
    Automates the monitoring and implementation of improvements and healing.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.prompt_dir: Path = self.workspace_root / "docs" / "prompt"
        self.improvements_file: Path = self.prompt_dir / "improvements.md"
        self.roadmap_file: Path = self.prompt_dir / "roadmap.txt"
        self.context_file: Path = self.prompt_dir / "context.txt"
        self.prompt_file: Path = self.prompt_dir / "prompt.txt"
        self.cloud_policy_file: Path = self.prompt_dir / "cloud_integration.md"
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.directives: Dict[str, Any] = {}

        # Phase 320: LAN Discovery integration
        self.discovery: Optional[Any] = None
        self._init_discovery()

        # Phase 50: Budget & Cloud integration
        from src.infrastructure.services.cloud.budget import BudgetManager

        self.budget = BudgetManager(
            daily_limit=25.0,  # Target from cloud_integration.md
            monthly_limit=250.0,
        )

    def _init_discovery(self) -> None:
        """Initializes LANDiscovery for peer finding."""
        try:
            from src.infrastructure.swarm.network.lan_discovery import \
                LANDiscovery

            secret_key: str | None = os.getenv("PYAGENT_SECRET")
            if not secret_key:
                self.logger.warning("PYAGENT_SECRET not set; LAN discovery disabled for security.")
                return
            self.discovery = LANDiscovery(
                agent_id=f"Coordinator-{os.getpid()}", service_port=8000, secret_key=secret_key
            )
            self.discovery.start()
        except ImportError:
            self.logger.warning("LANDiscovery not available.")

    async def load_strategic_context(self) -> None:
        """Loads and parses context.txt and prompt.txt for strategic directives."""
        self.directives = {
            "fixed_prompts": [],
            "research_links": [],
            "cloud_providers": [],
            "healing_metrics": {},
            "target_peers": [],
        }

        files_to_check: List[Path] = [self.context_file, self.prompt_file]
        for f in files_to_check:
            if f.exists():
                content: str = f.read_text(encoding="utf-8")
                # Extract "fixed prompt" sections
                fixed_prompts: List[Any] = re.findall(r"-\s+(.*?)(?=\n-|\n\n|\n#|$)", content, re.DOTALL)
                self.directives["fixed_prompts"].extend([p.strip().replace("\n", " ") for p in fixed_prompts])

                # Extract arXiv links
                arxiv: List[Any] = re.findall(r"arxiv\.org/(?:abs|list)/[\w\.\/\?=&]+", content)
                self.directives["research_links"].extend(arxiv)
                # Extract potential peers mentioned in context
                peers: List[Any] = re.findall(r"peer:\s*([\w\-]+)", content)
                self.directives["target_peers"].extend(peers)

        self.logger.info(
            f"Strategic context loaded: {len(self.directives['fixed_prompts'])} directives, "
            f"{len(self.directives['target_peers'])} target peers."
        )

    async def discover_external_servers(self) -> List[Dict[str, Any]]:
        """
        Connects with other servers in the local network or internet.
        Uses LANDiscovery, MCPServerRegistry, and ConnectivityManager for discovery.
        """
        all_nodes = []

        # 1. Discover local peers via LANDiscovery
        if self.discovery:
            # Accessing protected member _lock is discouraged; consider exposing via public API in LANDiscovery
            lock = getattr(self.discovery, '_lock', None)
            registry = getattr(self.discovery, 'registry', {})
            if lock is not None:
                with lock:
                    for peer_id, info in registry.items():
                        all_nodes.append(
                            {"id": peer_id, "type": "lan_peer", "ip": info.ip, "port": info.port, "status": "online"}
                        )
            else:
                for peer_id, info in registry.items():
                    all_nodes.append(
                        {"id": peer_id, "type": "lan_peer", "ip": info.ip, "port": info.port, "status": "online"}
                    )

        # 2. Discover registered MCP servers
        try:
            from src.infrastructure.services.mcp.registry import \
                MCPServerRegistry

            registry = MCPServerRegistry()
            for name in registry.servers:
                all_nodes.append(
                    {
                        "id": name,
                        "type": "mcp_server",
                        # Accessing protected member _sessions is discouraged;
                        # consider exposing via public API in MCPServerRegistry
                        "status": (
                            "connected"
                            if hasattr(registry, '_sessions') and name in registry._sessions
                            else "registered"
                        ),
                    }
                )
        except ImportError as e:
            self.logger.debug(f"MCPServerRegistry not available for discovery: {e}")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self.logger.error(f"[Robustness] Error during MCP server discovery from registry: {e}", exc_info=True)

        # 3. Check persistent ConnectivityManager status
        try:
            # Ensure connectivity status is checked from the source
            status_file: Path = self.workspace_root / "data" / "logs" / "connectivity_status.json"
            if status_file.exists():
                try:
                    data = json.loads(status_file.read_text(encoding="utf-8"))
                    for key, val in data.items():
                        is_valid = isinstance(val, dict) and val.get("working")
                        if is_valid and not key.startswith("__"):
                            # Avoid duplicates from LAN/MCP
                            if not any(n["id"] == key for n in all_nodes):
                                all_nodes.append({
                                    "id": key,
                                    "type": "remote_endpoint",
                                    "status": "available"
                                })
                except json.JSONDecodeError as jde:
                    self.logger.warning(f"Failed to parse connectivity_status.json: {jde}")
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    self.logger.error(f"[Robustness] Error with connectivity_status.json: {e}", exc_info=True)
        except ImportError as e:
            self.logger.debug(f"ConnectivityManager not available for status check: {e}")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self.logger.error(f"[Robustness] Unexpected error in discovery block: {e}", exc_info=True)

        self.logger.info(f"Discovery Cycle: Found {len(all_nodes)} total available/connected servers/nodes.")
        return all_nodes

    async def research_synthesis_loop(self) -> None:
        """
        Phase 51: Automated Research Synthesis Loop.
        Workflow: Find -> Summarize -> Map to Logic -> Implement -> Test -> documentation sync.
        """
        self.logger.info("Initiating Phase 51 Research Synthesis Loop...")

        # 1. Identify targets from strategic context
        await self.load_strategic_context()
        topics: List[Any] = [
            p.split(":", 1)[1].strip() for p in self.directives["fixed_prompts"] if p.lower().startswith("research:")
        ]

        if not topics:
            self.logger.info("No explicit research topics found. Checking for general multimodal cues.")
            if any("multimodal" in p.lower() for p in self.directives["fixed_prompts"]):
                topics = ["multimodal ia3 scaling tensorrt"]
            else:
                return

        # 2. Instantiate Director for cross-agent orchestration
        from src.infrastructure.swarm.orchestration.swarm.director_agent import \
            DirectorAgent

        # Use a temporary or the main improvements file
        director = DirectorAgent(str(self.improvements_file))

        for topic in topics:
            self.logger.info(f"Synthesizing research for topic: {topic}")
            goal = (
                f"Research Task: Explore {topic} on Arxiv. "
                "1. Download papers to data/research. "
                "2. Use ArchitecturalDesignAgent to map findings to IA3 and MUX configurations. "
                "3. Delegate implementation to CoderAgent. "
                "4. Update improvements.md with the synthesis results."
            )
            # This triggers the Director's project planning logic
            await director.think(f"Improvement Task: {goal}")

    async def cloud_orchestration_loop(self) -> None:
        """
        Phase 51: Distributed Cloud Coordination.
        Manages task offloading to discovered peers and cloud-hosted MCPServers.
        Integrates with BudgetManager for cost control.
        """
        self.logger.info("Initiating Cloud Orchestration Loop...")

        # 1. Discover nodes
        nodes: List[Dict[str, Any]] = await self.discover_external_servers()
        active_peers: List[Dict[str, Any]] = [n for n in nodes if n["status"] in ["online", "connected", "available"]]

        if not active_peers:
            self.logger.info("No active cloud or LAN peers found for offloading.")
            return

        # 2. Audit Budget
        current_burn = self.budget.get_current_burn()
        if current_burn >= self.budget.daily_limit:
            self.logger.warning(f"Daily cloud budget (${self.budget.daily_limit}) reached. Throttling offloads.")
            return

        # 3. Identify offloadable tasks (Complexity > 0.8)
        self.logger.info(f"Active Fleet: {len(active_peers)} nodes available. Current Burn: ${current_burn:.2f}")
        # In a real scenario, this would pop from a RequestQueue and call execute_remote_task

    async def run_healing_cycle(self) -> dict[str, Any]:
        """
        Phase 317: Automated Self-Healing Trigger.
        Reads health stats and documentation context to trigger repairs.
        """
        from src.infrastructure.swarm.orchestration.healing.self_healing_orchestrator import \
            SelfHealingOrchestrator

        # Initialize orchestrator (which now loads overrides from docs/prompt)
        orchestrator = SelfHealingOrchestrator(None)  # type: ignore

        # 1. Check Project Integrity (Imports/Syntax)
        integrity_report: Dict[str, Any] = orchestrator.check_project_integrity()

        # 2. Check Codebase Health (Technical Debt)
        health_audit: Dict[str, Any] = orchestrator.run_health_audit()

        # 3. Check for failed agents in health registry
        failed_agents: List[str] = []
        if orchestrator.core is not None:
            failed_agents = orchestrator.core.detect_failures()

        results: Dict[str, Any] = {
            "integrity": integrity_report,
            "health": health_audit,
            "failures": failed_agents,
            "actions_taken": [],
        }

        if failed_agents:
            self.logger.warning(f"Self-Healing: {len(failed_agents)} failures detected. Reviewing roadmap items...")
            for agent in failed_agents:
                # Prioritize healing for agents mentioned in the fixed prompts or roadmap
                is_priority = any(agent.lower() in p.lower() for p in self.directives["fixed_prompts"])
                if is_priority:
                    self.logger.info(f"Self-Healing: Priority recovery for {agent}")
                    # orchestrator.attempt_recovery(agent) # Would need fleet_manager
                    results["actions_taken"].append(f"Queued priority recovery for {agent}")

        return results

    async def execute_remote_task(self, task: Dict[str, Any], target_peer: str) -> Dict[str, Any]:
        """
        Dispatches a healing or improvement task to a remote peer.
        This enables 'Distributed computing across local network'.

        Args:
            task: The task to execute.
            target_peer: The peer to execute the task on.

        Returns:
            A dictionary with the result of the remote execution.
        """
        # 1. Check if peer is known and online
        peers: List[Dict[str, Any]] = await self.discover_external_servers()
        target: Dict[str, Any] | None = next((p for p in peers if p.get("id") == target_peer), None)

        valid_statuses: set[str] = {"online", "connected", "available"}
        if not target or target.get("status") not in valid_statuses:
            self.logger.warning(f"execute_remote_task: Peer {target_peer} is offline or unknown.")
            return {"status": "failed", "error": f"Peer {target_peer} is offline or unknown"}

        # 2. Simulate task dispatch (In Phase 51, this uses NixlConnector for KV-warm transfer)
        # For now, we simulate a successful dispatch and acknowledgment.
        self.logger.info(f"Dispatching task to remote peer {target_peer}")
        await asyncio.sleep(0.5)

        return {
            "status": "success",
            "peer": target_peer,
            "task_id": f"rem_{int(time.time())}",
            "result": "Task accepted by remote coordinator",
            "metadata": {"peer_addr": target.get("address")}
        }

    async def run_discovery_cycle(self) -> list[dict[str, str]]:
        """Discovers new improvement ideas from the tracking file."""
        if not self.improvements_file.exists():
            self.logger.error(f"Improvements file not found: {self.improvements_file}")
            return []

        content: str = self.improvements_file.read_text(encoding="utf-8")

        # Simple extraction logic for "High Priority" items
        hp_pattern = r"### High Priority\n(.*?)(?=\n###|\n==)"
        high_priority_section: re.Match[str] | None = re.search(hp_pattern, content, re.DOTALL)
        if not high_priority_section:
            return []

        item_pattern = r"\d+\.\s+\*\*(.*?)\*\*\n\s+-\s+Status:\s+(.*?)\n"
        items: List[Any] = re.findall(item_pattern, high_priority_section.group(1))

        active_ideas = []
        for title, status in items:
            if status.strip() in ["PLANNED", "RESEARCH", "PLANNING"]:
                active_ideas.append({"title": title.strip(), "status": status.strip()})

        return active_ideas

    async def scan_for_research(self) -> List[str]:
        """Scans improvements.md for new research links (arXiv/ScienceDirect)."""
        if not self.improvements_file.exists():
            return []

        content: str = self.improvements_file.read_text(encoding="utf-8")
        # Find arXiv links
        arxiv_links: List[Any] = re.findall(r"arxiv\.org/abs/(\d+\.\d+)", content)
        # Find ScienceDirect PIIs
        sciencedirect_links: List[Any] = re.findall(r"sciencedirect\.com/science/article/pii/(\w+)", content)

        links: List[str] = [f"https://arxiv.org/abs/{link}" for link in arxiv_links]
        links.extend([f"https://www.sciencedirect.com/science/article/pii/{link}" for link in sciencedirect_links])
        return list(set(links))

    async def sync_with_roadmap(self, active_ideas: list[dict[str, Any]]) -> None:
        """Cross-references improvements with the strategic roadmap."""
        if not self.roadmap_file.exists():
            return

        roadmap_content: str = self.roadmap_file.read_text(encoding="utf-8")
        for idea in active_ideas:
            if idea["title"] in roadmap_content:
                idea["on_roadmap"] = True
            else:
                idea["on_roadmap"] = False

    async def generate_action_plan(self, active_ideas: list[dict[str, Any]]) -> None:
        """Simulates triggering implementations for high-priority ideas."""
        for idea in active_ideas:
            print(f"[ACTION] Processing Improvement: {idea['title']} (Status: {idea['status']})")
            await self.trigger_agent_execution(idea)

    async def trigger_agent_execution(self, item: dict[str, Any]) -> None:
        """
        Synaptic Automation: Hands off planned improvements to the Director/Research swarm.
        This connects the monitoring phase to the execution phase.
        """
        title = item["title"]
        status = item["status"]

        try:
            if status == "PLANNED" or status == "PLANNING":
                from src.infrastructure.swarm.orchestration.swarm.director_agent import \
                    DirectorAgent

                self.logger.info(f"Handing off to DirectorAgent: {title}")
                agent = DirectorAgent(str(self.improvements_file))

                # Hand off task to director
                hand_off_prompt = (
                    f"Improvement Task: {title}\nPlease decompose this and delegate to the appropriate specialists."
                )
                director_res = await agent.think(hand_off_prompt)
                print(f"  -> [DIRECTOR RESPONSE] {director_res[:200]}...")

            elif status == "RESEARCH":
                from src.logic.agents.intelligence.research_agent import \
                    ResearchAgent

                self.logger.info(f"Handing off to ResearchAgent: {title}")
                agent = ResearchAgent(str(self.improvements_file))

                # Find associated research links if any
                links: List[str] = await self.scan_for_research()
                research_prompt = f"Research Task: {title}\nRelated links found: {links}"
                research_res = await agent.think(research_prompt)
                print(f"  -> [RESEARCH RESPONSE] {research_res[:200]}...")

        except ImportError as e:
            self.logger.warning(f"  -> [SKIP] Required agent not found: {e}")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self.logger.error(f"  -> [Robustness] Failed to trigger agent: {e}", exc_info=True)


async def main() -> None:
    coordinator = SelfImprovementCoordinator(os.getcwd())
    print("--- Starting Self-Improvement Cycle ---")

    # 1. Discover active ideas
    active_ideas: List[Dict[str, str]] = await coordinator.run_discovery_cycle()
    await coordinator.sync_with_roadmap(active_ideas)

    # 2. Scan for new research
    research_links: List[str] = await coordinator.scan_for_research()
    print(f"[INFO] Found {len(research_links)} research links to monitor.")
    for link in research_links:
        print(f"  -> Monitoring: {link}")

    # 3. Generate action plan
    await coordinator.generate_action_plan(active_ideas)
    print("--- Cycle Complete ---")


if __name__ == "__main__":
    asyncio.run(main())
