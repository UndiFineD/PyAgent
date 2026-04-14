import sys 
import uuid
import json
sys.path.append(".github/agents/code"); from backend import PostgresBackend



class IntentDecomposer:
    """Takes a high-level intent and breaks it down into a DAG of agent tasks."""
    
    def __init__(self):
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
                        "INSERT INTO global_intents (intent_id, description) VALUES (%s, %s)",
                        (intent_id, description)
                    )
                connection.commit()
            print(f"Created Global Intent: {intent_id}")
            return intent_id
        except Exception as exc:
            print(f"Failed to create intent: {exc}")
            raise
    
    def decompose_and_queue(self, intent_id: str, tasks: list[dict]):
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
        task_map = {}
        for t in tasks:
            task_map[t["internal_id"]] = f"task-{uuid.uuid4().hex[:12]}"
            
        try:
            import psycopg
            with psycopg.connect(self.backend.conn_str) as connection:
                with connection.cursor() as cursor:
                    for t in tasks:
                        global_task_id = task_map[t["internal_id"]]
                        # Resolve dependencies to global IDs
                        dependencies = [task_map[dep] for dep in t.get("depends_on", [])]
                        
                        cursor.execute(
                            '''
                            INSERT INTO agent_pending_tasks 
                            (task_id, intent_id, agent_name, payload_json, status, dependencies)
                            VALUES (%s, %s, %s, %s::jsonb, 'pending', %s::jsonb)
                            ''',
                            (
                                global_task_id,
                                intent_id,
                                t["agent"],
                                json.dumps(t["payload"]),
                                json.dumps(dependencies)
                            )
                        )
                        
                    # Mark intent as active
                    cursor.execute(
                        "UPDATE global_intents SET status = 'active' WHERE intent_id = %s",
                        (intent_id,)
                    )
                connection.commit()
            print(f"Successfully decomposed {len(tasks)} tasks into Intent {intent_id}")
        except Exception as exc:
            print(f"Failed to decompose intent: {exc}")

if __name__ == "__main__":
    print("Intent Decomposer Module Loaded")
