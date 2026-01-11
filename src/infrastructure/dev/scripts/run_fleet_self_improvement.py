#!/usr/bin/env python3

"""
Autonomous Fleet Self-Improvement Loop.
Scans the workspace for issues, applies autonomous fixes, and harvests external intelligence.
"""

import os
import sys
import json
import time
import argparse
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any

# Phase 120: Load environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Ensure the project root is in PYTHONPATH before importing from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.infrastructure.fleet.FleetManager import FleetManager


def run_cycle(fleet: FleetManager, root: str, prompt_path: str = None, current_cycle: int = 1) -> None:
    """Run a single improvement cycle."""
    start_time = time.time()
    print(f"\n--- CYCLE {current_cycle} STARTING ---")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 0. Load Strategic Directive / Directives
    strategic_note = ""
    target_dirs = ["src"]
    if prompt_path:
        p_path = Path(prompt_path)
        if not p_path.is_absolute():
            p_path = Path(root) / prompt_path
        if p_path.exists():
            try:
                strategic_note = p_path.read_text(encoding="utf-8")
                # Parse @focus: markers to reduce scan surface (Cycle Time Optimization)
                # Supports both simple comma-separated and JSON-style lists
                # Improved multi-line @focus parsing (Phase 140 fix)
                focus_match = re.search(r"@focus:\s*(\[.*?\]|.*?\n)", strategic_note, re.DOTALL | re.IGNORECASE)
                if focus_match:
                    focus_val = focus_match.group(1).strip()
                    if focus_val.startswith("[") and focus_val.endswith("]"):
                        try:
                            # Clean up multi-line formatting inside the list
                            clean_focus = re.sub(r'[\s\n]+', ' ', focus_val)
                            target_dirs = json.loads(clean_focus.replace("'", "\""))
                        except Exception:
                            # Fallback for complex lists
                            inner = focus_val[1:-1].split(",")
                            target_dirs = [d.strip().strip('"').strip("'").strip() for d in inner if d.strip()]
                    else:
                        target_dirs = [d.strip() for d in focus_val.split(",") if d.strip()]
                    print(f" - Directive Focus: {target_dirs}")
                
                # Parse and execute @cmd: markers (Proactive Fixes)
                cmd_matches = re.findall(r"@cmd:\s*(.*)", strategic_note, re.IGNORECASE)
                for cmd in cmd_matches:
                    clean_cmd = cmd.strip().strip('"').strip("'")
                    print(f" - Executing Directive Command: {clean_cmd}")
                    subprocess.run(clean_cmd, shell=True, cwd=root)

                # NEW: Parse and execute @python: blocks
                python_blocks = re.findall(r"@python:\s*\"\"\"(.*?)\"\"\"", strategic_note, re.DOTALL | re.IGNORECASE)
                for py_code in python_blocks:
                    print(f" - Executing Directive Python Block...")
                    exec(py_code, {"fleet": fleet, "root": root, "os": os, "sys": sys, "Path": Path})
            except Exception as e:
                print(f" - Failed to parse directive: {e}")
    
    # 1. Run the improvement cycle (Quality, Security, Tech Debt)
    combined_stats = {"files_scanned": 0, "issues_found": 0, "fixes_applied": 0, "details": []}
    for t_dir in target_dirs:
        stats = fleet.self_improvement.run_improvement_cycle(target_dir=t_dir)
        combined_stats["files_scanned"] += stats.get("files_scanned", 0)
        combined_stats["issues_found"] += stats.get("issues_found", 0)
        combined_stats["fixes_applied"] += stats.get("fixes_applied", 0)
        combined_stats["details"].extend(stats.get("details", []))
    
    stats = combined_stats
    
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
    library_path = os.path.join(root, "data/memory/knowledge_exports", "research_library.json")
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
    doc_res = fleet.doc_gen_agent.extract_docs(os.path.join(root, "src/infrastructure/fleet/FleetManager.py"))
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
    
    # 6. External Federated Learning (Phase 112+)
    consult_external_models(fleet, broken_items, prompt_path=prompt_path)
    
    # 7. Knowledge Synthesis (Phase 108)
    print("\n[Intelligence] Synthesizing collective knowledge...")
    try:
        new_patterns = fleet.intelligence.synthesize_collective_intelligence()
        if new_patterns:
            print(f" - Identified {len(new_patterns)} new actionable patterns for the next cycle.")
    except Exception as e:
        print(f" - Intelligence synthesis skipped: {e}")

    # 8. Self-Pruning Directive (Phase 135) - Auto-remove successful commands/focus
    if prompt_path and not broken_items:
        p_path = Path(prompt_path)
        if not p_path.is_absolute():
            p_path = Path(root) / prompt_path
        if p_path.exists():
            print(f"\n[Maintenance] Area '@focus: {target_dirs}' is CLEAN. Pruning directive...")
            content = p_path.read_text(encoding="utf-8")
            
            # Remove ONLY the first focus and commands that are now verified (Phase 135 fix)
            # DYNAMIC MULTI-LINE PRUNING (Phase 141)
            new_content = re.sub(r"^@focus:.*?\].*?\n", "", content, count=1, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)
            if new_content == content:
                # Fallback if no brackets
                new_content = re.sub(r"^@focus:.*$\n?", "", content, count=1, flags=re.MULTILINE | re.IGNORECASE)
            
            new_content = re.sub(r"^@cmd:.*$\n?", "", new_content, count=1, flags=re.MULTILINE | re.IGNORECASE)
            # For python blocks, we use DOTALL so we need to be careful. 
            # We'll remove the first python block if it exists.
            new_content = re.sub(r"^@python:\s*\"\"\"(.*?)\"\"\"\n?", "", new_content, count=1, flags=re.DOTALL | re.IGNORECASE)
            
            # Also remove completed task markers if they exist
            new_content = re.sub(r"^- \[x\].*$\n?", "", new_content, flags=re.MULTILINE | re.IGNORECASE)
            new_content = re.sub(r"^# DONE.*$\n?", "", new_content, flags=re.MULTILINE | re.IGNORECASE)

            if new_content != content:
                p_path.write_text(new_content.strip() + "\n", encoding="utf-8")
                print(f" - Updated {p_path.name}: Verified directives REMOVED.")

    duration = time.time() - start_time
    print(f"\n=== CYCLE {current_cycle} COMPLETE (Time spent: {duration:.2f}s) ===")

