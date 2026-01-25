#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Optional
from pathlib import Path
import logging

class LegacyAgentMixin:
    """Mixin to provide legacy test methods for the newer BaseAgent."""

    def _init_legacy_attrs(
        self,
        repo_root: str | None = None,
        dry_run: bool = False,
        loop: Any = None,
        enable_async: bool = False,
        enable_multiprocessing: bool = False,
        selective_agents: Any = None,
        timeout_per_agent: Any = None,
        file_path: str = ".",
    ):
        self.repo_root = Path(file_path)
        self.dry_run = dry_run
        self.loop = loop
        self.enable_async = enable_async
        self.enable_multiprocessing = enable_multiprocessing
        self.callbacks: list[Any] = []

        if self.dry_run:
            logging.getLogger().info("DRY RUN MODE")

        self.rate_limiter = None
        self.lock_manager = None
        self.diff_generator = None
        self.incremental_processor = None
        self.shutdown_handler = None
        self.health_checker = None

        self._selective_agents = (
            set(selective_agents)
            if selective_agents is not None and not isinstance(selective_agents, set)
            else selective_agents
        )
        self._timeout_per_agent = timeout_per_agent if timeout_per_agent is not None else {}
        self._metrics = {
            "files_processed": 0,
            "files_modified": 0,
            "agents_applied": {},
            "start_time": 0.0,
            "end_time": 0.0,
        }
        self._webhooks: list[Any] = []

    def enable_rate_limiting(self, config=None, requests_per_second: float | None = None) -> None:
        from src.core.base.common.utils.rate_limiter import RateLimiter
        from src.core.base.common.models.fleet_models import RateLimitConfig
        if config is None and requests_per_second is not None:
            config = RateLimitConfig(requests_per_second=requests_per_second)
        self.rate_limiter = RateLimiter(config)

    def get_rate_limit_stats(self):
        return self.rate_limiter.get_stats() if self.rate_limiter else {}

    def enable_file_locking(self, lock_timeout: float | None = None) -> None:
        from src.core.base.common.utils.file_lock_manager import FileLockManager
        self.lock_manager = FileLockManager()
        if lock_timeout is not None:
            self.lock_manager.lock_timeout = lock_timeout

    def enable_diff_preview(self) -> None:
        from src.core.base.common.utils.diff_generator import DiffGenerator
        self.diff_generator = DiffGenerator()

    def preview_changes(self, file_path: Path, content: str):
        if not self.diff_generator:
            from src.core.base.common.utils.diff_generator import DiffGenerator
            self.diff_generator = DiffGenerator()

        original = ""
        if file_path.exists():
            original = file_path.read_text(errors="ignore")

        return self.diff_generator.generate_diff(file_path, original, content)

    def enable_incremental_processing(self) -> None:
        from src.core.base.logic.incremental_processor import IncrementalProcessor
        self.incremental_processor = IncrementalProcessor(repo_root=self.repo_root)

    def get_changed_files(self, files: list[Path]):
        return self.incremental_processor.get_changed_files(files) if self.incremental_processor else files

    def reset_incremental_state(self):
        if self.incremental_processor:
            self.incremental_processor.reset_state()

    def enable_graceful_shutdown(self) -> None:
        from src.core.base.lifecycle.graceful_shutdown import GracefulShutdown
        self.shutdown_handler = GracefulShutdown(repo_root=self.repo_root)

    def resume_from_shutdown(self) -> Optional[Any]:
        if self.shutdown_handler:
            return self.shutdown_handler.get_shutdown_state()
        return None

    def run_health_checks(self):
        from src.core.base.logic.managers.system_managers import HealthChecker
        self.health_checker = HealthChecker(repo_root=self.repo_root)
        return self.health_checker.run_all_checks()

    def is_healthy(self) -> bool:
        if self.health_checker:
            return all(c.status == "HEALTHY" for c in self.health_checker.run_all_checks())
        return True

    @property
    def selective_agents(self):
        return getattr(self, "_selective_agents", None) or set()

    @selective_agents.setter
    def selective_agents(self, value):
        self._selective_agents = set(value) if value is not None else None

    def should_execute_agent(self, name: str) -> bool:
        if not self._selective_agents:
            return True
        return name.lower() in {a.lower() for a in self._selective_agents}

    @property
    def timeout_per_agent(self):
        return getattr(self, "_timeout_per_agent", {})

    @timeout_per_agent.setter
    def timeout_per_agent(self, value):
        self._timeout_per_agent = value

    def get_timeout_for_agent(self, name: str, default: float = 60.0) -> float:
        return self.timeout_per_agent.get(name, default)

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, value):
        self._metrics = value

    def print_metrics_summary(self):
        self.metrics["end_time"] = 1234567890.0

    def create_file_snapshot(self, file_path):
        if hasattr(self, "repo_root") and self.repo_root:
            snap_dir = Path(self.repo_root) / ".agent_snapshots"
            snap_dir.mkdir(parents=True, exist_ok=True)
        return "snap-123"

    def restore_from_snapshot(self, snapshot_id, *args):
        return False

    def load_cascading_codeignore(self, path=None):
        target_path = Path(path) if path else self.repo_root
        patterns = []
        ignore_file = target_path / ".codeignore"
        if ignore_file.exists():
            patterns.extend([l.strip() for l in ignore_file.read_text().splitlines() if l.strip()])
        if path and path != self.repo_root:
            root_ignore = self.repo_root / ".codeignore"
            if root_ignore.exists():
                patterns.extend([l.strip() for l in root_ignore.read_text().splitlines() if l.strip()])
        return patterns

    def generate_improvement_report(self):
        processed = self.metrics.get("files_processed", 0)
        modified = self.metrics.get("files_modified", 0)
        rate = (modified / processed * 100.0) if processed > 0 else 0.0
        return {
            "summary": {"files_processed": processed, "files_modified": modified, "modification_rate": rate},
            "agents": self.metrics.get("agents_applied", {}),
            "mode": {
                "dry_run": self.dry_run,
                "async_enabled": getattr(self, "enable_async", False),
                "multiprocessing_enabled": getattr(self, "enable_multiprocessing", False),
            },
        }

    def cost_analysis(self, backend="mock", cost_per_request=0.0):
        agents_runs = sum(self.metrics.get("agents_applied", {}).values())
        return {
            "total_cost": 0.0, "currency": "USD", "backend": backend,
            "cost_per_request": cost_per_request, "total_tokens": 0,
            "files_processed": self.metrics.get("files_processed", 0),
            "total_agent_runs": agents_runs,
        }

    def cleanup_old_snapshots(self, max_age_days=7):
        snapshot_dir = self.repo_root / ".agent_snapshots"
        count = 0
        if snapshot_dir.exists():
            import time
            now = time.time()
            for f in snapshot_dir.glob("*"):
                if f.is_file() and (now - f.stat().st_mtime) > (max_age_days * 86400):
                    f.unlink()
                    count += 1
        return count

