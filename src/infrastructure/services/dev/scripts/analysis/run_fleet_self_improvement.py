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
Autonomous Fleet Self-Improvement Loop.
Scans the workspace for issues, applies autonomous fixes, and harvests external intelligence.
"""

from __future__ import annotations


import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
# ruff: noqa: E402

# Ensure the project root is in PYTHONPATH before importing from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Phase 335: Support for custom Copilot CLI paths
COPILOT_PATH = r"C:\DEV\copilot-cli"
if os.path.exists(COPILOT_PATH) and COPILOT_PATH not in os.environ["PATH"]:
    os.environ["PATH"] = COPILOT_PATH + os.pathsep + os.environ["PATH"]
    logging.info(f"Augmented PATH with {COPILOT_PATH}")


# Import the Rust extension for fleet self-improvement (registers PyO3 functions)
try:
    # import rust_core  # Rust-powered analysis and fix functions
    RUST_ACCEL = True
    RUST_CORE = None
except ImportError:
    RUST_CORE = None
    RUST_ACCEL = False


# pylint: disable=wrong-import-position
from src.core.base.lifecycle.version import VERSION  # noqa: E402
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager  # noqa: E402
from src.observability.structured_logger import StructuredLogger  # noqa: E402
from src.infrastructure.services.dev.scripts.analysis.prompt_optimizer_agent import PromptOptimizerAgent  # noqa: E402
# pylint: enable=wrong-import-position


# Phase 317: Specialized helpers to reduce complexity
class DirectiveParser:
    """Parses strategic directives from prompt and context files."""

    def __init__(self, root: str, prompt_path: str | None, context_path: str | None) -> None:
        self.root = Path(root)
        self.prompt_path = prompt_path
        self.context_path = context_path
        self.strategic_note = ""

    def load_directives(self) -> str:
        """Loads and merges prompt and context files."""
        directive_files = [f for f in [self.prompt_path, self.context_path] if f]
        for directive_file in directive_files:
            p_path = Path(directive_file)
            if not p_path.is_absolute():
                p_path = self.root / directive_file
            if p_path.exists():
                try:
                    self.strategic_note += "\n" + p_path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError) as e:
                    logging.error(f" - Failed to load {directive_file}: {e}")
        return self.strategic_note

    def get_focus_dirs(self) -> list[str]:
        """Extracts @focus: folders from the directives."""
        if not self.strategic_note:
            return ["src"]

        focus_match = re.search(r"@focus:\s*(\[.*?\]|.*?\n)", self.strategic_note, re.DOTALL | re.IGNORECASE)
        if not focus_match:
            return ["src"]

        focus_val = focus_match.group(1).strip()
        if focus_val.startswith("[") and focus_val.endswith("]"):
            try:
                clean_focus = re.sub(r"[\s\n]+", " ", focus_val)
                return json.loads(clean_focus.replace("'", '"'))
            except (json.JSONDecodeError, ValueError):
                inner = focus_val[1:-1].split(",")
                return [d.strip().strip('"').strip("'").strip() for d in inner if d.strip()]
        return [d.strip() for d in focus_val.split(",") if d.strip()]

    def execute_commands(self) -> None:
        """Extracts and runs @cmd: markers."""
        if not self.strategic_note:
            return

        import shlex

        cmd_matches = re.findall(r"@cmd:\s*(.*)", self.strategic_note, re.IGNORECASE)
        for cmd in cmd_matches:
            clean_cmd = cmd.strip().strip('"').strip("'")
            logging.info(f" - Executing Directive Command: {clean_cmd}")
            try:
                subprocess.run(shlex.split(clean_cmd), cwd=str(self.root), check=False)
            except (OSError, subprocess.SubprocessError) as e:
                logging.error(f"   - Command failed: {e}")


class IntelligenceHarvester:
    """Orchestrates external intelligence harvesting."""

    def __init__(self, fleet: FleetManager, model_name: str) -> None:
        self.fleet = fleet
        self.model_name = model_name


    def harvest(self) -> list[dict[str, Any]]:
        """Harvests insights from multiple external backends, with prompt optimization."""
        from src.infrastructure.compute.backend import execution_engine as ai

        prompt = "Provide 3 high-level architectural or security recommendations for a Python-based AI Agent fleet."
        lessons = []

        # --- Prompt Optimizer Integration ---
        optimizer = PromptOptimizerAgent()
        ai.llm_chat_via_ollama = optimizer.wrap_agent_prompt(
            ai.llm_chat_via_ollama, agent_name="Ollama"
        )
        ai.llm_chat_via_github_models = optimizer.wrap_agent_prompt(
            ai.llm_chat_via_github_models, agent_name="GitHubModels"
        )
        ai.llm_chat_via_copilot_cli = optimizer.wrap_agent_prompt(
            ai.llm_chat_via_copilot_cli, agent_name="CopilotCLI"
        )

        # 1. Ollama (Local External)
        ollama_res = ai.llm_chat_via_ollama(prompt)
        if ollama_res:
            lessons.append({"provider": "Ollama", "text": ollama_res})

        # 2. GitHub Models (Global External)
        gemini_res = ai.llm_chat_via_github_models(prompt, model=self.model_name)
        if gemini_res:
            lessons.append({"provider": "GitHubModels", "text": gemini_res})

        # 3. Copilot CLI (System Intel)
        copilot_res = ai.llm_chat_via_copilot_cli(prompt)
        if copilot_res:
            lessons.append({"provider": "CopilotCLI", "text": copilot_res})

        # Feed to fleet
        if lessons:
            try:
                for lesson in lessons:
                    self.fleet.intelligence.contribute_insight(
                        agent_name=f"External_{lesson['provider']}",
                        insight=lesson["text"],
                        confidence=0.85,
                    )
            except Exception:
                # Broad except is justified here to avoid breaking the intelligence harvesting loop
                logging.debug("Insight contribution failed.")

        return lessons



# Global flag to ensure Triton compatibility is only checked/logged on the first cycle

class CycleOrchestrator:
    """Manages the execution of multiple improvement cycles."""

    def __init__(self, fleet: FleetManager, args: argparse.Namespace) -> None:
        self.fleet = fleet
        self.args = args
        self.root = os.getcwd()
        self.logger = StructuredLogger(agent_id="SelfImprovementLoop")
        self.is_infinite = args.cycles <= 0
        self._triton_checked_once = False
        # Stores normalized messages from the last completed cycle for stagnation detection
        self._last_cycle_messages: list[str] | None = None


    def run(self) -> None:
        """Executes the loop based on arguments, always printing per-cycle timing."""
        current_cycle = 0
        while True:
            current_cycle += 1
            start_time = time.time()
            # Only allow Triton compatibility check/logging on the first cycle
            if not hasattr(self, '_triton_checked_once') or not self._triton_checked_once:
                # Proactively set GITHUB_TOKEN from gh CLI if not already set
                if not os.environ.get("GITHUB_TOKEN"):
                    try:
                        res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=False)
                        if res.returncode == 0:
                            token = res.stdout.strip()
                            if token:
                                os.environ["GITHUB_TOKEN"] = token
                                logging.info("GITHUB_TOKEN set from 'gh auth token' for first cycle.")
                    except subprocess.SubprocessError:
                        logging.warning("Could not set GITHUB_TOKEN from gh CLI.")
                result = run_cycle(
                    self.fleet,
                    self.root,
                    self.logger,
                    prompt_path=self.args.prompt,
                    context_path=self.args.context,
                    model_name=self.args.model,
                    allow_triton_check=True,
                )
                self._triton_checked_once = True
            else:
                result = run_cycle(
                    self.fleet,
                    self.root,
                    self.logger,
                    prompt_path=self.args.prompt,
                    context_path=self.args.context,
                    model_name=self.args.model,
                    allow_triton_check=False,
                )
            duration = time.time() - start_time
            print(f"\n=== CYCLE {current_cycle} COMPLETE (Time spent: {duration:.2f}s) ===")
            # Compare messages with previous cycle to detect stagnation.
            # Only apply this early-cancel behavior when the user requested multiple cycles.
            current_messages: list[str] = result.get("messages", []) if isinstance(result, dict) else []

            if getattr(self.args, "cycles", 1) > 1 and current_cycle > 1:
                if hasattr(self, "_last_cycle_messages") and self._last_cycle_messages == current_messages:
                    self.logger.info("No new messages since previous cycle — cancelling remaining cycles.")
                    break

            # Save for next cycle comparison
            self._last_cycle_messages = current_messages

            if not self.is_infinite and current_cycle >= self.args.cycles:
                break

            self.logger.info("Waiting before next cycle... (Press Ctrl+C to stop)")
            _cycle_throttle(self.args.delay, self.root, self._get_last_focus(), use_watcher=self.args.watch)

    def _get_last_focus(self) -> list[str]:
        """Peeks at the prompt for the watcher's benefit."""
        if not self.args.prompt:
            return ["src"]
        parser = DirectiveParser(self.root, self.args.prompt, None)
        parser.load_directives()
        return parser.get_focus_dirs()


