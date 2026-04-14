from __future__ import annotations

import argparse
import importlib.util
import inspect
import json
import sys
from pathlib import Path
from typing import Any

from backend import PostgresBackend


def load_agent_module(agent_name: str):
    code_dir = Path(__file__).resolve().parent
    module_path = code_dir / f"{agent_name}.py"
    if not module_path.exists():
        raise FileNotFoundError(f"No code module found for agent '{agent_name}'")

    module_key = f"agent_runtime_{agent_name.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_key, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module spec for {agent_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_agent_class(module):
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__ and obj.__name__.endswith("Agent"):
            return obj
    raise LookupError(f"No *Agent class found in {module.__name__}")


def dispatch_task(task: dict[str, Any]) -> dict[str, Any]:
    agent_name = str(task.get("agent") or task.get("owner") or "0master")
    module = load_agent_module(agent_name)
    agent_class = find_agent_class(module)
    agent = agent_class()
    result = agent.execute(task)
    return {
        "task_id": task.get("task_id") or task.get("id"),
        "agent": agent_name,
        "result": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Cron-friendly fleet manager for agent code modules.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of tasks to process in one run.")
    args = parser.parse_args()

    print("FleetManager: Awakening to check for pending work...")
    backend = PostgresBackend()
    tasks = backend.get_pending_tasks()
    if not tasks:
        print("FleetManager: No pending tasks found.")
        return 0

    queued_tasks = tasks[: max(args.limit, 1)]
    print(f"FleetManager: Found {len(tasks)} tasks, dispatching {len(queued_tasks)}.")
    results: list[dict[str, Any]] = []
    failures = 0
    for task in queued_tasks:
        agent_name = str(task.get("agent") or task.get("owner") or "0master")
        task_id = str(task.get("task_id") or task.get("id") or backend.build_task_signature(agent_name, task))
        task["task_id"] = task_id
        task_signature = backend.build_task_signature(agent_name, task)

        try:
            cached = backend.get_cached_result(agent_name, task_signature)
            if cached is not None:
                cache_result = {
                    "task_id": task_id,
                    "agent": agent_name,
                    "result": cached.get("result", cached),
                    "mode": "cache_reuse",
                }
                backend.record_execution_event(agent_name, task, "cached", cache_result, None)
                backend.append_memory_entry(
                    agent_name,
                    f"Reused cached execution result for task {task_id}.",
                    {"task_signature": task_signature, "mode": "cache_reuse"},
                )
                results.append(cache_result)
                continue

            backend.mark_task_status(task_id, "processing")
            dispatched = dispatch_task(task)
            backend.store_cached_result(agent_name, task_signature, task, dispatched)
            backend.mark_task_status(task_id, "completed", result=dispatched)
            backend.record_execution_event(agent_name, task, "completed", dispatched, None)
            backend.append_memory_entry(
                agent_name,
                f"Completed task {task_id} via fleetmanager dispatch.",
                {"task_signature": task_signature, "mode": dispatched.get("result", {}).get("mode")},
            )
            results.append(dispatched)
        except Exception as exc:
            failures += 1
            error_result = {
                "task_id": task_id,
                "agent": agent_name,
                "error": str(exc),
            }
            backend.mark_task_status(task_id, "failed", error=str(exc))
            backend.record_execution_event(agent_name, task, "failed", None, str(exc))
            backend.append_memory_entry(
                agent_name,
                f"Task {task_id} failed during fleetmanager dispatch.",
                {"task_signature": task_signature, "error": str(exc)},
            )
            results.append(error_result)

    print(json.dumps(results, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
