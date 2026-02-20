#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Execution handler for agent commands.
"""

import contextlib
import logging
import os
import subprocess
import sys
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from src.core.base.common.shell_core import ShellCore
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class AgentCommandHandler:
    """Minimal AgentCommandHandler used by tests.

    Provides a lightweight interface for running commands and preparing an
    environment. The real implementation is more featureful; tests only import
    and perform basic calls.
    """

    def __init__(
        self,
        repo_root: Path,
        models_config: dict[str, Any] | None = None,
        recorder: Any = None,
    ) -> None:
        self.repo_root = repo_root
        self.models = models_config or {}
        self.recorder = recorder
        self.shell = ShellCore(repo_root=repo_root)

    def _record(self, action: str, result: str, meta: dict[str, Any] | None = None) -> None:
        if self.recorder and hasattr(self.recorder, "record_interaction"):
            try:
                self.recorder.record_interaction(provider="Shell", model="subprocess", prompt=action, result=result, meta=meta)
            except Exception:
                pass

    def run_command(self, cmd: list[str], timeout: int = 120, max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        local_cmd, env = self._prepare_command_environment(list(cmd))

        # Simple single-run execution for tests
        res = self.shell.execute(local_cmd, timeout=timeout, env=env)
        try:
            self._record(" ".join(cmd), f"RC={res.returncode}\n{getattr(res, 'stdout', '')[:1000]}")
        except Exception:
            pass
        return subprocess.CompletedProcess(args=res.command if hasattr(res, 'command') else cmd, returncode=getattr(res, 'returncode', 0), stdout=getattr(res, 'stdout', ''), stderr=getattr(res, 'stderr', ''))

    def _prepare_command_environment(self, cmd: list[str]) -> tuple[list[str], dict[str, str]]:
        local_cmd = list(cmd)
        env = os.environ.copy()
        return local_cmd, env

    def _get_agent_env_vars(self, agent_name: str) -> dict[str, str]:
        return {}

    @contextlib.contextmanager
    def with_agent_env(self, agent_name: str) -> Iterator[None]:
        prev: dict[str, str | None] = {}
        keys = ["DV_AGENT_MODEL_PROVIDER", "DV_AGENT_MODEL_NAME", "DV_AGENT_MODEL_TEMPERATURE", "DV_AGENT_MODEL_MAX_TOKENS"]
        try:
            for k in keys:
                prev[k] = os.environ.get(k)
            yield
        finally:
            for k, v in prev.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
