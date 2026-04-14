import importlib
import json
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATION_DIR = REPO_ROOT / ".github" / "agents" / "orchestration"
sys.path.insert(0, str(ORCHESTRATION_DIR))

intent_decomposer_module = importlib.import_module("intent_decomposer")
daemon_module = importlib.import_module("daemon")


class FakeCursor:
    def __init__(self):
        self.exec_calls = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.exec_calls.append((sql, params))


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def cursor(self):
        return self._cursor

    def commit(self):
        return None


def test_normalize_task_payload_preserves_provider_fields(monkeypatch):
    class FakeBackend:
        conn_str = "postgres://user@localhost/db"

    monkeypatch.setattr(intent_decomposer_module, "PostgresBackend", FakeBackend)
    decomposer = intent_decomposer_module.IntentDecomposer()
    payload = decomposer._normalize_task_payload(
        {
            "payload": {"prompt": "do work"},
            "provider": "openrouter",
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "base_url": "https://openrouter.ai/api/v1",
        }
    )
    assert payload["provider"] == "openrouter"
    assert payload["model"] == "nvidia/nemotron-3-super-120b-a12b:free"
    assert payload["base_url"] == "https://openrouter.ai/api/v1"


def test_decompose_and_queue_writes_merged_payload(monkeypatch):
    fake_cursor = FakeCursor()
    fake_conn = FakeConnection(fake_cursor)

    class FakeBackend:
        conn_str = "postgres://user@localhost/db"

    def fake_connect(conn_str):
        return fake_conn

    monkeypatch.setattr(intent_decomposer_module, "PostgresBackend", FakeBackend)
    monkeypatch.setitem(sys.modules, "psycopg", types.SimpleNamespace(connect=fake_connect))

    decomposer = intent_decomposer_module.IntentDecomposer()
    tasks = [
        {
            "internal_id": "plan",
            "agent": "4plan",
            "provider": "openrouter",
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "payload": {"prompt": "plan it"},
            "depends_on": [],
        }
    ]
    decomposer.decompose_and_queue("intent-1", tasks)

    insert_params = fake_cursor.exec_calls[0][1]
    payload_json = json.loads(insert_params[3])
    assert payload_json["provider"] == "openrouter"
    assert payload_json["model"] == "nvidia/nemotron-3-super-120b-a12b:free"


def test_daemon_execute_task_marks_success(monkeypatch):
    status_updates = []

    class FakeBackend:
        def register_worker(self, **kwargs):
            return None

        def mark_task_status(self, task_id, status, result=None, error=None):
            status_updates.append((task_id, status, result, error))

        def _log(self, source, message):
            return None

    class FakeAgent:
        def execute(self, task):
            assert task["provider"] == "openrouter"
            return {"status": "ok"}

    monkeypatch.setattr(daemon_module, "PostgresBackend", FakeBackend)
    daemon = daemon_module.DistributedWorkerDaemon()
    monkeypatch.setattr(daemon, "_load_agent_class", lambda agent_name: FakeAgent)

    daemon.execute_task(
        {
            "task_id": "task-1",
            "agent_name": "workflow",
            "provider": "openrouter",
            "payload": {"prompt": "run"},
        }
    )

    assert status_updates == [("task-1", "completed", {"output": {"status": "ok"}}, None)]


def test_daemon_execute_task_marks_failure(monkeypatch):
    status_updates = []

    class FakeBackend:
        def register_worker(self, **kwargs):
            return None

        def mark_task_status(self, task_id, status, result=None, error=None):
            status_updates.append((task_id, status, result, error))

        def _log(self, source, message):
            return None

    class FakeAgent:
        def execute(self, task):
            raise RuntimeError("boom")

    monkeypatch.setattr(daemon_module, "PostgresBackend", FakeBackend)
    daemon = daemon_module.DistributedWorkerDaemon()
    monkeypatch.setattr(daemon, "_load_agent_class", lambda agent_name: FakeAgent)

    daemon.execute_task({"task_id": "task-2", "agent_name": "workflow", "payload": {"prompt": "run"}})

    assert status_updates[0][1] == "failed"
    assert "boom" in status_updates[0][3]
