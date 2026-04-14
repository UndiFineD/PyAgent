import time
# import os
import platform
import uuid
# import sys
from backend import PostgresBackend


class DistributedWorkerDaemon:
    def __init__(self, geo_region: str = "us-east"):
        self.backend = PostgresBackend()
        self.worker_id = f"worker-{platform.node()}-{uuid.uuid4().hex[:6]}"
        self.hostname = platform.node()
        self.capabilities = ["python", "bash", "docker", "docker-compose", "git"]
        self.geo_region = geo_region

    def start(self):
        print(f"Starting Distributed Worker Daemon: {self.worker_id} in {self.geo_region}")
        self.backend.register_worker(
            worker_id=self.worker_id,
            hostname=self.hostname,
            capabilities=self.capabilities,
            geo_region=self.geo_region
        )

        try:
            self.loop()
        except KeyboardInterrupt:
            print("Worker shutting down gracefully.")

    def loop(self):
        while True:
            # 1. Heartbeat
            self.backend.heartbeat_worker(self.worker_id)

            # 2. Claim tasks from the global DAG queue
            task = self.backend.claim_task(self.worker_id, self.capabilities)

            if task:
                print(f"Claimed Task {task['task_id']} for Agent {task['agent_name']}")
                self.execute_task(task)
            else:
                # No tasks with satisfied dependencies available
                time.sleep(2)

    def execute_task(self, task):
        # Dynamically load the module from .github/agents/code/
        try:
            print(f"Executing payload: {task['payload']}")

            import importlib.util
            import inspect
            from pathlib import Path

            agent_name = task.get('agent_name', '0master')
            code_dir = Path(__file__).resolve().parent
            module_path = code_dir / f"{agent_name}.py"

            if not module_path.exists():
                raise FileNotFoundError(f"Agent fast-path code {module_path} not found.")

            module_key = f"agent_runtime_{agent_name.replace('-', '_')}"
            spec = importlib.util.spec_from_file_location(module_key, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the agent class and execute
            agent_class = None
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.__name__ and obj.__name__.endswith("Agent"):
                    agent_class = obj
                    break

            if not agent_class:
                raise LookupError(f"No *Agent class found in {module.__name__}")

            agent_instance = agent_class()
            result = agent_instance.execute(task['payload'])

            # Mark complete in global DAG
            self.backend.mark_task_status(
                task_id=task['task_id'],
                status='completed',
                result={'output': result}
            )
            print(f"Completed Task {task['task_id']}")

        except Exception as e:
            print(f"Task Failed: {e}")
            self.backend.mark_task_status(
                task_id=task['task_id'],
                status='failed',
                error=str(e)
            )


if __name__ == "__main__":
    daemon = DistributedWorkerDaemon()
    daemon.start()
