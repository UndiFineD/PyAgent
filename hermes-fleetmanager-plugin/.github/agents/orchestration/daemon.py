import importlib
import importlib.util
import inspect
import platform
import time
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from backend import PostgresBackend
except Exception:  # pragma: no cover - allow importing as top-level module in tests
    try:
        from .backend import PostgresBackend
    except Exception:
        PostgresBackend = None  # type: ignore

try:
    from .loader import find_agent_class, load_agent_module
except Exception:  # pragma: no cover - allow importing as top-level module in tests
    try:
        from loader import find_agent_class, load_agent_module
    except Exception:
        find_agent_class = None  # type: ignore
        load_agent_module = None  # type: ignore


class DistributedWorkerDaemon:
    """Worker loop that claims and executes queued orchestration tasks."""

    def __init__(self, geo_region: str = "us-east"):
        if PostgresBackend is None:
            raise RuntimeError("PostgresBackend implementation not available")
        self.backend = PostgresBackend()
        self.worker_id = f"worker-{platform.node()}-{uuid.uuid4().hex[:6]}"
        self.hostname = platform.node()
        self.capabilities = ["python", "bash", "docker", "docker-compose", "git"]
        self.geo_region = geo_region

    def start(self) -> None:
        print(f"Starting Distributed Worker Daemon: {self.worker_id} in {self.geo_region}")
        self.backend.register_worker(
            worker_id=self.worker_id,
            hostname=self.hostname,
            capabilities=self.capabilities,
            geo_region=self.geo_region,
        )

        try:
            self.loop()
        except KeyboardInterrupt:
            print("Worker shutting down gracefully.")
            self.backend.log("daemon", f"Worker {self.worker_id} shutdown gracefully.")

    def loop(self) -> None:
        while True:
            try:
                self.backend.heartbeat_worker(self.worker_id)

                if int(time.time()) % 60 == 0:
                    self.backend.reassign_zombie_tasks(timeout_minutes=5)

                task: Optional[Dict[str, Any]] = self.backend.claim_task(self.worker_id, self.capabilities)

                if task:
                    print(f"Claimed Task {task['task_id']} for Agent {task['agent_name']}")
                    self.execute_task(task)
                else:
                    time.sleep(2)

            except Exception as exc:
                error_trace = traceback.format_exc()
                print(f"Daemon Loop Exception: {exc}")
                self.backend.log("daemon", f"Worker {self.worker_id} Loop Crashed: {error_trace}")
                print("Self-healing: Daemon waiting 5 seconds before restarting loop...")
                time.sleep(5)

    def _load_agent_class(self, agent_name: str):
        try:
            from loader import find_agent_class, load_agent_module

            module = load_agent_module(agent_name)
            return find_agent_class(module)
        except Exception:
            code_dir = Path(__file__).resolve().parents[1] / "code"
            module_path = code_dir / f"{agent_name}.py"

            if not module_path.exists():
                raise FileNotFoundError(f"Agent fast-path code {module_path} not found.")

            module_key = f"agent_runtime_{agent_name.replace('-', '_')}"
            spec = importlib.util.spec_from_file_location(module_key, module_path)
            if spec is None or getattr(spec, "loader", None) is None:
                raise ImportError(f"Cannot load spec for {module_path}")
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.__name__ and obj.__name__.endswith("Agent"):
                    return obj
            raise LookupError(f"No *Agent class found for agent '{agent_name}'")

    def execute_task(self, task: dict[str, Any]) -> None:
        try:
            print(f"Executing payload: {task.get('payload')}")

            agent_name = str(task.get("agent_name") or task.get("agent") or "0master")
            agent_class = self._load_agent_class(agent_name)
            agent_instance = agent_class()

            try:
                result = agent_instance.execute(task)
            except Exception as internal_err:
                raise RuntimeError(f"Agent execution crashed: {internal_err}") from internal_err

            self.backend.mark_task_status(
                task_id=task["task_id"],
                status="completed",
                result={"output": result},
            )
            print(f"Completed Task {task['task_id']}")

        except Exception as exc:
            print(f"Task Failed: {exc}")
            error_msg = str(exc) + "\n" + traceback.format_exc()
            self.backend.mark_task_status(
                task_id=task["task_id"],
                status="failed",
                error=error_msg,
            )


if __name__ == "__main__":
    daemon = DistributedWorkerDaemon()
    daemon.start()
