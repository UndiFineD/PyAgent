import importlib
import sys
from pathlib import Path
import types

REPO_ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = REPO_ROOT / ".github" / "agents" / "orchestration"
sys.path.insert(0, str(CODE_DIR))
PostgresBackend = importlib.import_module("backend").PostgresBackend


class FakeCursor:
    def __init__(self, fetch_row=None, rowcount=1, fetch_rows=None):
        self.exec_calls = []
        self._fetch_row = fetch_row
        self._rowcount = rowcount
        self._fetch_rows = fetch_rows or []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.exec_calls.append((sql, params))

    def fetchone(self):
        return self._fetch_row

    def fetchall(self):
        return self._fetch_rows

    @property
    def rowcount(self):
        return self._rowcount


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


def test_reassign_zombie_tasks_and_claim_task(monkeypatch, tmp_path):
    # Prepare fake psycopg module
    fake_cursor = FakeCursor()
    fake_conn = FakeConnection(fake_cursor)

    def fake_connect(conn_str):
        return fake_conn

    fake_psycopg = types.SimpleNamespace(connect=fake_connect)
    monkeypatch.setitem(sys.modules, "psycopg", fake_psycopg)

    backend = PostgresBackend()
    backend.conn_str = "postgres://user@localhost/db"

    # Test reassign_zombie_tasks: should call execute with the interval param as string
    count = backend.reassign_zombie_tasks(5)
    assert count == 1
    assert fake_cursor.exec_calls, "No DB exec calls recorded"
    last_sql, last_params = fake_cursor.exec_calls[-1]
    assert isinstance(last_params, tuple)
    assert last_params[0] == "5"

    # Test claim_task: produce a row from fetchone
    fake_cursor._fetch_row = ("task123", "intent1", "fleet", {"payload": True}, None)
    result = backend.claim_task("worker-1")
    assert result is not None
    assert result.get("task_id") == "task123"


def test_fetch_db_pending_tasks_preserves_agent_and_provider(monkeypatch):
    fake_cursor = FakeCursor(
        fetch_rows=[
            (
                "task-1",
                "intent-1",
                "4plan",
                {"prompt": "plan this", "provider": "openrouter", "model": "anthropic/claude-opus-4.6"},
                ["dep-1"],
            )
        ]
    )
    fake_conn = FakeConnection(fake_cursor)

    def fake_connect(conn_str):
        return fake_conn

    fake_psycopg = types.SimpleNamespace(connect=fake_connect)
    monkeypatch.setitem(sys.modules, "psycopg", fake_psycopg)

    backend = PostgresBackend()
    backend.conn_str = "postgres://user@localhost/db"

    tasks = backend._fetch_db_pending_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert task["task_id"] == "task-1"
    assert task["intent_id"] == "intent-1"
    assert task["agent"] == "4plan"
    assert task["agent_name"] == "4plan"
    assert task["provider"] == "openrouter"
    assert task["model"] == "anthropic/claude-opus-4.6"
