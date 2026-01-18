import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.getcwd())

from unittest.mock import MagicMock, patch
from src.maintenance.SelfImprovementCoordinator import SelfImprovementCoordinator

def mock_run_subagent(description, prompt, original_content=""):
    print(f"  [MOCK BACKEND] Called with description: {description}")
    
    # If it's a planning prompt from DirectorAgent
    if "generate a step-by-step execution plan" in prompt:
        print("  [MOCK BACKEND] Generating mock project plan...")
        return """
        [
            {"agent": "MarkdownAgent", "file": "docs/AUTO_DOC.md", "prompt": "Create initial automation docs."},
            {"agent": "CoderAgent", "file": "scripts/auto_doc.py", "prompt": "Create a script to automate documentation."}
        ]
        """
    
    # Generic response for other agents
    return f"Mocked result for {description}"

async def main():
    print("--- Starting Self-Improvement Automation Cycle (MOCKED) ---")
    
    # Patch the backend
    with patch("src.infrastructure.backend.run_subagent", side_effect=mock_run_subagent):
        # Initialize coordinator
        coordinator = SelfImprovementCoordinator(os.getcwd())
        
        # 1. Discover improvements
        print("\nStep 1: Scanning improvements.md...")
        ideas = await coordinator.run_discovery_cycle()
        
        # Filter ideas to only include "Documentation Automation" for a clean test
        test_ideas = [i for i in ideas if "Documentation Automation" in i["title"]]
        if not test_ideas:
            print("No 'Documentation Automation' task found. Adding a fake one for testing.")
            test_ideas = [{"title": "Documentation Automation", "status": "PLANNED"}]
        
        print(f"Discovered {len(test_ideas)} relevant ideas.")
        
        # 2. Sync with roadmap
        await coordinator.sync_with_roadmap(test_ideas)
        
        # 3. Generate Action Plan (Triggers Agents)
        print("\nStep 2: Executing Action Plans...")
        await coordinator.generate_action_plan(test_ideas)
        
    print("\n--- Cycle Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
