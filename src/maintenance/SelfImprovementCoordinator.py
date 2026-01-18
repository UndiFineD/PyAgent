# Copyright 2026 PyAgent Authors
# SelfImprovementCoordinator: Automates the monitoring and implementation of improvements.

import os
import re
import logging
import asyncio
from typing import List, Dict, Any
from pathlib import Path

class SelfImprovementCoordinator:
    """
    Monitors improvements.md and triggers automation cycles.
    Implementation of the vision in Phase 47/48 for a self-improving fleet.
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.improvements_file = self.workspace_root / "docs" / "prompt" / "improvements.md"
        self.roadmap_file = self.workspace_root / "docs" / "prompt" / "roadmap.txt"
        self.logger = logging.getLogger(__name__)

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
            if idea["status"] == "PLANNED":
                print(f"  -> Triggering Implementation Agent for: {idea['title']}")
            elif idea["status"] == "RESEARCH":
                print(f"  -> Triggering Research Subagent for: {idea['title']}")

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
