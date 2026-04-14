import json
import uuid
from typing import Any, cast

try:
    from .backend import PostgresBackend
except Exception:  # pragma: no cover - allow importing as top-level module in tests
    from backend import PostgresBackend


class IntentDecomposer:
    """Takes a high-level intent and breaks it down into a DAG of agent tasks."""

    def __init__(self) -> None:
        self.backend = PostgresBackend()

    def create_intent(self, description: str) -> str:
        intent_id = f"intent-{uuid.uuid4().hex[:8]}"
        if not self.backend.conn_str:
            print("No database connection. Intents require Postgres.")
            return intent_id

        try:
            import psycopg

            with psycopg.connect(self.backend.conn_str) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO global_intents (intent_id, description) VALUES (%s, %s)", (intent_id, description)
                    )
                connection.commit()
            print(f"Created Global Intent: {intent_id}")
            return intent_id
        except Exception as exc:
            print(f"Failed to create intent: {exc}")
            raise

    def _normalize_task_payload(self, task: dict[str, Any]) -> dict[str, Any]:
        """Merge routing metadata into payload so provider/model selections survive queuing.

        The queue schema stores `agent_name` separately, but any LLM routing fields
        need to remain inside payload_json for downstream agents.
        """
        raw_payload = task.get("payload", {})
        if isinstance(raw_payload, dict):
            payload: dict[str, Any] = cast(dict[str, Any], raw_payload)
        else:
            payload = {"value": raw_payload}

        for key in ("provider", "model", "base_url", "api_mode"):
            if key in task and key not in payload:
                payload[key] = task[key]
        return payload

    def decompose_and_queue(self, intent_id: str, tasks: list[dict[str, Any]]) -> None:
        """
        Tasks format:
        [
            {
               "internal_id": "step1",
               "agent": "4plan",
               "payload": {"title": "Design global DB schema"},
               "depends_on": []
            },
            {
               "internal_id": "step2",
               "agent": "6code",
               "payload": {"title": "Implement schema"},
               "depends_on": ["step1"]
            }
        ]
        """
        if not self.backend.conn_str:
            return

        # Map internal IDs to global task UUIDs to wire up dependencies
        task_map: dict[str, str] = {}
        for t in tasks:
            task_map[t["internal_id"]] = f"task-{uuid.uuid4().hex[:12]}"

        try:
            import psycopg

            with psycopg.connect(self.backend.conn_str) as connection:
                with connection.cursor() as cursor:
                    for t in tasks:
                        global_task_id = task_map[t["internal_id"]]
                        # Resolve dependencies to global IDs (typed)
                        deps_raw: Any = t.get("depends_on", [])
                        dependencies: list[str] = []
                        if isinstance(deps_raw, list):
                            deps_raw_list: list[Any] = cast(list[Any], deps_raw)
                            for dep in deps_raw_list:
                                if isinstance(dep, str):
                                    dependencies.append(task_map[dep])

                        payload = self._normalize_task_payload(t)
                        agent_name = str(t.get("agent", ""))

                        params = (
                            global_task_id,
                            intent_id,
                            agent_name,
                            json.dumps(payload),
                            json.dumps(dependencies),
                        )

                        cursor.execute(
                            """
                            INSERT INTO agent_pending_tasks
                            (task_id, intent_id, agent_name, payload_json, status, dependencies)
                            VALUES (%s, %s, %s, %s::jsonb, 'pending', %s::jsonb)
                            """,
                            params,
                        )

                    # Mark intent as active
                    cursor.execute("UPDATE global_intents SET status = 'active' WHERE intent_id = %s", (intent_id,))
                connection.commit()
            print(f"Successfully decomposed {len(tasks)} tasks into Intent {intent_id}")
        except Exception as exc:
            print(f"Failed to decompose intent: {exc}")


if __name__ == "__main__":
    print("Intent Decomposer Module Loaded")
