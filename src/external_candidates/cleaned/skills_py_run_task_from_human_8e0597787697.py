# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\dobbybud.py\agent_task_manager.py\scripts.py\run_task_from_human_8e0597787697.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\dobbybud\agent-task-manager\scripts\run_task_from_human.py

#!/usr/bin/env python3

# scripts/run_task_from_human.py - The Human Automation Designer Interface

import json

import sys

from orchestrator import run_workflow

from task_parser import parse_human_request


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 run_task_from_human.py "<human request>"')

        print(
            'Example: python3 run_task_from_human.py "Alert me on Signal if the $SHIPYARD whale balance drops below 10%"'
        )

        sys.exit(1)

    human_request = " ".join(sys.argv[1:])

    print(f"--- Processing Human Request: {human_request} ---")

    # 1. Parse Request

    parsed_task = parse_human_request(human_request)

    if "error" in parsed_task:
        print(f"❌ Could not parse request: {parsed_task['error']}")

        sys.exit(1)

    print(f"✅ Request parsed into task: {parsed_task['task_name']}")

    # 2. Run Workflow (Handles state and cooldowns internally)

    final_results = run_workflow(parsed_task)

    print("\n--- Workflow Execution Results ---")

    print(json.dumps(final_results, indent=2))


if __name__ == "__main__":
    main()
