from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PostgresBackend:
    """Runtime backend for fast-path agent execution with file and DB fallbacks."""

    def __init__(self) -> None:
        self.conn_str = os.getenv("DATABASE_URL", "")
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
        if isinstance(file_overrides, dict):
            agent_overrides = file_overrides.get(agent_name, {})
            if isinstance(agent_overrides, dict):
                overrides.update(agent_overrides)

        db_overrides = self._fetch_db_rule_override(agent_name)
        if isinstance(db_overrides, dict):
            overrides.update(db_overrides)
        return overrides

    def get_pending_tasks(self) -> list[dict[str, Any]]:
        """Load pending work from local queue files and optional PostgreSQL."""
        tasks: list[dict[str, Any]] = []
        file_tasks = self._read_json(self.pending_tasks_path, [])
        if isinstance(file_tasks, list):
            tasks.extend(
                task
                for task in file_tasks
                if isinstance(task, dict) and str(task.get("status", "pending")).lower() == "pending"
            )

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
            agent_cache = cache_data.get(agent_name, {})
            if isinstance(agent_cache, dict):
                cached = agent_cache.get(signature)
                if isinstance(cached, dict):
                    return cached

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
        agent_cache = cache_data.setdefault(agent_name, {})
        if isinstance(agent_cache, dict):
            agent_cache[signature] = {
                "signature": signature,
                "task": task,
                "result": result,
                "updated_at": now,
            }
        self._write_json(self.execution_cache_path, cache_data)
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
            updated_tasks: list[dict[str, Any]] = []
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                current_id = str(task.get("task_id") or task.get("id") or "")
                if current_id == task_id:
                    task["status"] = status
                    task["updated_at"] = self._utc_now()
                    if result is not None:
                        task["last_result"] = result
                    if error is not None:
                        task["last_error"] = error
                updated_tasks.append(task)
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
        event = {
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
        with history_path.open("a", encoding="utf-8") as handle:
            handle.write(
                f"\n### Runtime Memory - {timestamp}\n"
                f"- Summary: {summary}\n"
                f"- Metadata: `{json.dumps(metadata, sort_keys=True, default=str)}`\n"
            )
        self._store_db_memory_entry(agent_name, summary, metadata, timestamp)

    def _extract_tasks_from_kanban(self, kanban_data: Any) -> list[dict[str, Any]]:
        if not isinstance(kanban_data, dict):
            return []
        raw_tasks = kanban_data.get("tasks", [])
        if not isinstance(raw_tasks, list):
            return []

        normalized: list[dict[str, Any]] = []
        for task in raw_tasks:
            if not isinstance(task, dict):
                continue
            lane = str(task.get("lane", "")).lower()
            status = str(task.get("status", "")).lower()
            if lane in {"done", "released", "archive"} or status in {"done", "released", "closed"}:
                continue
            normalized.append(task)
        return normalized

    def _fetch_db_rule_override(self, agent_name: str) -> dict[str, Any]:
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
            return payload
        if isinstance(payload, str):
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                self._log("backend", f"Invalid JSON override payload for {agent_name}")
        return {}

    def _fetch_db_pending_tasks(self) -> list[dict[str, Any]]:
        if not self.conn_str:
            return []
        try:
            import psycopg  # type: ignore
        except Exception:
            return []

        try:
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT payload_json
                        FROM agent_pending_tasks
                        WHERE status = 'pending'
                        ORDER BY priority DESC, created_at ASC
                        LIMIT 100
                        """
                    )
                    rows = cursor.fetchall()
        except Exception as exc:
            self._log("backend", f"PostgreSQL task lookup failed: {exc}")
            return []

        tasks: list[dict[str, Any]] = []
        for (payload,) in rows:
            if isinstance(payload, dict):
                tasks.append(payload)
            elif isinstance(payload, str):
                try:
                    decoded = json.loads(payload)
                except json.JSONDecodeError:
                    self._log("backend", "Invalid JSON task payload encountered.")
                    continue
                if isinstance(decoded, dict):
                    tasks.append(decoded)
        return tasks

    def _fetch_db_cached_result(self, agent_name: str, signature: str) -> dict[str, Any] | None:
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
            payload.setdefault("updated_at", str(updated_at))
            return payload
        return None

    def _store_db_cached_result(
        self,
        agent_name: str,
        signature: str,
        task: dict[str, Any],
        result: dict[str, Any],
        updated_at: str,
    ) -> None:
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
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            self._log("backend", f"Failed to read JSON from {path}: {exc}")
            return default

    def _write_json(self, path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    def _deduplicate_tasks(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for task in tasks:
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
        timestamp = datetime.now(timezone.utc).isoformat()
        log_path = self.log_dir / f"{source}.log.md"
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{timestamp}] {message}\n")

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def register_worker(self, worker_id: str, hostname: str, capabilities: list[str], geo_region: str = 'local') -> None:
        """Register or update a distributed worker node."""
        if not self.conn_str:
            return
        try:
            import psycopg
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        '''
                        INSERT INTO distributed_workers (worker_id, hostname, capabilities, geo_region, status, last_heartbeat)
                        VALUES (%s, %s, %s::jsonb, %s, 'active', CURRENT_TIMESTAMP)
                        ON CONFLICT (worker_id) DO UPDATE SET
                            hostname = EXCLUDED.hostname,
                            capabilities = EXCLUDED.capabilities,
                            geo_region = EXCLUDED.geo_region,
                            last_heartbeat = CURRENT_TIMESTAMP,
                            status = 'active'
                        ''' ,
                        (worker_id, hostname, json.dumps(capabilities), geo_region)
                    )
                connection.commit()
        except Exception as exc:
            self._log("backend", f"Failed to register worker {worker_id}: {exc}")

    def heartbeat_worker(self, worker_id: str) -> None:
        """Emit a heartbeat for a worker, keeping it active in the global pool."""
        if not self.conn_str:
            return
        try:
            import psycopg
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        '''
                        UPDATE distributed_workers
                        SET last_heartbeat = CURRENT_TIMESTAMP
                        WHERE worker_id = %s
                        ''',
                        (worker_id,)
                    )
                connection.commit()
        except Exception as exc:
            self._log("backend", f"Failed worker heartbeat {worker_id}: {exc}")

    def claim_task(self, worker_id: str, capabilities: list[str] | None = None) -> dict | None:
        """Atomically claim a task whose DAG dependencies are fully completed."""
        if not self.conn_str:
            return None
        
        try:
            import psycopg
            # Query complex DAG logic: 
            # 1. Status is pending
            # 2. No dependencies OR all dependencies have status 'completed'
            # 3. Atomically update status to 'claimed' and return payload
            
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        '''
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
                        ''',
                        (worker_id,)
                    )
                    row = cursor.fetchone()
                connection.commit()
                if row:
                    return {
                        "task_id": row[0],
                        "intent_id": row[1],
                        "agent_name": row[2],
                        "payload": row[3],
                        "dependencies": row[4]
                    }
        except Exception as exc:
            self._log("backend", f"Failed to claim task for {worker_id}: {exc}")
        return None

    def reassign_zombie_tasks(self, timeout_minutes: int = 5) -> int:
        """Self-healing mechanism to reclaim tasks from dead workers."""
        if not self.conn_str:
            return 0
        try:
            import psycopg
            with psycopg.connect(self.conn_str) as connection:
                with connection.cursor() as cursor:
                    # Find claimed tasks where the assigned worker hasn't heartbeated in X minutes
                    cursor.execute(
                        '''
                        UPDATE agent_pending_tasks
                        SET status = 'pending', assigned_worker_id = NULL
                        WHERE status = 'claimed'
                        AND assigned_worker_id IN (
                            SELECT worker_id FROM distributed_workers 
                            WHERE last_heartbeat < (CURRENT_TIMESTAMP - INTERVAL '%s minutes')
                        )
                        ''',
                        (timeout_minutes,)
                    )
                    count = cursor.rowcount
                connection.commit()
                if count > 0:
                    self._log("backend", f"Self-healed {count} zombie tasks back to pending queue.")
                return count
        except Exception as exc:
            self._log("backend", f"Failed to run self-healing zombie task recovery: {exc}")
            return 0