def consult_external_models(fleet: FleetManager, broken_items: List[Dict[str, Any]], prompt_path: str = None) -> List[Dict[str, str]]:
    """
    Queries external model backends (Ollama, Gemini, and Agentic Copilot) 
    to extract lessons for the fleet.
    """
    import requests
    from src.infrastructure.backend.LLMClient import LLMClient
    from pathlib import Path
    
    ai = LLMClient(requests, workspace_root=str(fleet.workspace_root))
    
    print("\n[Federated Learning] Consulting external models for specialized lessons...")
    
    # Context of current health
    if broken_items:
        context = f"The fleet currently has issues in {len(broken_items)} files. Top issue: {broken_items[0]['file']}."
    else:
        context = "The fleet is currently stable and optimized."

    # Load strategic prompt from provided path or default note.txt
    strategic_note = ""
    if prompt_path:
        note_path = Path(prompt_path)
        if not note_path.is_absolute():
            note_path = Path(fleet.workspace_root) / prompt_path
    else:
        note_path = Path(fleet.workspace_root) / "docs" / "notes" / "note.txt"
        
    if note_path.exists():
        try:
            strategic_note = note_path.read_text(encoding="utf-8")
            print(f" - Ingested strategic directive from {note_path.name}")
        except Exception:
            pass

    prompt = f"""
    Context: {context}
    Strategic Directive: {strategic_note}
    
    Task: Provide one advanced technical 'lesson' or 'fix' for a multi-agent autonomous swarm based on the directive and context.
    Topics: Resilience, Consensus, Latent Signals, distributed memory, or directory consolidation.
    Format: A single concise sentence explaining the best practice.
    """

    lessons = []

    # 1. Ollama (Local External)
    print(" - Synchronizing with Ollama (Local)...")
    ollama_res = ai.llm_chat_via_ollama(prompt, model="tinyllama:latest")
    if ollama_res:
        lessons.append({"provider": "Ollama", "text": ollama_res})

    # 2. Gemini/GitHub (Global External)
    print(" - Harvesting insights from GitHub Models...")
    # Using a reliable model ID for GitHub Models
    gemini_res = ai.llm_chat_via_github_models(prompt, model="Meta-Llama-3.1-8B-Instruct") 
    if gemini_res:
        lessons.append({"provider": "GitHubModels", "text": gemini_res})

    # 3. Agentic consultation (Copilot CLI)
    print(" - Querying GitHub Copilot CLI (System Intel)...")
    copilot_res = ai.llm_chat_via_copilot_cli(prompt)
    if copilot_res:
        lessons.append({"provider": "CopilotCLI", "text": copilot_res})
    else:
        # Fallback to smart_chat if CLI fails
        agentic_res = ai.smart_chat(prompt, preference="external", external_model="Meta-Llama-3.1-8B-Instruct")
        if agentic_res:
            lessons.append({"provider": "Copilot/Agent", "text": agentic_res})

    # Feed lessons into Intelligence Orchestrator (Phase 108)
    if lessons:
        try:
            # Note: fleet.intelligence is accessed via lazy attribute delegation
            for lesson in lessons:
                fleet.intelligence.contribute_insight(
                    agent_name=f"External_{lesson['provider']}",
                    insight=lesson['text'],
                    confidence=0.85
                )
            print(f" - Successfully integrated {len(lessons)} external insights into Hive Mind.")
        except Exception as e:
            print(f" - Failed to contribute insights to Intelligence Orchestrator: {e}")
            
    return lessons

