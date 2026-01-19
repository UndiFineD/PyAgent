# Copyright 2026 PyAgent Authors
# SelfImprovementCoordinator: Automates the monitoring and implementation of improvements.

import os
import re
import logging
import asyncio
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

class SelfImprovementCoordinator:
    """
    Monitors improvements.md, roadmap.txt, context.txt, and prompt.txt.
    Automates the monitoring and implementation of improvements and healing.
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.prompt_dir = self.workspace_root / "docs" / "prompt"
        self.improvements_file = self.prompt_dir / "improvements.md"
        self.roadmap_file = self.prompt_dir / "roadmap.txt"
        self.context_file = self.prompt_dir / "context.txt"
        self.prompt_file = self.prompt_dir / "prompt.txt"
        self.cloud_policy_file = self.prompt_dir / "cloud_integration.md"
        self.logger = logging.getLogger(__name__)
        self.directives: Dict[str, Any] = {}
        
        # Phase 320: LAN Discovery integration
        self.discovery: Optional[Any] = None
        self._init_discovery()

        # Phase 50: Budget & Cloud integration
        from src.infrastructure.cloud.budget import BudgetManager
        self.budget = BudgetManager(
            daily_limit=25.0, # Target from cloud_integration.md
            monthly_limit=250.0
        )

    def _init_discovery(self):
        """Initializes LANDiscovery for peer finding."""
        try:
            from src.infrastructure.network.LANDiscovery import LANDiscovery
            secret_key = os.getenv("PYAGENT_SECRET")
            if not secret_key:
                self.logger.warning("PYAGENT_SECRET not set; LAN discovery disabled for security.")
                return
            self.discovery = LANDiscovery(
                agent_id=f"Coordinator-{os.getpid()}",
                service_port=8000,
                secret_key=secret_key
            )
            self.discovery.start()
        except ImportError:
            self.logger.warning("LANDiscovery not available.")
    async def load_strategic_context(self):
        """Loads and parses context.txt and prompt.txt for strategic directives."""
        self.directives = {
            "fixed_prompts": [],
            "research_links": [],
            "cloud_providers": [],
            "healing_metrics": {},
            "target_peers": []
        }

        files_to_check = [self.context_file, self.prompt_file]
        for f in files_to_check:
            if f.exists():
                content = f.read_text(encoding="utf-8")
                # Extract "fixed prompt" sections
                fixed_prompts = re.findall(r"-\s+(.*?)(?=\n-|\n\n|\n#|$)", content, re.DOTALL)
                self.directives["fixed_prompts"].extend([p.strip().replace("\n", " ") for p in fixed_prompts])
                
                # Extract arXiv links
                arxiv = re.findall(r"arxiv\.org/(?:abs|list)/[\w\.\/\?=&]+", content)
                self.directives["research_links"].extend(arxiv)                
                # Extract potential peers mentioned in context
                peers = re.findall(r"peer:\s*([\w\-]+)", content)
                self.directives["target_peers"].extend(peers)

        self.logger.info(f"Strategic context loaded: {len(self.directives['fixed_prompts'])} directives, {len(self.directives['target_peers'])} target peers.")

    async def discover_external_servers(self) -> List[Dict[str, Any]]:
        """
        Connects with other servers in the local network or internet.
        Uses LANDiscovery, MCPServerRegistry, and ConnectivityManager for discovery.
        """
        all_nodes = []
        
        # 1. Discover local peers via LANDiscovery
        if self.discovery:
            with self.discovery._lock:
                for peer_id, info in self.discovery.registry.items():
                    all_nodes.append({
                        "id": peer_id,
                        "type": "lan_peer",
                        "ip": info.ip,
                        "port": info.port,
                        "status": "online"
                    })

        # 2. Discover registered MCP servers
        try:
            from src.infrastructure.mcp_tools.registry import MCPServerRegistry
            registry = MCPServerRegistry()
            for name, server in registry.servers.items():
                all_nodes.append({
                    "id": name,
                    "type": "mcp_server",
                    "status": "connected" if name in registry._sessions else "registered"
                })
        except ImportError as e:
            self.logger.debug(f"MCPServerRegistry not available for discovery: {e}")
        except Exception as e:
            self.logger.error(f"Error during MCP server discovery from registry: {e}", exc_info=True)
            
        # 3. Check persistent ConnectivityManager status
        try:
            from src.core.base.ConnectivityManager import ConnectivityManager
            # Ensure connectivity status is checked from the source
            status_file = self.workspace_root / "data" / "logs" / "connectivity_status.json"
            if status_file.exists():
                try:
                    data = json.loads(status_file.read_text(encoding="utf-8"))
                    for key, val in data.items():
                        if isinstance(val, dict) and val.get("working") and not key.startswith("__"):
                            # Avoid duplicates from LAN/MCP
                            if not any(n["id"] == key for n in all_nodes):
                                all_nodes.append({"id": key, "type": "remote_endpoint", "status": "available"})
                except json.JSONDecodeError as jde:
                    self.logger.warning(f"Failed to parse connectivity_status.json: {jde}")
                except Exception as inner_e:
                    self.logger.error(f"Error reading/processing connectivity_status.json: {inner_e}")
        except ImportError as e:
            self.logger.debug(f"ConnectivityManager not available for status check: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in ConnectivityManager discovery block: {e}", exc_info=True)

        self.logger.info(f"Discovery Cycle: Found {len(all_nodes)} total available/connected servers/nodes.")
        return all_nodes

    async def run_healing_cycle(self):
        """
        Phase 317: Automated Self-Healing Trigger.
        Reads health stats and documentation context to trigger repairs.
        """
        from src.infrastructure.orchestration.healing.SelfHealingOrchestrator import SelfHealingOrchestrator
        from src.infrastructure.orchestration.healing.SelfHealingOrchestrator import SelfHealingOrchestrator
        
        # Initialize orchestrator (which now loads overrides from docs/prompt)
        orchestrator = SelfHealingOrchestrator(None) # type: ignore
        
        # 1. Check Project Integrity (Imports/Syntax)
        integrity_report = orchestrator.check_project_integrity()
        
        # 2. Check Codebase Health (Technical Debt)
        health_audit = orchestrator.run_health_audit()
        
        # 3. Check for failed agents in health registry
        failed_agents = []
        if orchestrator.core is not None:
            failed_agents = orchestrator.core.detect_failures()
            
        results = {
            "integrity": integrity_report,
            "health": health_audit,
            "failures": failed_agents,
            "actions_taken": []
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
        """
        # 1. Check if peer is known and online
        peers = await self.discover_external_servers()
        target = next((p for p in peers if p["id"] == target_peer), None)
        
        valid_statuses = {"online", "connected", "available"}
        if not target or target.get("status") not in valid_statuses:
            return {"status": "failed", "error": f"Peer {target_peer} is offline or unknown"}

        # 2. Simulate task dispatch (Integration with RequestQueue.py / DistributedCoordinator.py)
        # In Phase 51, this would use NixlConnector or MooncakeConnector for KV-warm transfer
        await asyncio.sleep(0.5) 
        
        return {
            "status": "success", 
            "peer": target_peer, 
            "task_id": f"rem_{int(time.time())}",
            "result": "Task accepted by remote coordinator"
        }

    async def run_discovery_cycle(self):
        """Discovers new improvement ideas from the tracking file."""
        if not self.improvements_file.exists():
            self.logger.error(f"Improvements file not found: {self.improvements_file}")
            return []

        content = self.improvements_file.read_text(encoding="utf-8")
        
        # Simple extraction logic for "High Priority" items
        high_priority_section = re.search(r"### High Priority\n(.*?)(?=\n###|\n==)", content, re.DOTALL)
        if not high_priority_section:
            return []

        items = re.findall(r"\d+\.\s+\*\*(.*?)\*\*\n\s+-\s+Status:\s+(.*?)\n", high_priority_section.group(1))
        
        active_ideas = []
        for title, status in items:
            if status.strip() in ["PLANNED", "RESEARCH", "PLANNING"]:
                active_ideas.append({"title": title.strip(), "status": status.strip()})
        
        return active_ideas

    async def scan_for_research(self) -> List[str]:
        """Scans improvements.md for new research links (arXiv/ScienceDirect)."""
        if not self.improvements_file.exists():
            return []
            
        content = self.improvements_file.read_text(encoding="utf-8")
        # Find arXiv links
        arxiv_links = re.findall(r"arxiv\.org/abs/(\d+\.\d+)", content)
        # Find ScienceDirect PIIs
        sciencedirect_links = re.findall(r"sciencedirect\.com/science/article/pii/(\w+)", content)
        
        links = [f"https://arxiv.org/abs/{l}" for l in arxiv_links]
        links.extend([f"https://www.sciencedirect.com/science/article/pii/{l}" for l in sciencedirect_links])
        return list(set(links))

    async def sync_with_roadmap(self, active_ideas: List[Dict[str, Any]]):
        """Cross-references improvements with the strategic roadmap."""
        if not self.roadmap_file.exists():
            return
            
        roadmap_content = self.roadmap_file.read_text(encoding="utf-8")
        for idea in active_ideas:
            if idea["title"] in roadmap_content:
                idea["on_roadmap"] = True
            else:
                idea["on_roadmap"] = False

    async def generate_action_plan(self, active_ideas: List[Dict[str, Any]]):
        """Simulates triggering implementations for high-priority ideas."""
        for idea in active_ideas:
            print(f"[ACTION] Processing Improvement: {idea['title']} (Status: {idea['status']})")
            await self.trigger_agent_execution(idea)

    async def trigger_agent_execution(self, item: Dict[str, Any]):
        """
        Synaptic Automation: Hands off planned improvements to the Director/Research swarm.
        This connects the monitoring phase to the execution phase.
        """
        title = item["title"]
        status = item["status"]
        
        try:
            if status == "PLANNED" or status == "PLANNING":
                from src.infrastructure.orchestration.swarm.DirectorAgent import DirectorAgent
                self.logger.info(f"Handing off to DirectorAgent: {title}")
                agent = DirectorAgent(str(self.improvements_file))
                
                # Hand off task to director
                prompt = f"Improvement Task: {title}\nPlease decompose this and delegate to the appropriate specialists."
                res = await agent.think(prompt)
                print(f"  -> [DIRECTOR RESPONSE] {res[:200]}...")
                
            elif status == "RESEARCH":
                from src.logic.agents.intelligence.ResearchAgent import ResearchAgent
                self.logger.info(f"Handing off to ResearchAgent: {title}")
                agent = ResearchAgent(str(self.improvements_file))
                
                # Find associated research links if any
                links = await self.scan_for_research()
                prompt = f"Research Task: {title}\nRelated links found: {links}"
                res = await agent.think(prompt)
                print(f"  -> [RESEARCH RESPONSE] {res[:200]}...")

        except ImportError as e:
            self.logger.warning(f"  -> [SKIP] Required agent not found: {e}")
        except Exception as e:
            self.logger.error(f"  -> [ERROR] Failed to trigger agent: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

async def main():
    coordinator = SelfImprovementCoordinator(os.getcwd())
    print("--- Starting Self-Improvement Cycle ---")
    
    # 1. Discover active ideas
    active_ideas = await coordinator.run_discovery_cycle()
    await coordinator.sync_with_roadmap(active_ideas)
    
    # 2. Scan for new research
    research_links = await coordinator.scan_for_research()
    print(f"[INFO] Found {len(research_links)} research links to monitor.")
    for link in research_links:
        print(f"  -> Monitoring: {link}")
        
    # 3. Generate action plan
    await coordinator.generate_action_plan(active_ideas)
    print("--- Cycle Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