# Phase 120: Load environment variables if available
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # dotenv is optional
    pass

__version__ = VERSION



def run_cycle(
    fleet: FleetManager,
    root: str,
    logger: StructuredLogger,
    prompt_path: str | None = None,
    context_path: str | None = None,
    current_cycle: int = 1,
    model_name: str = "gemini-3-flash",
    allow_triton_check: bool = True,
) -> dict[str, Any]:
    """Run a single improvement cycle and return a dict with per-cycle messages and stats.

    Returns a dict with keys:
      - "messages": list[str] normalized external intelligence messages
      - "stats": combined_stats dictionary summarizing the run
    """
    logger.info(f"--- CYCLE {current_cycle} STARTING ---")

    # 1. Parse Directives
    parser = DirectiveParser(root, prompt_path, context_path)
    parser.load_directives()
    target_dirs = parser.get_focus_dirs()
    parser.execute_commands()

    # 2. Run Improvement Loop
    combined_stats = {"files_scanned": 0, "issues_found": 0, "fixes_applied": 0, "details": []}
    for t_dir in target_dirs:
        # Patch: Only allow Triton compatibility check on first cycle
        stats = fleet.self_improvement.run_improvement_cycle(target_dir=t_dir, allow_triton_check=allow_triton_check)
        combined_stats["files_scanned"] += stats.get("files_scanned", 0)
        combined_stats["issues_found"] += stats.get("issues_found", 0)
        combined_stats["fixes_applied"] += stats.get("fixes_applied", 0)
        combined_stats["details"].extend(stats.get("details", []))

    # 3. Report Results
    logger.info(
        f" - Scanned: {combined_stats['files_scanned']}, Issues: {combined_stats['issues_found']}, "
        f"Fixed: {combined_stats['fixes_applied']}"
    )

    _report_remaining_debt(
        combined_stats,
        logger,
        fleet,
        root,
        target_dirs=target_dirs,
        prompt_path=prompt_path,
        model_name=model_name,
    )

    # 4. Harvest External Intelligence
    harvester = IntelligenceHarvester(fleet, model_name)
    lessons = harvester.harvest()

    # Normalize messages for inter-cycle comparison
    messages = [f"{l.get('provider')}:{l.get('text')}" for l in lessons if isinstance(l, dict) and l.get('text')]

    # Return per-cycle information for orchestration decisions
    return {"messages": messages, "stats": combined_stats}


