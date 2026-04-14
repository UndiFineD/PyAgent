import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATION_DIR = REPO_ROOT / ".github" / "agents" / "orchestration"
sys.path.insert(0, str(ORCHESTRATION_DIR))

fleetmanager_module = importlib.import_module("fleetmanager")


def test_dispatch_task_preserves_routing_metadata(monkeypatch):
    class FakeAgent:
        def execute(self, task):
            return {"seen_provider": task.get("provider"), "seen_model": task.get("model")}

    monkeypatch.setattr(fleetmanager_module, "load_agent_module", lambda name: object())
    monkeypatch.setattr(fleetmanager_module, "find_agent_class", lambda module: FakeAgent)

    task = {
        "task_id": "task-1",
        "agent_name": "workflow",
        "provider": "openrouter",
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "base_url": "https://openrouter.ai/api/v1",
        "api_mode": "chat_completions",
    }
    result = fleetmanager_module.dispatch_task(task)

    assert result["agent"] == "workflow"
    assert result["provider"] == "openrouter"
    assert result["model"] == "nvidia/nemotron-3-super-120b-a12b:free"
    assert result["result"]["seen_provider"] == "openrouter"


def test_main_reuses_cached_result(monkeypatch):
    events = []
    memory_entries = []

    class FakeBackend:
        def get_pending_tasks(self):
            return [{"task_id": "task-1", "agent": "fleet", "prompt": "do work"}]

        def build_task_signature(self, agent_name, task):
            return "sig-1"

        def get_cached_result(self, agent_name, signature):
            return {"result": {"status": "cached"}}

        def record_execution_event(self, agent_name, task, status, result, error):
            events.append((agent_name, status, result, error))

        def append_memory_entry(self, agent_name, summary, metadata):
            memory_entries.append((agent_name, summary, metadata))

    monkeypatch.setattr(fleetmanager_module, "PostgresBackend", lambda: FakeBackend())
    monkeypatch.setattr(sys, "argv", ["fleetmanager.py", "--limit", "1"])

    exit_code = fleetmanager_module.main()
    assert exit_code == 0
    assert events and events[0][1] == "cached"
    assert memory_entries and memory_entries[0][2]["mode"] == "cache_reuse"


def test_main_marks_failures(monkeypatch):
    status_updates = []
    events = []

    class FakeBackend:
        def get_pending_tasks(self):
            return [{"task_id": "task-2", "agent": "fleet", "prompt": "do work"}]

        def build_task_signature(self, agent_name, task):
            return "sig-2"

        def get_cached_result(self, agent_name, signature):
            return None

        def mark_task_status(self, task_id, status, result=None, error=None):
            status_updates.append((task_id, status, result, error))

        def store_cached_result(self, agent_name, signature, task, result):
            raise AssertionError("store_cached_result should not be called on failure")

        def record_execution_event(self, agent_name, task, status, result, error):
            events.append((agent_name, status, result, error))

        def append_memory_entry(self, agent_name, summary, metadata):
            pass

    monkeypatch.setattr(fleetmanager_module, "PostgresBackend", lambda: FakeBackend())

    def fail_dispatch(task):
        raise RuntimeError("dispatch exploded")

    monkeypatch.setattr(fleetmanager_module, "dispatch_task", fail_dispatch)
    monkeypatch.setattr(sys, "argv", ["fleetmanager.py", "--limit", "1"])

    exit_code = fleetmanager_module.main()
    assert exit_code == 1
    assert status_updates[0][1] == "processing"
    assert status_updates[1][1] == "failed"
    assert "dispatch exploded" in status_updates[1][3]
    assert events[-1][1] == "failed"
