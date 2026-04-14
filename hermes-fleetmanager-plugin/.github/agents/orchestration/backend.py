from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, cast, Callable, TypeVar, TYPE_CHECKING, Protocol
import time
import re

# Generic return type for DB operations (module-level so analyzers see it)
R = TypeVar("R")

# Prefer concrete psycopg types when type-checking; otherwise provide
# lightweight Protocols at module scope so static analyzers and callables
# in methods can reference `DBConn` / `DBCursor` unambiguously.
if TYPE_CHECKING:
    try:
        from psycopg import Connection as DBConn, Cursor as DBCursor  # type: ignore
    except Exception:  # pragma: no cover - typing-only fallback

        class DBConn(Protocol):  # type: ignore
            def cursor(self, *args: Any, **kwargs: Any) -> Any: ...

            def commit(self, *args: Any, **kwargs: Any) -> None: ...

        class DBCursor(Protocol):  # type: ignore
            def execute(self, *args: Any, **kwargs: Any) -> Any: ...

            def fetchone(self, *args: Any, **kwargs: Any) -> Any: ...

            def fetchall(self, *args: Any, **kwargs: Any) -> Any: ...

            @property
            def rowcount(self) -> int | None: ...

else:

    class DBConn(Protocol):
        def cursor(self, *args: Any, **kwargs: Any) -> Any: ...

        def commit(self, *args: Any, **kwargs: Any) -> None: ...

    class DBCursor(Protocol):
        def execute(self, *args: Any, **kwargs: Any) -> Any: ...

        def fetchone(self, *args: Any, **kwargs: Any) -> Any: ...

        def fetchall(self, *args: Any, **kwargs: Any) -> Any: ...

        @property
        def rowcount(self) -> int | None: ...


