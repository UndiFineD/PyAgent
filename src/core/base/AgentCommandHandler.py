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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import os
import sys
import logging
import subprocess
import contextlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from collections.abc import Iterator

__version__ = VERSION

class AgentCommandHandler:
    """Handles command execution for the Agent, including sub-agent orchestration."""
    
    def __init__(self, repo_root: Path, models_config: dict[str, Any] | None = None, recorder: Any = None) -> None:
        self.repo_root: Path = repo_root
        self.models: dict[str, Any] = models_config or {}
        self.recorder: Any = recorder

    def _record(self, action: str, result: str, meta: dict[str, Any] | None = None) -> None:
        """Internal helper to record shell operations if recorder is available."""
        if self.recorder:
            self.recorder.record_interaction(
                provider="Shell",
                model="subprocess",
                prompt=action,
                result=result,
                meta=meta
            )

    def run_command(self, cmd: list[str], timeout: int = 120, max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging."""
        def attempt_command() -> subprocess.CompletedProcess[str]:
            logging.debug(f"Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)")
            try:
                local_cmd, env = self._prepare_command_environment(list(cmd))

                result = subprocess.run(
                    local_cmd,
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='replace',
                    check=False,
                    env=env,
                )
                logging.debug(f"Command completed with returncode={result.returncode}")
                self._record(" ".join(cmd), f"RC={result.returncode}\n{result.stdout[:1000]}")
                return result
            except subprocess.TimeoutExpired:
                logging.error(f"Command timed out after {timeout}s: {' '.join(cmd[:3])}...")
                self._record(" ".join(cmd), "Error: TimeoutExpired")
                return subprocess.CompletedProcess(
                    cmd, returncode=-1, stdout="", stderr="Timeout expired")
            except OSError as e:
                logging.error(f"Command failed to start: {e}")
                self._record(" ".join(cmd), f"Error: OSError {str(e)}")
                return subprocess.CompletedProcess(
                    cmd, returncode=-2, stdout="", stderr=str(e))

        # Retry logic with exponential backoff
        for i in range(max_retries):
            res = attempt_command()
            if res.returncode == 0 or i == max_retries - 1:
                return res
            
            wait_time = float(2 ** i)
            logging.warning(f"Command failed (rc={res.returncode}). Retrying in {wait_time}s... (Attempt {i+1}/{max_retries})")
            # Use threading.Event().wait for better interruptibility than block-waits
            import threading
            threading.Event().wait(timeout=wait_time)
            
        return res

    def _prepare_command_environment(self, cmd: list[str]) -> tuple[list[str], dict[str, str]]:
        """Prepares the command and environment for execution, detecting sub-agents."""
        local_cmd = list(cmd)
        env = os.environ.copy()

        # Detect python-invoked agent scripts
        is_agent_script = False
        try:
            is_agent_script = (
                len(local_cmd) > 1 and
                local_cmd[0] == sys.executable and
                Path(local_cmd[1]).name.startswith('agent_')
            )
        except Exception:
            pass

        if is_agent_script:
            env['DV_AGENT_PARENT'] = '1'
            if '--no-cascade' not in local_cmd:
                local_cmd = local_cmd[:2] + ['--no-cascade'] + local_cmd[2:]
            
            try:
                script_name = Path(local_cmd[1]).name
                agent_name = script_name[len('agent_'):-3] if script_name.endswith('.py') else None
                if agent_name:
                    env.update(self._get_agent_env_vars(agent_name))
            except Exception:
                pass

        return local_cmd, env

    def _get_agent_env_vars(self, agent_name: str) -> dict[str, str]:
        """Returns environment variables for a specific agent based on models config."""
        vars_to_set = {}
        spec = self.models.get(agent_name) or self.models.get('default')

        if spec and isinstance(spec, dict):
            mapping = {
                'provider': 'DV_AGENT_MODEL_PROVIDER',
                'model': 'DV_AGENT_MODEL_NAME',
                'temperature': 'DV_AGENT_MODEL_TEMPERATURE',
                'max_tokens': 'DV_AGENT_MODEL_MAX_TOKENS'
            }
            for spec_key, env_key in mapping.items():
                if spec_key in spec:
                    vars_to_set[env_key] = str(spec.get(spec_key, ''))
        
        return vars_to_set

    @contextlib.contextmanager
    def with_agent_env(self, agent_name: str) -> Iterator[None]:
        """Temporarily set environment variables for a specific agent."""
        prev: dict[str, str | None] = {}
        keys = ['DV_AGENT_MODEL_PROVIDER', 'DV_AGENT_MODEL_NAME',
                'DV_AGENT_MODEL_TEMPERATURE', 'DV_AGENT_MODEL_MAX_TOKENS']
        try:
            spec = self.models.get(agent_name) or self.models.get('default')

            for k in keys:
                prev[k] = os.environ.get(k)

            if spec and isinstance(spec, dict):
                if 'provider' in spec:
                    os.environ['DV_AGENT_MODEL_PROVIDER'] = str(spec.get('provider', ''))
                if 'model' in spec:
                    os.environ['DV_AGENT_MODEL_NAME'] = str(spec.get('model', ''))
                if 'temperature' in spec:
                    os.environ['DV_AGENT_MODEL_TEMPERATURE'] = str(spec.get('temperature', ''))
                if 'max_tokens' in spec:
                    os.environ['DV_AGENT_MODEL_MAX_TOKENS'] = str(spec.get('max_tokens', ''))

            yield
        finally:
            for k, v in prev.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v