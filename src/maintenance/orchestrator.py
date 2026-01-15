import asyncio
import sys
from pathlib import Path
from .utils import GitManager, get_timestamp
from .agents import PytestAgent, MypyAgent, RuffAgent, Flake8Agent, UnittestAgent, ReminderAgent

class MaintenanceOrchestrator:
    def __init__(self):
        self.agents = [
            PytestAgent(),
            MypyAgent(),
            RuffAgent(),
            Flake8Agent(),
            UnittestAgent(),
            ReminderAgent()
        ]

    async def run_maintenance(self):
        print(f"--- Starting Maintenance Workflow {get_timestamp()} ---")
        
        restore_branch, original_branch = GitManager.create_restore_point()
        if not restore_branch:
            print("Failed to create restore branch. Aborting.")
            return

        print(f"Created restore branch: {restore_branch}")
        print(f"Launching {len(self.agents)} agents concurrently...")

        tasks = [agent.perform_maintenance_cycle() for agent in self.agents]
        results = await asyncio.gather(*tasks)

        # Final Evaluation
        success_count = sum(1 for r in results if r)
        total_count = len(self.agents)
        
        print(f"\n--- Maintenance Cycle Complete ---")
        print(f"Successes: {success_count}/{total_count}")
        
        if success_count == total_count:
            print("All agents reported success. Preparing for merge...")
            # GitManager.merge_to_main(restore_branch)
            print(f"To finish, run: git checkout main; git merge {restore_branch}")
        else:
            print(f"Some maintenance tasks failed. Inspect logs in 'fixes/' directory.")
            print(f"Changes were staged in {restore_branch}.")

        # Always return to original branch to avoid "hanging branches"
        print(f"Returning to {original_branch}...")
        GitManager.run_git(["checkout", original_branch])

        # Summary of all proposals for learning
        self.generate_global_summary(results)

    def generate_global_summary(self, results):
        summary_path = Path("fixes/global_summary.md")
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("# Global Maintenance Report\n\n")
            f.write(f"Run Date: {get_timestamp()}\n")
            f.write(f"System State: {'HEALTHY' if all(results) else 'ISSUES REMAIN'}\n\n")
            
            for i, agent in enumerate(self.agents):
                status = "✅ Success" if results[i] else "❌ Failed"
                f.write(f"## {agent.name}: {status}\n")
                f.write(f"Path: {agent.base_path}\n\n")
        
        print(f"Global summary written to {summary_path}")

if __name__ == "__main__":
    orchestrator = MaintenanceOrchestrator()
    asyncio.run(orchestrator.run_maintenance())