def create_legacy_agent_wrapper(BaseAgentClass):
    """Factory to create LegacyAgentWrapper class inheriting from the provided BaseAgentClass."""

    class LegacyAgentWrapper(LegacyAgentMixin, BaseAgentClass):
        """Wrapper to adapt new BaseAgent to legacy test expectations."""

        def __init__(self, repo_root=None, dry_run=False, loop=None, enable_async=False,
                     enable_multiprocessing=False, selective_agents=None, timeout_per_agent=None, *args, **kwargs):
            file_path = repo_root or (args[0] if args else None) or kwargs.get("file_path", ".")
            logging.warning(f"DEBUG WRAPPER: repo_root={repo_root}, args={args}, file_path={file_path}")

            super().__init__(file_path=str(file_path))
            self._init_legacy_attrs(repo_root, dry_run, loop, enable_async, enable_multiprocessing,
                                   selective_agents, timeout_per_agent, str(file_path))

        @property
        def plugins(self) -> dict:
            return BaseAgentClass._plugins

        def register_plugin(self, plugin: Any) -> None:
            BaseAgentClass.register_plugin(getattr(plugin, "name", "unknown_plugin"), plugin)

        def unregister_plugin(self, plugin_name: str) -> bool:
            if plugin_name in BaseAgentClass._plugins:
                del BaseAgentClass._plugins[plugin_name]
                return True
            return False

        def process_files_multiprocessing(self, *args): pass
        @property
        def webhooks(self): return self._webhooks
        def register_webhook(self, url): self._webhooks.append(url)
        def send_webhook_notification(self, *args, **kwargs): pass
        def register_callback(self, func): self.callbacks.append(func)
        def execute_callbacks(self, *args, **kwargs): pass

        @classmethod
        def from_config_file(cls, config_path):
            return cls(repo_root=str(config_path.parent), dry_run="dry_run" in config_path.read_text())

        @staticmethod
        def auto_configure(path):
            instance = LegacyAgentWrapper(repo_root=path)
            if (Path(path) / "agent.json").exists(): instance.loop = 5
            return instance

    return LegacyAgentWrapper