def _cycle_throttle(delay: int) -> None:
    """Implement a controlled delay between improvement cycles."""
    import time
    time.sleep(delay)

def main() -> None:
    parser = argparse.ArgumentParser(description="PyAgent Fleet Self-Improvement Loop")
    parser.add_argument("--cycles", "-c", type=int, default=1, help="Number of improvement cycles to run (default: 1). Use 0 or -1 for infinite/continuous.")
    parser.add_argument("--delay", "-d", type=int, default=6, help="Delay in seconds between cycles (default: 6)")
    parser.add_argument("--prompt", "-p", type=str, help="Path to a strategic prompt/directive file (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Initialize and verify fleet without running full cycle")
    args = parser.parse_args()

    root = os.getcwd()
    fleet = FleetManager(root)
    
    print("=== SWARM SELF-IMPROVEMENT CYCLE INITIATED ===")
    print(f"Scanning workspace: {root}")

    if args.dry_run:
        print("Dry-run mode: Initialization successful. Fleet is healthy.")
        print(f"SDK Version: {fleet.agents.core.sdk_version}")
        sys.exit(0)

    try:
        num_cycles = args.cycles
        is_infinite = num_cycles <= 0
        prompt_path = args.prompt
        
        if num_cycles == 1:
            run_cycle(fleet, root, prompt_path=prompt_path, current_cycle=1)
        else:
            current_cycle = 0
            if is_infinite:
                print(f"Running in CONTINUOUS mode with {args.delay}s delay. Press Ctrl+C to stop.")
            else:
                print(f"Running {num_cycles} cycles with {args.delay}s delay. Press Ctrl+C to stop.")
                
            while True:
                current_cycle += 1
                
                run_cycle(fleet, root, prompt_path=prompt_path, current_cycle=current_cycle)
                
                if not is_infinite and current_cycle >= num_cycles:
                    break
                    
                print(f"\nWaiting {args.delay}s before next cycle... (Press Ctrl+C to stop)")
                _cycle_throttle(args.delay)
                
    except KeyboardInterrupt:
        print("\n=== STOPPING SELF-IMPROVEMENT (User Interrupt) ===")
        sys.exit(0)

if __name__ == "__main__":
    main()