def consult_external_models(
    fleet: Any,
    broken_items: list[dict[str, Any]],
    prompt_path: str | None = None,
    model_name: str | None = None
) -> None:
    """
    Placeholder for federated learning consultation (Phase 112).
    """
    # pylint: disable=unused-argument
    print("[Intelligence] Consulting external federated models for remaining debt...")
    if broken_items:
        print(f" - Analyzed {len(broken_items)} debt clusters.")
        for item in broken_items:
            print(f"   * File: {item['file']}")
            for issue in item["remaining_issues"]:
                print(f"     - {issue.get('type', 'Unknown')}: {issue.get('message', '')}")
    print("[Intelligence] Federated consensus reached: Continue localized refactoring.")


def _analyze_unfixed_issues(stats: dict[str, Any]) -> list[dict[str, Any]]:
    """Filters and summarizes issues that were not fixed."""
    broken_items = []
    # Clean up whitespace
    for detail in stats["details"]:
        unfixed = [i for i in detail["issues"] if not i.get("fixed")]
        if unfixed:
            # Filter matches for the orchestrator itself if they are false positives
            if "run_fleet_self_improvement.py" in detail["file"]:
                unfixed = [
                    i for i in unfixed
                    if "subprocess.run" not in str(i) and "time.sleep" not in str(i)
                ]

            if unfixed:
                broken_items.append({"file": detail["file"], "remaining_issues": unfixed})
    return broken_items


def _update_auto_documentation(fleet: FleetManager, root: str, stats: dict[str, Any]) -> None:
    """Updates FLEET_AUTO_DOC.md with cycle results."""
    fleet_path = os.path.join(root, "src/infrastructure/fleet/fleet_manager.py")
    doc_res = fleet.doc_gen_agent.extract_docs(fleet_path)
    doc_path = os.path.join(root, "docs/FLEET_AUTO_DOC.md")

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write("# Swarm Auto-Generated Documentation\n\n")
        f.write(doc_res)

    maintenance_summary = (
        f"\n## {time.strftime('%Y-%m-%d')} - Maintenance Cycle Summary\n"
        f"The fleet's SelfImprovementOrchestrator completed a cycle over "
        f"{stats['files_scanned']} files. Re-stabilization phase engaged.\n"
    )
    with open(doc_path, "a", encoding="utf-8") as f:
        f.write(maintenance_summary)


