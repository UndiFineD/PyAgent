import sys
import time
import platform
import uuid
import traceback
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "code"))
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
            self.backend._log("daemon", f"Worker {self.worker_id} shutdown gracefully.")

    def loop(self):
        while True:
            try:
                # 1. Heartbeat to stay alive in global registry
                self.backend.heartbeat_worker(self.worker_id)
                
                # 2. Self Healer - Only run occasionally (using simple random or modulo in real app, here we just call it)
                if int(time.time()) % 60 == 0:
                    self.backend.reassign_zombie_tasks(timeout_minutes=5)

                # 3. Claim tasks from the global DAG queue
                task = self.backend.claim_task(self.worker_id, self.capabilities)

                if task:
                    print(f"Claimed Task {task['task_id']} for Agent {task['agent_name']}")
                    self.execute_task(task)
                else:
                    # No tasks with satisfied dependencies available
                    time.sleep(2)
            
            except Exception as e:
                # SUPERVISOR: Self-healing crash protection
                error_trace = traceback.format_exc()
                print(f"Daemon Loop Exception: {e}")
                self.backend._log("daemon", f"Worker {self.worker_id} Loop Crashed: {error_trace}")
                print("Self-healing: Daemon waiting 5 seconds before restarting loop...")
                time.sleep(5)

    def execute_task(self, task):
        # Dynamically load the module from .github/agents/code/
        try:
            print(f"Executing payload: {task['payload']}")

            import importlib.util
            import inspect

            agent_name = task.get('agent_name', '0master')
            code_dir = Path(__file__).resolve().parents[1] / "code"
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
            
            # Defensive execution
            try:
                result = agent_instance.execute(task['payload'])
            except Exception as internal_err:
                raise RuntimeError(f"Agent execution crashed: {internal_err}")

            # Mark complete in global DAG
            self.backend.mark_task_status(
                task_id=task['task_id'],
                status='completed',
                result={'output': result}
            )
            print(f"Completed Task {task['task_id']}")

        except Exception as e:
            print(f"Task Failed: {e}")
            error_msg = str(e) + "\n" + traceback.format_exc()
            self.backend.mark_task_status(
                task_id=task['task_id'],
                status='failed',
                error=error_msg
            )

if __name__ == "__main__":
    daemon = DistributedWorkerDaemon()
    daemon.start()
