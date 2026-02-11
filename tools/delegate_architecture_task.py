#!/usr/bin/env python3
"""
Minimal task runner that reads implement_architecture.json and delegates
the implementation to a local Copilot CLI if available.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

def find_spec():
    candidates = [
        "implement_architecture.json",
        os.path.join("temp", "implement_architecture.json"),
        os.path.join("data", "implement_architecture.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("implement_architecture.json not found; looked in: " + ", ".join(candidates))

def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_copilot_cli(override=None):
    if override:
        if shutil.which(override):
            return shutil.which(override)
        return None
    for name in ("copilot", "copilot-cli", "github-copilot-cli"):
        p = shutil.which(name)
        if p:
            return p
    return None

def run_cli(cli_path, spec_path, extra_args=None):
    extra_args = extra_args or []
    cmd = [cli_path, "implement", "--input", spec_path] + extra_args
    print("Executing:", " ".join(cmd))
    try:
        return subprocess.call(cmd)
    except OSError as e:
        print("Failed to execute CLI:", e, file=sys.stderr)
        return 3

def summarize_spec(spec):
    print("Specification summary:")
    if isinstance(spec, dict):
        for k, v in list(spec.items())[:10]:
            print(f"- {k}: {type(v).__name__}")
    else:
        print(f"- top-level type: {type(spec).__name__}")

def main():
    parser = argparse.ArgumentParser(description="Delegate architecture implementation via local Copilot CLI")
    parser.add_argument("--spec", help="Path to implement_architecture.json")
    parser.add_argument("--cli", help="Path or name of Copilot CLI to use (overrides auto-detection)")
    parser.add_argument("--dry-run", action="store_true", help="Only print actions without executing CLI")
    parser.add_argument("--extra-arg", action="append", help="Extra argument(s) passed to the CLI", default=[])
    args = parser.parse_args()

    try:
        spec_path = args.spec or find_spec()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    try:
        spec = load_spec(spec_path)
    except Exception as e:
        print("Failed to read spec:", e, file=sys.stderr)
        sys.exit(2)

    summarize_spec(spec)

    cli = find_copilot_cli(args.cli)
    if not cli:
        print("No local Copilot CLI found. Install one of: copilot, copilot-cli, github-copilot-cli")
        print("Or provide a path with --cli. Dry-run mode:", args.dry_run)
        if args.dry_run:
            print("Dry-run complete.")
            sys.exit(0)
        sys.exit(4)

    if args.dry_run:
        print("Would run CLI:", cli, "with spec", spec_path, "and extra args", args.extra_arg)
        sys.exit(0)

    rc = run_cli(cli, spec_path, args.extra_arg)
    print("CLI exited with code", rc)
    sys.exit(rc if isinstance(rc, int) else 0)

if __name__ == "__main__":
    main()


"""
Delegate the implementation of 3 architectural security patterns to CoderAgent.
Run with: python tools/delegate_architecture_task.py
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.common.models.core_enums import AgentPriority
from src.logic.agents.development.coder_agent import CoderAgent


def load_task_spec() -> dict:
    """Load task specification from JSON file."""
    task_file = Path(__file__).resolve().parents[1] / "temp" / "implement_architecture.json"
    if not task_file.exists():
        raise FileNotFoundError(f"Task file not found: {task_file}")
    
    with open(task_file, encoding='utf-8') as f:
        return json.load(f)


def build_task_prompt(spec: dict) -> str:
    """Convert JSON task spec to detailed prompt."""
    lines = [
        "Implement 3 architectural patterns for the PyAgent fleet:\n",
    ]
    
    for idx, pattern in enumerate(spec["requirements"]["patterns"], 1):
        lines.append(f"## {idx}. {pattern['name']}")
        lines.append(f"File: {pattern.get('file', pattern.get('target', 'TBD'))}")
        lines.append(f"{pattern['description']}\n")
        
        impl = pattern.get("implementation", {})
        if "class_name" in impl:
            lines.append(f"Class: {impl['class_name']}")
        if "methods" in impl:
            lines.append(f"Methods: {', '.join(impl['methods'])}")
        if "features" in impl:
            lines.append("Features:")
            for feature in impl["features"]:
                lines.append(f"  - {feature}")
        if "methods_to_extract" in impl:
            lines.append(f"Extract methods: {', '.join(impl['methods_to_extract'])}")
        lines.append("")
    
    lines.append("\nConstraints:")
    for constraint in spec.get("constraints", []):
        lines.append(f"- {constraint}")
    
    return "\n".join(lines)


async def main_delegate() -> None:
    """Execute the delegation."""
    print("🚀 Delegating architecture implementation to CoderAgent...")
    
    # Load task specification
    try:
        task_spec = load_task_spec()
        task_prompt = build_task_prompt(task_spec)
        print(f"📄 Loaded task: {task_spec.get('task_type', 'unknown')}")
    except Exception as e:
        print(f"❌ Failed to load task spec: {e}")
        sys.exit(1)
    
    # Create cascade context to track this task
    context = CascadeContext(
        task_id="arch_patterns_implementation_001",
        agent_id="copilot_cli_delegator",
        cascade_depth=0
    )
    
    # Target file for the agent to work on (first pattern file)
    first_pattern = task_spec["requirements"]["patterns"][0]
    target_file = str(Path(__file__).resolve().parents[1] / first_pattern.get("file", first_pattern.get("target")))
    
    # Initialize CoderAgent
    try:
        agent = CoderAgent(target_file)
        
        print(f"📋 Task ID: {context.task_id}")
        print(f"🎯 Starting file: {target_file}")
        print(f"🔢 Priority: {task_spec.get('priority', 'high').upper()}")
        print(f"\n{'='*60}")
        print("TASK PROMPT:")
        print(task_prompt)
        print(f"{'='*60}\n")
        
        # Use the delegation mixin if available
        if hasattr(agent, 'delegator'):
            result = await agent.delegator.delegate(
                agent_type="CoderAgent",
                prompt=task_prompt,
                target_file=target_file,
                context=context,
                priority=AgentPriority.HIGH
            )
        else:
            # Direct execution fallback (BaseAgent.run is synchronous)
            result = agent.run(task_prompt)
        
        print(f"\n{'='*60}\n")
        print("✅ Delegation Result:")
        print(result)
        
    except Exception as e:
        print(f"❌ Delegation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Provide two modes: the CLI-driven implementer or the CoderAgent delegator
    if len(sys.argv) > 1:
        # pass-through to the original CLI runner behavior
        main()
    else:
        asyncio.run(main_delegate())