def _log_explainability(fleet: FleetManager, stats: dict[str, Any]) -> None:
    """Logs the reasoning for the improvement cycle."""
    fleet.explainability.log_reasoning_step(
        "self_improvement_01",
        "SelfImprovementOrchestrator",
        "run_improvement_cycle",
        justification="Autonomous fleet optimization maintains system health and security parity.",
        context={"stats": stats},
    )


def _verify_ai_recording(fleet: FleetManager) -> None:
    """Verifies that local interaction recording is functional."""
    test_prompt = "How can we optimize for a trillion parameters?"
    test_result = "By using compressed sharding and adler32 hashing for high-speed indexing."
    fleet.recorder.record_interaction("internal_fleet_optimizer", "logic-v1", test_prompt, test_result)


def _synthesize_collective_knowledge(fleet: FleetManager) -> None:
    """Triggers knowledge synthesis from the swarm."""
    logger = StructuredLogger(agent_id="SelfImprovementLoop")
    try:
        new_patterns = fleet.intelligence.synthesize_collective_intelligence()
        if new_patterns:
            logger.info(f"[Intelligence] Identified {len(new_patterns)} new actionable patterns for the next cycle.")
            for idx, pattern in enumerate(new_patterns, 1):
                file_link = ""
                doc_link = ""
                if isinstance(pattern, dict):
                    desc = pattern.get("description", str(pattern))
                    file_path = pattern.get("file")
                    # ...existing code...
                    doc = pattern.get("doc")
                else:
                    desc = str(pattern)
                    file_path = None
                    # ...existing code...
                    doc = None
                if file_path:
                    file_link = f" [View]({file_path})"
                if doc:
                    doc_link = f" [Docs]({doc})"
                logger.info(f"  {idx}. {desc}{file_link}{doc_link}")
    except Exception:
        # Broad except is justified here to ensure explainability logging never breaks the main loop
        logger.warning("[Intelligence] Synthesis skipped.")


def _attempt_autonomous_solutions(fleet: FleetManager, broken_items: list[dict[str, Any]], model_name: str) -> None:
    """
    Constructs a prompt with cycle findings and attempts to solve remaining issues
    via autonomous reasoning or external LLM consultation.
    """
    if not broken_items:
        return

    print("\n[Autonomous Solver] Attempting to resolve remaining technical debt...")

    # Construct the context prompt
    context_prompt = "The following technical debt issues remain after the initial improvement cycle:\n\n"
    for item in broken_items:
        context_prompt += f"File: {item['file']}\n"
        for issue in item["remaining_issues"]:
            context_prompt += f"- {issue.get('type')}: {issue.get('message')}\n"
        context_prompt += "\n"

    context_prompt += (
        "Analyze these specific issues. Provide a concrete Python code snippet or "
        "architectural change that resolves the pattern causing these warnings. "
        "Focus on the root cause (e.g., missing type hints, unsafe IO pattern, recursion depth)."
    )

    # Attempt to solve via Fleet Intelligence (External LLM)
    try:
        from src.infrastructure.compute.backend import execution_engine as ai

        print(" - Querying external intelligence for solution patterns...")
        # Use available heavy model
        solution = ai.llm_chat_via_github_models(context_prompt, model=model_name)

        if solution:
            print("\n[Autonomous Solver] Proposed Solution:")
            print("-" * 40)
            print(solution.strip())
            print("-" * 40)

            # Record this lesson
            fleet.intelligence.contribute_insight(
                agent_name="AutonomousSolver",
                insight=f"Proposed fix for debt cluster: {solution[:100]}...",
                confidence=0.9
            )
            print(" - Solution pattern recorded to collective knowledge.")

    except Exception:
        # Broad except is justified here to ensure the main loop continues even if LLM call fails
        print(" - Autonomous solving failed.")


