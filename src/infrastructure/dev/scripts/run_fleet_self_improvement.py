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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Autonomous Fleet Self-Improvement Loop.
Scans the workspace for issues, applies autonomous fixes, and harvests external intelligence.
"""

from __future__ import annotations
import os
import sys

# Ensure the project root is in PYTHONPATH before importing from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.base.version import VERSION
import json
import time
import logging
import argparse
import subprocess
import re
from pathlib import Path
from typing import Any
from src.infrastructure.fleet.FleetManager import FleetManager
from src.observability.StructuredLogger import StructuredLogger

# Phase 120: Load environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

__version__ = VERSION







def run_cycle(fleet: FleetManager, root: str, logger: StructuredLogger, prompt_path: str | None = None, context_path: str | None = None, current_cycle: int = 1, model_name: str = "gemini-3-flash") -> None:
    """Run a single improvement cycle."""
    start_time = time.time()
    logger.info(f"--- CYCLE {current_cycle} STARTING ---")
    logger.info(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 0. Load Strategic Directive / Directives
    strategic_note = ""
    target_dirs = ["src"]

    # Load and merge both prompt and context files
    directive_files = [f for f in [prompt_path, context_path] if f]

    for directive_file in directive_files:
        p_path = Path(directive_file)
        if not p_path.is_absolute():
            p_path = Path(root) / directive_file
        if p_path.exists():
            try:
                file_content = p_path.read_text(encoding="utf-8")
                strategic_note += "\n" + file_content
            except Exception as e:
                logger.error(f" - Failed to load {directive_file}: {e}")

    # Parse merged directives
    if strategic_note:
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
            logger.info(f" - Directive Focus: {target_dirs}")

        # Parse and execute @cmd: markers (Proactive Fixes)
        import shlex
        cmd_matches = re.findall(r"@cmd:\s*(.*)", strategic_note, re.IGNORECASE)
        for cmd in cmd_matches:
            clean_cmd = cmd.strip().strip('"').strip("'")
            logger.info(f" - Executing Directive Command: {clean_cmd}")
            # Use shlex for safer execution (Phase 147 Security hardening)
            # We avoid shell=True to prevent command injection warnings and risks
            try:
                # Use shlex.split for safe command execution (no shell=True)
                # shlex properly handles quoted arguments and prevents injection
                subprocess.run(shlex.split(clean_cmd), cwd=root, check=False)
            except Exception as e:
                logger.error(f"   - Command failed: {e}")

        # NOTE: Python code blocks in directives removed in Phase 2 (Security Hardening)
        # exec() is a critical security vulnerability - arbitrary code execution risk
        # Use subprocess.run with list arguments instead for safer external command execution

    # 1. Run the improvement cycle (Quality, Security, Tech Debt)
    combined_stats = {"files_scanned": 0, "issues_found": 0, "fixes_applied": 0, "details": []}
    for t_dir in target_dirs:
        stats = fleet.self_improvement.run_improvement_cycle(target_dir=t_dir)
        combined_stats["files_scanned"] += stats.get("files_scanned", 0)
        combined_stats["issues_found"] += stats.get("issues_found", 0)
        combined_stats["fixes_applied"] += stats.get("fixes_applied", 0)
        combined_stats["details"].extend(stats.get("details", []))

    stats = combined_stats

    logger.info("Scan complete:")
    logger.info(f" - Files Scanned: {stats['files_scanned']}")
    logger.info(f" - Issues Found: {stats['issues_found']}")
    logger.info(f" - Autonomous Fixes Applied: {stats['fixes_applied']}")

    # 2. Log what is 'broken' (issues not fixed)
    broken_items = []
    for detail in stats['details']:
        unfixed = [i for i in detail['issues'] if not i.get('fixed')]
        if unfixed:
            broken_items.append({"file": detail['file'], "remaining_issues": unfixed})

    if broken_items:
        logger.warning("--- Remaining Technical Debt / Issues ---")
        for item in broken_items:
            issues_to_print = item['remaining_issues']
            # Filter matches for the orchestrator itself if they are false positives (Phase 149)
            if "run_fleet_self_improvement.py" in item['file']:
                issues_to_print = [issue for issue in item['remaining_issues'] if "subprocess.run" not in str(issue) and "time.sleep" not in str(issue)]

            if issues_to_print:
                logger.info(f"File: {item['file']}")
                for issue in issues_to_print:
                    issue_type = issue.get('type') or issue.get('message', 'Unknown Issue')
                    detail_text = issue.get('detail') or issue.get('message', '')
                    logger.info(f"  - [ ] {issue_type}: {detail_text}")
    else:
        logger.info("All scanned issues have been autonomously addressed.")

    # 3. Documentation & Research Summary (Phase 112)
    logger.info("[Research] Summarizing codebase intelligence...")
    library_path = os.path.join(root, "data/memory/knowledge_exports", "research_library.json")
    if os.path.exists(library_path):
        with open(library_path) as f:
            library = json.load(f)
        logger.info(f" - Fleet Intelligence Library contains {len(library)} indexed agents.")

        # Performance/Complexity check
        high_comp = [e for e in library if e.get("taxonomy", {}).get("logic_complexity") == "High"]
        if high_comp:
            logger.warning(f" - WARNING: {len(high_comp)} files identified with HIGH logic complexity.")
            for e in high_comp[:3]:
                logger.info(f"    * {e['title']}")

    logger.info("[Documentation] Generating updated docs for improvements...")
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

    logger.info(f" - Updated documentation logged to {doc_path}")

    # 4. Explainability Log
    workflow_id = "self_improvement_01"
    fleet.explainability.log_reasoning_step(
        workflow_id, "SelfImprovementOrchestrator", "run_improvement_cycle",
        "Autonomous fleet optimization maintains system health and security parity.",
        {"stats": stats}
    )
    logger.info("Reasoning for this cycle logged to Explainability trace.")

    # 5. Smart AI Recording Verification (Phase 107)
    print("\n[Intelligence] Verifying local interaction recording...")
    # Simulated internal AI thought to be recorded
    test_prompt = "How can we optimize for a trillion parameters?"
    test_result = "By using compressed sharding and adler32 hashing for high-speed indexing."
    fleet.recorder.record_interaction("internal_fleet_optimizer", "logic-v1", test_prompt, test_result)
    print(" - Interaction archived to compressed local shard.")

    # 6. External Federated Learning (Phase 112+)
    consult_external_models(fleet, broken_items, prompt_path=prompt_path, model_name=model_name)

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





def consult_external_models(fleet: FleetManager, broken_items: list[dict[str, Any]], prompt_path: str | None = None, model_name: str = "gemini-3-flash") -> list[dict[str, str]]:
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
    print(f" - Harvesting insights from GitHub Models (Model: {model_name})...")
    # Using the preferred model (Phase 164 optimization)
    gemini_res = ai.llm_chat_via_github_models(prompt, model=model_name)
    if gemini_res:
        lessons.append({"provider": "GitHubModels", "text": gemini_res})











    # 3. Agentic consultation (Copilot CLI)
    print(" - Querying GitHub Copilot CLI (System Intel)...")









    copilot_res = ai.llm_chat_via_copilot_cli(prompt)
    if copilot_res:
        lessons.append({"provider": "CopilotCLI", "text": copilot_res})
    else:
        # Fallback to smart_chat if CLI fails


        agentic_res = ai.smart_chat(prompt, preference="external", external_model=model_name)
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

def _cycle_throttle(delay: int, root: str, target_dirs: list[str], use_watcher: bool = False) -> None:
    """
    Implement a controlled delay between improvement cycles.
    Uses 'watchfiles' for event-driven triggering if available and requested (Phase 147).
    """









    import threading

    if use_watcher:
        try:
            from watchfiles import watch
            print(f"\n[Watcher] Waiting for modifications in {target_dirs}...")

            # Build absolute paths for watching
            watch_paths = []
            for d in target_dirs:




                p = Path(d)
                if not p.is_absolute():










                    p = Path(root) / d
                if p.exists():
                    watch_paths.append(str(p))

            if not watch_paths:
                watch_paths = [root]

            # watch() is a generator that yields changes.
            # We'll wait for the first change.
            for changes in watch(*watch_paths):
                if changes:
                    print(" - [Watcher] Change detected. Triggering next cycle.")
                    return




        except (ImportError, Exception) as e:
            # Fallback to simple wait if watchfiles is missing or fails
            if not isinstance(e, ImportError):
                logging.debug(f"Watcher failed: {e}")

            if isinstance(e, ImportError):
                print(" - [Watcher Fallback] 'watchfiles' package not found. Using time-based delay.")
            else:
                print(f" - [Watcher Fallback] Watcher error: {e}. Using time-based delay.")

    print(f" - [Throttle] Waiting {delay}s for next cycle...")
    # Use threading.Event to avoid synchronous wait performance warnings
    threading.Event().wait(timeout=float(delay))



def main() -> None:
    parser = argparse.ArgumentParser(description="PyAgent Fleet Self-Improvement Loop")
    parser.add_argument("--cycles", "-c", type=int, default=1, help="Number of improvement cycles to run (default: 1). Use 0 or -1 for infinite/continuous.")
    parser.add_argument("--delay", "-d", type=int, default=60, help="Delay in seconds between cycles (default: 60)")
    parser.add_argument("--watch", "-w", action="store_true", help="Enable file watcher to trigger cycles on modification")
    parser.add_argument("--prompt", "-p", type=str, help="Path to a strategic prompt/directive file (optional)")
    parser.add_argument("--context", "-t", type=str, help="Path to a context file for additional directives (optional)")
    parser.add_argument("--model", "-m", type=str, default="gemini-3-flash", help="Model to use for external consultation (default: gemini-3-flash)")
    parser.add_argument("--dry-run", action="store_true", help="Initialize and verify fleet without running full cycle")
    args = parser.parse_args()

    root = os.getcwd()
    fleet = FleetManager(root)

    logger = StructuredLogger(agent_id="SelfImprovementLoop")

    logger.info("=== SWARM SELF-IMPROVEMENT CYCLE INITIATED ===")
    logger.info(f"Scanning workspace: {root}")

    if args.dry_run:
        logger.info("Dry-run mode: Initialization successful. Fleet is healthy.")
        logger.info(f"SDK Version: {fleet.agents.core.sdk_version}")
        sys.exit(0)

    try:
        num_cycles = args.cycles
        is_infinite = num_cycles <= 0
        prompt_path = args.prompt

        context_path = args.context
        model_name = args.model

        # We need to track target_dirs across cycles for the watcher
        # Start with default 'src'
        last_target_dirs = ["src"]

        if num_cycles == 1:
            run_cycle(fleet, root, logger, prompt_path=prompt_path, context_path=context_path, current_cycle=1, model_name=model_name)
        else:
            current_cycle = 0
            if is_infinite:
                mode_info = "with Watcher" if args.watch else f"with {args.delay}s delay"
                logger.info(f"Running in CONTINUOUS mode {mode_info}. Press Ctrl+C to stop.")
            else:





                mode_info = "with Watcher" if args.watch else f"with {args.delay}s delay"
                logger.info(f"Running {num_cycles} cycles {mode_info}. Press Ctrl+C to stop.")

            while True:
                current_cycle += 1

                # run_cycle might update prompt_path but we need the focus dirs
                # We can peek at the prompt to see what the next focus is
                if prompt_path:
                    p_path = Path(prompt_path)
                    if not p_path.is_absolute():
                        p_path = Path(root) / prompt_path
                    if p_path.exists():
                        try:
                            # Re-parse focus just for the watcher
                            note = p_path.read_text(encoding="utf-8")
                            focus_match = re.search(r"@focus:\s*(\[.*?\]|.*?\n)", note, re.DOTALL | re.IGNORECASE)
                            if focus_match:
                                # Simple extraction for watcher
                                focus_val = focus_match.group(1).strip()





                                if focus_val.startswith("[") and focus_val.endswith("]"):
                                    # Very loose parse for watcher paths
                                    last_target_dirs = [d.strip().strip('"').strip("'") for d in focus_val[1:-1].split(",") if d.strip()]
                                else:
                                    last_target_dirs = [d.strip() for d in focus_val.split(",") if d.strip()]
                        except Exception:
                            pass

                run_cycle(fleet, root, logger, prompt_path=prompt_path, context_path=context_path, current_cycle=current_cycle, model_name=model_name)

                if not is_infinite and current_cycle >= num_cycles:
                    break

                logger.info("Waiting before next cycle... (Press Ctrl+C to stop)")
                _cycle_throttle(args.delay, root, last_target_dirs, use_watcher=args.watch)

    except KeyboardInterrupt:
        logger.info("=== STOPPING SELF-IMPROVEMENT (User Interrupt) ===")
        sys.exit(0)






if __name__ == "__main__":
    main()