class PostgresBackend:
    """Runtime backend for fast-path agent execution with file and DB fallbacks."""

    def __init__(self) -> None:
        """Initialize backend with environment-configured PostgreSQL connection and file paths."""
        self.conn_str = os.getenv("DATABASE_URL", "")
        root_override = os.getenv("AGENTS_ROOT")
        if root_override:
            self.root_dir = Path(root_override)
        else:
            self.root_dir = Path(__file__).resolve().parents[1]
        self.governance_dir = self.root_dir / "governance"
        self.log_dir = self.root_dir / "log"
        self.memory_dir = self.root_dir / "memory"
        self.data_dir = self.root_dir / "data"
        self.kanban_path = self.root_dir / "kanban" / "kanban.json"
        self.override_path = self.governance_dir / "agent_overrides.json"
        self.pending_tasks_path = self.data_dir / "pending_tasks.json"
        self.execution_cache_path = self.data_dir / "execution_cache.json"
        self.execution_events_path = self.log_dir / "execution_events.jsonl"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def get_rule_overrides(self, agent_name: str) -> dict[str, Any]:
        """Load fast-path overrides with precedence: file defaults, then PostgreSQL."""
        overrides: dict[str, Any] = {}
        file_overrides = self._read_json(self.override_path, {})
        agent_overrides: Any | None = None
        if isinstance(file_overrides, dict):
            file_overrides_typed: dict[str, Any] = cast(dict[str, Any], file_overrides)
            agent_overrides = file_overrides_typed.get(agent_name)
        if isinstance(agent_overrides, dict):
            overrides.update(cast(dict[str, Any], agent_overrides))

        db_overrides = self._fetch_db_rule_override(agent_name)
        overrides.update(db_overrides)
        return overrides

    def get_pending_tasks(self) -> list[dict[str, Any]]:
        """Load pending work from local queue files and optional PostgreSQL."""
        tasks: list[dict[str, Any]] = []
        file_tasks = self._read_json(self.pending_tasks_path, [])
        if isinstance(file_tasks, list):
            file_tasks_typed: list[Any] = cast(list[Any], file_tasks)
            filtered: list[dict[str, Any]] = []
            for item in file_tasks_typed:
                if not isinstance(item, dict):
                    continue
                item_typed = cast(dict[str, Any], item)
                if str(item_typed.get("status", "pending")).lower() == "pending":
                    filtered.append(item_typed)
            tasks.extend(filtered)

        kanban_data = self._read_json(self.kanban_path, {"tasks": []})
        tasks.extend(self._extract_tasks_from_kanban(kanban_data))
        tasks.extend(self._fetch_db_pending_tasks())
        return self._deduplicate_tasks(tasks)

    def build_task_signature(self, agent_name: str, task: dict[str, Any]) -> str:
        """Create a stable signature for cache reuse across runs."""
        relevant_task = {
            key: value
            for key, value in task.items()
            if key not in {"created_at", "updated_at", "task_id", "id", "status", "attempts"}
        }
        serialized = json.dumps(
            {"agent": agent_name, "task": relevant_task},
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def get_cached_result(self, agent_name: str, signature: str) -> dict[str, Any] | None:
        """Return a cached result from files first, then PostgreSQL."""
        cache_data = self._read_json(self.execution_cache_path, {})
        if isinstance(cache_data, dict):
            cache_data_typed: dict[str, Any] = cast(dict[str, Any], cache_data)
            agent_cache_any = cache_data_typed.get(agent_name)
            if isinstance(agent_cache_any, dict):
                agent_cache = cast(dict[str, Any], agent_cache_any)
                cached = agent_cache.get(signature)
                if isinstance(cached, dict):
                    return cast(dict[str, Any], cached)

        db_cached = self._fetch_db_cached_result(agent_name, signature)
        if isinstance(db_cached, dict):
            return db_cached
        return None

    def store_cached_result(
        self,
        agent_name: str,
        signature: str,
        task: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        """Persist reusable results to both file backup and PostgreSQL."""
        now = self._utc_now()
        cache_data = self._read_json(self.execution_cache_path, {})
        if not isinstance(cache_data, dict):
            cache_data = {}
        cache_data_typed: dict[str, Any] = cast(dict[str, Any], cache_data)
        agent_cache_any = cache_data_typed.setdefault(agent_name, {})
        if isinstance(agent_cache_any, dict):
            agent_cache = cast(dict[str, Any], agent_cache_any)
            agent_cache[signature] = {
                "signature": signature,
                "task": task,
                "result": result,
                "updated_at": now,
            }
        self._write_json(self.execution_cache_path, cache_data_typed)
        self._store_db_cached_result(agent_name, signature, task, result, now)

    def mark_task_status(
        self,
        task_id: str,
        status: str,
        result: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        """Persist queue status changes to file backup and PostgreSQL."""
        tasks = self._read_json(self.pending_tasks_path, [])
        if isinstance(tasks, list):
            file_tasks_typed: list[Any] = cast(list[Any], tasks)
            updated_tasks: list[dict[str, Any]] = []
            for item in file_tasks_typed:
                if not isinstance(item, dict):
                    continue
                task_typed: dict[str, Any] = cast(dict[str, Any], item)
                current_id = str(task_typed.get("task_id") or task_typed.get("id") or "")
                if current_id == task_id:
                    task_typed["status"] = status
                    task_typed["updated_at"] = self._utc_now()
                    if result is not None:
                        task_typed["last_result"] = result
                    if error is not None:
                        task_typed["last_error"] = error
                updated_tasks.append(task_typed)
            self._write_json(self.pending_tasks_path, updated_tasks)

        self._store_db_task_status(task_id, status, result, error)

    def record_execution_event(
        self,
        agent_name: str,
        task: dict[str, Any],
        status: str,
        result: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        """Write execution events to file logs and PostgreSQL."""
        event: dict[str, Any] = {
            "agent": agent_name,
            "task_id": task.get("task_id") or task.get("id"),
            "title": task.get("title"),
            "status": status,
            "result": result,
            "error": error,
            "timestamp": self._utc_now(),
        }
        with self.execution_events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, default=str) + "\n")
        self._store_db_execution_event(event)

    def append_memory_entry(
        self,
        agent_name: str,
        summary: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Persist compact reusable memory entries to file backup and PostgreSQL."""
        metadata = metadata or {}
        timestamp = self._utc_now()
        history_path = self.memory_dir / f"history.{agent_name}.memory.md"
        redacted = self._redact_metadata(metadata)
        with history_path.open("a", encoding="utf-8") as handle:
            handle.write(
                f"\n### Runtime Memory - {timestamp}\n"
                f"- Summary: {summary}\n"
                f"- Metadata: `{json.dumps(redacted, sort_keys=True, default=str)}`\n"
            )
        # emit a lightweight metric and store DB entry
        self._increment_metric("memory_entries_written")
        self._store_db_memory_entry(agent_name, summary, redacted, timestamp)

    def _redact_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """Return a redacted copy of metadata, masking common secret keys and truncating long values."""
        secret_keys = re.compile(r"(secret|token|password|passwd|api[_-]?key|credential|auth)", re.I)

        def redact_value(val: Any) -> Any:
            """Redact string values that look like secrets and truncate long strings for log safety."""
            if isinstance(val, str):
                if len(val) > 200:
                    return val[:200] + "...[truncated]"
                return val
            if isinstance(val, dict):
                val_dict: dict[str, Any] = cast(dict[str, Any], val)
                out_dict: dict[str, Any] = {}
                for k, v in val_dict.items():
                    out_dict[str(k)] = redact_value(v)
                return out_dict
            if isinstance(val, list):
                val_list: list[Any] = cast(list[Any], val)
                out_list: list[Any] = []
                for v in val_list:
                    out_list.append(redact_value(v))
                return out_list
            return val

        out: dict[str, Any] = {}
        for k, v in (metadata or {}).items():
            if secret_keys.search(k):
                out[k] = "[REDACTED]"
            else:
                out[k] = redact_value(v)
        return out

    def _increment_metric(self, name: str, amount: int = 1) -> None:
        """Increment a simple file-backed metric counter in the log dir."""
        metrics_path = self.log_dir / "metrics.json"
        data: Any = {}
        if metrics_path.exists():
            try:
                data = json.loads(metrics_path.read_text(encoding="utf-8"))
            except Exception:
                data = {}
        data_typed: dict[str, Any] = cast(dict[str, Any], data)
        existing = data_typed.get(name, 0)
        try:
            existing_int = int(existing)
        except Exception:
            existing_int = 0
        try:
            amount_int = int(amount)
        except Exception:
            amount_int = 0
        data_typed[name] = existing_int + amount_int
        try:
            metrics_path.write_text(json.dumps(data_typed, indent=2), encoding="utf-8")
        except Exception:
            # never fail the main flow due to metric writes
            pass

    def _extract_tasks_from_kanban(self, kanban_data: Any) -> list[dict[str, Any]]:
        """Extract tasks from kanban data, filtering out completed/released items."""
        if not isinstance(kanban_data, dict):
            return []
        kanban_typed: dict[str, Any] = cast(dict[str, Any], kanban_data)
        raw_tasks_obj = kanban_typed.get("tasks", [])
        if not isinstance(raw_tasks_obj, list):
            return []
        raw_tasks: list[Any] = cast(list[Any], raw_tasks_obj)

        normalized: list[dict[str, Any]] = []
        for task in raw_tasks:
            if not isinstance(task, dict):
                continue
            task_typed: dict[str, Any] = cast(dict[str, Any], task)
            lane = str(task_typed.get("lane", "")).lower()
            status = str(task_typed.get("status", "")).lower()
            if lane in {"done", "released", "archive"} or status in {"done", "released", "closed"}:
                continue
            normalized.append(task_typed)
        return normalized

    def _fetch_db_rule_override(self, agent_name: str) -> dict[str, Any]:
        """Fetch rule overrides for a specific agent from the database."""
        if not self.conn_str:
            return {}
        try:
            import psycopg  # type: ignore
        except Exception:
            self._log("backend", "psycopg not installed; using file-based overrides.")
            return {}

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT override_json
                        FROM agent_rule_overrides
                        WHERE agent_name = %s AND enabled = TRUE
                        ORDER BY updated_at DESC
                        LIMIT 1
                        """,
                        (agent_name,),
                    )
                    row = cursor.fetchone()
        except Exception as exc:
            self._log("backend", f"PostgreSQL override lookup failed for {agent_name}: {exc}")
            return {}

        if not row:
            return {}
        payload = row[0]
        if isinstance(payload, dict):
            return cast(dict[str, Any], payload)
        if isinstance(payload, str):
            try:
                decoded = json.loads(payload)
            except json.JSONDecodeError:
                self._log("backend", f"Invalid JSON override payload for {agent_name}")
                return {}
            if isinstance(decoded, dict):
                return cast(dict[str, Any], decoded)
            self._log("backend", f"JSON override payload for {agent_name} is not an object")
            return {}
        return {}

    def _fetch_db_pending_tasks(self) -> list[dict[str, Any]]:
        """Fetch pending tasks from the database."""
        if not self.conn_str:
            return []
        try:
            import psycopg  # type: ignore
        except Exception:
            return []

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT task_id, intent_id, agent_name, payload_json, dependencies
                        FROM agent_pending_tasks
                        WHERE status = 'pending'
                        ORDER BY priority DESC, created_at ASC
                        LIMIT 100
                        """)
                    rows = cursor.fetchall()
        except Exception as exc:
            self._log("backend", f"PostgreSQL task lookup failed: {exc}")
            return []

        tasks: list[dict[str, Any]] = []
        for row in rows:
            task_id, intent_id, agent_name, payload, dependencies = row
            task_data: dict[str, Any] | None = None
            if isinstance(payload, dict):
                task_data = cast(dict[str, Any], payload)
            elif isinstance(payload, str):
                try:
                    decoded = json.loads(payload)
                except json.JSONDecodeError:
                    self._log("backend", "Invalid JSON task payload encountered.")
                    continue
                if isinstance(decoded, dict):
                    task_data = cast(dict[str, Any], decoded)
            if task_data is None:
                continue

            task_data.setdefault("task_id", str(task_id))
            task_data.setdefault("intent_id", str(intent_id))
            task_data.setdefault("agent", str(agent_name))
            task_data.setdefault("agent_name", str(agent_name))
            task_data.setdefault("dependencies", dependencies)
            tasks.append(task_data)
        return tasks

    def _fetch_db_cached_result(self, agent_name: str, signature: str) -> dict[str, Any] | None:
        """Fetch a cached execution result from the database for a given agent and task signature."""
        if not self.conn_str:
            return None
        try:
            import psycopg  # type: ignore
        except Exception:
            return None

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT last_result, updated_at
                        FROM agent_execution_cache
                        WHERE agent_name = %s AND task_signature = %s
                        ORDER BY updated_at DESC
                        LIMIT 1
                        """,
                        (agent_name, signature),
                    )
                    row = cursor.fetchone()
        except Exception as exc:
            self._log("backend", f"PostgreSQL cache lookup failed for {agent_name}: {exc}")
            return None

        if not row:
            return None
        payload, updated_at = row
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                return None
        if isinstance(payload, dict):
            payload_typed: dict[str, Any] = cast(dict[str, Any], payload)
            payload_typed.setdefault("updated_at", str(updated_at))
            return payload_typed
        return None

    def _store_db_cached_result(
        self,
        agent_name: str,
        signature: str,
        task: dict[str, Any],
        result: dict[str, Any],
        updated_at: str,
    ) -> None:
        """Store a cached execution result in the database for a given agent and task signature."""
        if not self.conn_str:
            return
        try:
            import psycopg  # type: ignore
        except Exception:
            return

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO agent_execution_cache (
                            agent_name,
                            task_signature,
                            task_json,
                            last_result,
                            updated_at
                        ) VALUES (%s, %s, %s::jsonb, %s::jsonb, %s)
                        ON CONFLICT (agent_name, task_signature)
                        DO UPDATE SET
                            task_json = EXCLUDED.task_json,
                            last_result = EXCLUDED.last_result,
                            updated_at = EXCLUDED.updated_at
                        """,
                        (
                            agent_name,
                            signature,
                            json.dumps(task, default=str),
                            json.dumps(result, default=str),
                            updated_at,
                        ),
                    )
                connection.commit()
        except Exception as exc:
            self._log("backend", f"PostgreSQL cache write failed for {agent_name}: {exc}")

    def _store_db_task_status(
        self,
        task_id: str,
        status: str,
        result: dict[str, Any] | None,
        error: str | None,
    ) -> None:
        """Store a task status update in the database for a given task ID, with optional result and error details."""
        if not self.conn_str:
            return
        try:
            import psycopg  # type: ignore
        except Exception:
            return

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE agent_pending_tasks
                        SET status = %s,
                            last_result = COALESCE(%s::jsonb, last_result),
                            last_error = COALESCE(%s, last_error),
                            completed_at = CURRENT_TIMESTAMP
                        WHERE task_id = %s
                        """,
                        (
                            status,
                            json.dumps(result, default=str) if result is not None else None,
                            error,
                            task_id,
                        ),
                    )
                connection.commit()
        except Exception as exc:
            self._log("backend", f"PostgreSQL task status update failed for {task_id}: {exc}")

    def _store_db_execution_event(self, event: dict[str, Any]) -> None:
        """Store an execution event in the database with details about the agent, task, status, result, and error."""
        if not self.conn_str:
            return
        try:
            import psycopg  # type: ignore
        except Exception:
            return

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO agent_execution_events (
                            agent_name,
                            task_id,
                            status,
                            payload_json,
                            created_at
                        ) VALUES (%s, %s, %s, %s::jsonb, %s)
                        """,
                        (
                            event.get("agent"),
                            event.get("task_id"),
                            event.get("status"),
                            json.dumps(event, default=str),
                            event.get("timestamp"),
                        ),
                    )
                connection.commit()
        except Exception as exc:
            self._log("backend", f"PostgreSQL execution event write failed: {exc}")

    def _store_db_memory_entry(
        self,
        agent_name: str,
        summary: str,
        metadata: dict[str, Any],
        created_at: str,
    ) -> None:
        """Store a memory entry in the database for a given agent, with a summary, metadata, and timestamp."""
        if not self.conn_str:
            return
        try:
            import psycopg  # type: ignore
        except Exception:
            return

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO agent_memory_entries (
                            agent_name,
                            summary_text,
                            metadata_json,
                            created_at
                        ) VALUES (%s, %s, %s::jsonb, %s)
                        """,
                        (
                            agent_name,
                            summary,
                            json.dumps(metadata, default=str),
                            created_at,
                        ),
                    )
                connection.commit()
        except Exception as exc:
            self._log("backend", f"PostgreSQL memory write failed for {agent_name}: {exc}")

    def _read_json(self, path: Path, default: Any) -> Any:
        """Read JSON data from a file, returning a default value on failure or if the file doesn't exist."""
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            self._log("backend", f"Failed to read JSON from {path}: {exc}")
            return default

    def _write_json(self, path: Path, payload: Any) -> None:
        """Write JSON data to a file, creating parent directories if needed,
        and logging any errors without raising exceptions."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    def _deduplicate_tasks(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Deduplicate tasks based on a combination of agent, title,
        and creation time, ensuring stable signatures for cache reuse
        and preventing duplicate work."""
        seen: set[str] = set()
        deduped: list[dict[str, Any]] = []
        tasks_typed: list[dict[str, Any]] = tasks
        for task in tasks_typed:
            identifier = str(
                task.get("id")
                or task.get("task_id")
                or f"{task.get('agent', '0master')}::{task.get('title', '')}::{task.get('created_at', '')}"
            )
            if identifier in seen:
                continue
            task.setdefault("task_id", identifier)
            seen.add(identifier)
            deduped.append(task)
        return deduped

    def _log(self, source: str, message: str) -> None:
        """Append a log message to a source-specific log file with
        a timestamp, ensuring that logging failures do not disrupt the main flow."""
        timestamp = datetime.now(timezone.utc).isoformat()
        log_path = self.log_dir / f"{source}.log.md"
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{timestamp}] {message}\n")

    def log(self, source: str, message: str) -> None:
        """Public logging wrapper for external callers.

        Use this method instead of accessing the protected `_log` attribute
        from outside the class. It delegates to `_log` and safely ignores
        any logging errors to avoid disrupting runtime behavior.
        """
        try:
            self._log(source, message)
        except Exception:
            # Do not let logging failures break caller flows
            return

    def _utc_now(self) -> str:
        """Return the current UTC time as an ISO-formatted string,
        for consistent timestamping across database entries and logs."""
        return datetime.now(timezone.utc).isoformat()

    def _run_db_op(
        self, op_func: Callable[[DBConn, DBCursor], R], attempts: int = 3, backoff: float = 0.5
    ) -> Optional[R]:
        """Run a DB operation with simple retry/backoff.

        `op_func` is called with (connection, cursor) and may return a value.
        Returns the op_func return value on success, or None on failure.
        """
        if not self.conn_str:
            return None
        try:
            import psycopg  # type: ignore
        except Exception:
            self._log("backend", "psycopg not installed; skipping DB operation.")
            return None

        last_exc = None
        for attempt in range(attempts):
            try:
                with psycopg.connect(self.conn_str) as connection:
                    with connection.cursor() as cursor:
                        result = op_func(connection, cursor)
                    connection.commit()
                return result
            except Exception as exc:
                last_exc = exc
                self._log("backend", f"DB op failed (attempt {attempt+1}/{attempts}): {exc}")
                if attempt < attempts - 1:
                    time.sleep(backoff * (2**attempt))
        self._log("backend", f"DB op ultimately failed after {attempts} attempts: {last_exc}")
        return None

    def register_worker(
        self, worker_id: str, hostname: str, capabilities: list[str], geo_region: str = "local"
    ) -> None:
        """Register or update a distributed worker node."""

        def op(conn: DBConn, cursor: DBCursor) -> Any:
            """Insert or update the worker record in the distributed_workers
            table with the provided details and set status to active.
            """
            cursor.execute(
                """
                INSERT INTO distributed_workers (
                    worker_id, hostname, capabilities, geo_region, status, last_heartbeat)
                VALUES (%s, %s, %s::jsonb, %s, 'active', CURRENT_TIMESTAMP)
                ON CONFLICT (worker_id) DO UPDATE SET
                    hostname = EXCLUDED.hostname,
                    capabilities = EXCLUDED.capabilities,
                    geo_region = EXCLUDED.geo_region,
                    last_heartbeat = CURRENT_TIMESTAMP,
                    status = 'active'
                """,
                (worker_id, hostname, json.dumps(capabilities), geo_region),
            )

        res = self._run_db_op(op)
        if res is None:
            self._log("backend", f"Failed to register worker {worker_id}")

    def heartbeat_worker(self, worker_id: str) -> None:
        """Emit a heartbeat for a worker, keeping it active in the global pool."""

        def op(conn: DBConn, cursor: DBCursor) -> Any:
            """Update the last_heartbeat timestamp for the worker in
            the distributed_workers table to indicate it's still alive.
            """
            cursor.execute(
                """
                UPDATE distributed_workers
                SET last_heartbeat = CURRENT_TIMESTAMP
                WHERE worker_id = %s
                """,
                (worker_id,),
            )

        res = self._run_db_op(op)
        if res is None:
            self._log("backend", f"Failed worker heartbeat {worker_id}")

    def claim_task(self, worker_id: str, capabilities: list[str] | None = None) -> Optional[Dict[str, Any]]:
        """Atomically claim a task whose DAG dependencies are fully completed."""
        if not self.conn_str:
            return None

        def op(conn: DBConn, cursor: DBCursor) -> Any:
            """Atomically select a pending task that has all dependencies completed,
            mark it as claimed by this worker, and return its details.
            Uses SELECT FOR UPDATE SKIP LOCKED to avoid"""
            cursor.execute(
                """
                WITH available_tasks AS (
                    SELECT task_id
                    FROM agent_pending_tasks apt
                    WHERE status = 'pending'
                    AND (
                        jsonb_array_length(dependencies) = 0
                        OR NOT EXISTS (
                            SELECT 1 FROM jsonb_array_elements_text(dependencies) dep_id
                            JOIN agent_pending_tasks dep_task ON dep_task.task_id = dep_id
                            WHERE dep_task.status != 'completed'
                        )
                    )
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                )
                UPDATE agent_pending_tasks
                SET status = 'claimed',
                    assigned_worker_id = %s,
                    started_at = CURRENT_TIMESTAMP
                WHERE task_id = (SELECT task_id FROM available_tasks)
                RETURNING task_id, intent_id, agent_name, payload_json, dependencies;
                """,
                (worker_id,),
            )
            return cursor.fetchone()

        row = self._run_db_op(op)
        if row:
            return {
                "task_id": row[0],
                "intent_id": row[1],
                "agent_name": row[2],
                "payload": row[3],
                "dependencies": row[4],
            }
        return None

    def reassign_zombie_tasks(self, timeout_minutes: int = 5) -> int:
        """Self-healing mechanism to reclaim tasks from dead workers."""
        if not self.conn_str:
            return 0

        def op(conn: DBConn, cursor: DBCursor) -> Any:
            cursor.execute(
                """
                UPDATE agent_pending_tasks
                SET status = 'pending', assigned_worker_id = NULL
                WHERE status = 'claimed'
                AND assigned_worker_id IN (
                    SELECT worker_id FROM distributed_workers
                    WHERE last_heartbeat < (CURRENT_TIMESTAMP - (%s || ' minutes')::interval)
                )
                """,
                (str(timeout_minutes),),
            )
            return cursor.rowcount

        count = self._run_db_op(op) or 0
        if count > 0:
            self._log("backend", f"Self-healed {count} zombie tasks back to pending queue.")
        return count
