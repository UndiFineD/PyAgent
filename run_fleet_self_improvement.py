
import os
import sys
import json
import time
from pathlib import Path

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.classes.fleet.FleetManager import FleetManager

def main():
    root = os.getcwd()
    fleet = FleetManager(root)
    
    print("=== SWARM SELF-IMPROVEMENT CYCLE INITIATED ===")
    print(f"Scanning workspace: {root}")
    
    # 1. Run the improvement cycle (Quality, Security, Tech Debt)
    # We'll focus on the 'src' directory where the core logic resides
    stats = fleet.self_improvement.run_improvement_cycle(target_dir="src")
    
    print(f"\nScan complete:")
    print(f" - Files Scanned: {stats['files_scanned']}")
    print(f" - Issues Found: {stats['issues_found']}")
    print(f" - Autonomous Fixes Applied: {stats['fixes_applied']}")
    
    # 2. Log what is 'broken' (issues not fixed)
    broken_items = []
    for detail in stats['details']:
        unfixed = [i for i in detail['issues'] if not i.get('fixed')]
        if unfixed:
            broken_items.append({"file": detail['file'], "remaining_issues": unfixed})
    
    if broken_items:
        print("\n--- Remaining Technical Debt / Issues ---")
        for item in broken_items:
            print(f"File: {item['file']}")
            for issue in item['remaining_issues']:
                issue_type = issue.get('type') or issue.get('message', 'Unknown Issue')
                print(f"  - [ ] {issue_type}: {issue.get('detail') or issue.get('message', '')}")
    else:
        print("\nAll scanned issues have been autonomously addressed.")

    # 3. Documentation & Research Summary (Phase 112)
    print("\n[Research] Summarizing codebase intelligence...")
    library_path = os.path.join(root, "knowledge_exports", "research_library.json")
    if os.path.exists(library_path):
        with open(library_path, "r") as f:
            library = json.load(f)
        print(f" - Fleet Intelligence Library contains {len(library)} indexed agents.")
        
        # Performance/Complexity check
        high_comp = [e for e in library if e.get("taxonomy", {}).get("logic_complexity") == "High"]
        if high_comp:
            print(f" - WARNING: {len(high_comp)} files identified with HIGH logic complexity.")
            for e in high_comp[:3]:
                print(f"    * {e['title']}")

    print("\n[Documentation] Generating updated docs for improvements...")
    doc_res = fleet.doc_gen_agent.extract_docs(os.path.join(root, "src/classes/fleet/FleetManager.py"))
    doc_path = os.path.join(root, "docs/FLEET_AUTO_DOC.md")
    # Using 'a' to preserve maintenance summary if it exists, or handling intelligently
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write("# Swarm Auto-Generated Documentation\n\n")
        f.write(doc_res)
    
    # Re-trigger maintenance log if it was overwritten
    maintenance_summary = f"\n## {time.strftime('%Y-%m-%d')} - Maintenance Cycle Summary\n"
    maintenance_summary += f"The fleet's SelfImprovementOrchestrator completed a cycle over {stats['files_scanned']} files. Re-stabilization phase engaged.\n"
    with open(doc_path, "a", encoding="utf-8") as f:
        f.write(maintenance_summary)
        
    print(f" - Updated documentation logged to {doc_path}")

    # 4. Explainability Log
    workflow_id = "self_improvement_01"
    fleet.explainability.log_reasoning_step(
        workflow_id, "SelfImprovementOrchestrator", "run_improvement_cycle",
        "Autonomous fleet optimization maintains system health and security parity.",
        {"stats": stats}
    )
    print(f"\nReasoning for this cycle logged to Explainability trace.")

    # 5. Smart AI Recording Verification (Phase 107)
    print("\n[Intelligence] Verifying local interaction recording...")
    # Simulated internal AI thought to be recorded
    test_prompt = "How can we optimize for a trillion parameters?"
    test_result = "By using compressed sharding and adler32 hashing for high-speed indexing."
    fleet.recorder.record_interaction("internal_fleet_optimizer", "logic-v1", test_prompt, test_result)
    print(" - Interaction archived to compressed local shard.")
    
    print("\n=== CYCLE COMPLETE ===")

if __name__ == "__main__":
    main()