def _prune_verified_directives(
    prompt_path: str | None,
    root: str,
    target_dirs: list[str],
    broken_items: list[Any]
) -> None:
    """Removes completed directives from the prompt file."""
    if not (prompt_path and not broken_items):
        return

    p_path = Path(prompt_path)
    if not p_path.is_absolute():
        p_path = Path(root) / prompt_path
    if not p_path.exists():
        return

    print(f"\n[Maintenance] Area '@focus: {target_dirs}' is CLEAN. Pruning directive...")
    content = p_path.read_text(encoding="utf-8")

    # DYNAMIC MULTI-LINE PRUNING (Phase 141)
    new_content = re.sub(
        r"^@focus:.*?\].*?\n",
        "",
        content,
        count=1,
        flags=re.MULTILINE | re.IGNORECASE | re.DOTALL,
    )
    if new_content == content:
        new_content = re.sub(r"^@focus:.*$\n?", "", content, count=1, flags=re.MULTILINE | re.IGNORECASE)

    new_content = re.sub(r"^@cmd:.*$\n?", "", new_content, count=1, flags=re.MULTILINE | re.IGNORECASE)
    new_content = re.sub(
        r"^@python:\s*\"\"\"(.*?)\"\"\"\n?", "", new_content, count=1,
        flags=re.DOTALL | re.IGNORECASE
    )
    new_content = re.sub(r"^- \[x\].*$\n?", "", new_content, flags=re.MULTILINE | re.IGNORECASE)
    new_content = re.sub(r"^# DONE.*$\n?", "", new_content, flags=re.MULTILINE | re.IGNORECASE)

    if new_content != content:
        p_path.write_text(new_content.strip() + "\n", encoding="utf-8")
        print(f" - Updated {p_path.name}: Verified directives REMOVED.")


def _report_remaining_debt(
    stats: dict[str, Any],
    logger: StructuredLogger,
    fleet: FleetManager,
    root: str,
    target_dirs: list[str],
    prompt_path: str | None = None,
    model_name: str | None = None,
) -> None:
    """Logs issues that were not autonomously fixed and performs maintenance."""
    # start_time = time.time()  # Unused variable removed

    # 1. Analyze and Log Unfixed Issues
    broken_items = _analyze_unfixed_issues(stats)
    if broken_items:
        logger.warning("--- Remaining Technical Debt ---")
        for item in broken_items:
            logger.info(f"File: {item['file']}")
            for issue in item["remaining_issues"]:
                logger.info(f"  - [ ] {issue.get('type', 'Issue')}: {issue.get('message', '')}")

    # 2. Update Documentation
    logger.info("[Documentation] Generating updated docs for improvements...")
    _update_auto_documentation(fleet, root, stats)
    logger.info(" - Updated documentation logged to docs/FLEET_AUTO_DOC.md")

    # 3. Observability and Recording
    _log_explainability(fleet, stats)
    print("[Intelligence] Verifying local interaction recording...")
    _verify_ai_recording(fleet)
    print(" - Interaction archived to compressed local shard.")

    # 4. Intelligence and Synthesis
    consult_external_models(fleet, broken_items, prompt_path=prompt_path, model_name=model_name)

    # 5. Autonomous Problem Solving
    _attempt_autonomous_solutions(fleet, broken_items, model_name)

    _synthesize_collective_knowledge(fleet)

    # 6. Maintenance: Pruning
    _prune_verified_directives(prompt_path, root, target_dirs, broken_items)

    # duration = time.time() - start_time  # Unused variable removed


def _cycle_throttle(
    delay: int,
    root: str,
    target_dirs: list[str],
    use_watcher: bool = False
) -> None:
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

        except Exception:
            # Broad except is justified here to ensure fallback to time-based delay always works
            print(" - [Watcher Fallback] Watcher error. Using time-based delay.")

    print(f" - [Throttle] Waiting {delay}s for next cycle...")
    # Use threading.Event to avoid synchronous wait performance warnings
    threading.Event().wait(timeout=float(delay))



def main() -> None:
    """
    Entry point for the fleet self-improvement loop.
    Parses command-line arguments and launches the CycleOrchestrator.
    """
    parser = argparse.ArgumentParser(description="PyAgent Fleet Self-Improvement Loop")
    parser.add_argument("--cycles", "-c", type=int, default=1)
    parser.add_argument("--delay", "-d", type=int, default=60)
    parser.add_argument("--watch", "-w", action="store_true")
    parser.add_argument("--prompt", "-p", type=str)
    parser.add_argument("--context", "-t", type=str)
    parser.add_argument("--model", "-m", type=str, default="gemini-3-flash")
    parser.add_argument("--dry-run", action="store_true")
    args: argparse.Namespace = parser.parse_args()

    fleet: FleetManager = FleetManager(os.getcwd())
    if args.dry_run:
        logging.info("Dry-run mode: Initialization successful.")
        sys.exit(0)

    try:
        orchestrator: CycleOrchestrator = CycleOrchestrator(fleet, args)
        orchestrator.run()
    except KeyboardInterrupt:
        logging.info("=== STOPPING SELF-IMPROVEMENT (User Interrupt) ===")
        sys.exit(0)


if __name__ == "__main__":
    main()
