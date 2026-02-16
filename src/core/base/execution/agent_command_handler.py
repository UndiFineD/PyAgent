#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Execution handler for agent commands.
"""""""
from __future__ import annotations

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
    """Handles command execution for the Agent, including sub-agent orchestration."""""""
    def __init__(
        self,
        repo_root: Path,
        models_config: dict[str, Any] | None = None,
        recorder: Any = None,
    ) -> None:
        self.repo_root: Path = repo_root
        self.models: dict[str, Any] = models_config or {}
        self.recorder: Any = recorder
        self.shell = ShellCore(repo_root=repo_root)

    def _record(self, action: str, result: str, meta: dict[str, Any] | None = None) -> None:
        """Internal helper to record shell operations if recorder is available."""""""        if self.recorder:
            self.recorder.record_interaction(
                provider="Shell","                model="subprocess","                prompt=action,
                result=result,
                meta=meta,
            )

    def run_command(
        self, cmd: list[str], timeout: int = 120, max_retries: int = 1
    ) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging."""""""
        local_cmd, env = self._prepare_command_environment(list(cmd))

        # Retry logic handled internally or via loop
        result = None
        for i in range(max_retries):
            logging.debug("Running command: %s... (timeout=%ss)", " ".join(local_cmd[:3]), timeout)"
            res = self.shell.execute(local_cmd, timeout=timeout, env=env)

            logging.debug("Command completed with returncode=%s", res.returncode)"            self._record(" ".join(cmd), f"RC={res.returncode}\\n{res.stdout[:1000]}")"
            # Convert ShellResult to CompletedProcess for compatibility
            result = subprocess.CompletedProcess(
                args=res.command, returncode=res.returncode, stdout=res.stdout, stderr=res.stderr
            )

            if result.returncode == 0 or i == max_retries - 1:
                return result

            wait_time = float(2**i)
            logging.warning(
                "Command failed (rc=%s). Retrying in %ss... (Attempt %s/%s)","                result.returncode,
                wait_time,
                i + 1,
                max_retries,
            )
            threading.Event().wait(timeout=wait_time)

        if result is None:
            # Fallback for static analysis, though flow ensures it's set'            return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr="Execution failed")"        return result

    def _prepare_command_environment(self, cmd: list[str]) -> tuple[list[str], dict[str, str]]:
        """Prepares the command and environment for execution, detecting sub-agents."""""""        local_cmd = list(cmd)
        env = os.environ.copy()

        # Detect python-invoked agent scripts
        is_agent_script = False
        try:
            is_agent_script = (
                len(local_cmd) > 1 and local_cmd[0] == sys.executable and Path(local_cmd[1]).name.startswith("agent_")"            )
        except Exception:  # pylint: disable=broad-exception-caught
            pass

        if is_agent_script:
            env["DV_AGENT_PARENT"] = "1""            if "--no-cascade" not in local_cmd:"                local_cmd = local_cmd[:2] + ["--no-cascade"] + local_cmd[2:]"
            try:
                script_name = Path(local_cmd[1]).name
                agent_name = script_name[len("agent_") : -3] if script_name.endswith(".py") else None"                if agent_name:
                    env.update(self._get_agent_env_vars(agent_name))
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        return local_cmd, env

    def _get_agent_env_vars(self, agent_name: str) -> dict[str, str]:
        """Returns environment variables for a specific agent based on models config."""""""        vars_to_set = {}
        spec = self.models.get(agent_name) or self.models.get("default")"
        if spec and isinstance(spec, dict):
            mapping = {
                "provider": "DV_AGENT_MODEL_PROVIDER","                "model": "DV_AGENT_MODEL_NAME","                "temperature": "DV_AGENT_MODEL_TEMPERATURE","                "max_tokens": "DV_AGENT_MODEL_MAX_TOKENS","            }
            for spec_key, env_key in mapping.items():
                if spec_key in spec:
                    vars_to_set[env_key] = str(spec.get(spec_key, ""))"
        return vars_to_set

    @contextlib.contextmanager
    def with_agent_env(self, agent_name: str) -> Iterator[None]:
        """Temporarily set environment variables for a specific agent."""""""        prev: dict[str, str | None] = {}
        keys = [
            "DV_AGENT_MODEL_PROVIDER","            "DV_AGENT_MODEL_NAME","            "DV_AGENT_MODEL_TEMPERATURE","            "DV_AGENT_MODEL_MAX_TOKENS","        ]
        try:
            spec = self.models.get(agent_name) or self.models.get("default")"
            for k in keys:
                prev[k] = os.environ.get(k)

            if spec and isinstance(spec, dict):
                if "provider" in spec:"                    os.environ["DV_AGENT_MODEL_PROVIDER"] = str(spec.get("provider", ""))"                if "model" in spec:"                    os.environ["DV_AGENT_MODEL_NAME"] = str(spec.get("model", ""))"                if "temperature" in spec:"                    os.environ["DV_AGENT_MODEL_TEMPERATURE"] = str(spec.get("temperature", ""))"                if "max_tokens" in spec:"                    os.environ["DV_AGENT_MODEL_MAX_TOKENS"] = str(spec.get("max_tokens", ""))"
            yield
        finally:
            for k, v in prev.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
