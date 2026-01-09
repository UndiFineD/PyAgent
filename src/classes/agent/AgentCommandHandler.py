#!/usr/bin/env python3

import os
import sys
import logging
import subprocess
import time
import contextlib
from pathlib import Path
from typing import List, Dict, Any, Optional

class AgentCommandHandler:
    """Handles command execution for the Agent, including sub-agent orchestration."""
    
    def __init__(self, repo_root: Path, models_config: Optional[Dict[str, Any]] = None) -> None:
        self.repo_root = repo_root
        self.models = models_config or {}

    def run_command(self, cmd: List[str], timeout: int = 120, max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging."""
        def attempt_command() -> subprocess.CompletedProcess[str]:
            logging.debug(f"Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)")
            try:
                local_cmd = list(cmd)
                env = os.environ.copy()

                # Detect python-invoked agent scripts
                try:
                    is_agent_script = (
                        len(local_cmd) > 1 and
                        local_cmd[0] == sys.executable and
                        Path(local_cmd[1]).name.startswith('agent_')
                    )
                except Exception:
                    is_agent_script = False

                if is_agent_script:
                    env['DV_AGENT_PARENT'] = '1'
                    if '--no-cascade' not in local_cmd:
                        local_cmd = local_cmd[:2] + ['--no-cascade'] + local_cmd[2:]
                    
                    try:
                        script_name = Path(local_cmd[1]).name
                        agent_name = script_name[len('agent_'):-3] if script_name.endswith('.py') else None
                    except Exception:
                        agent_name = None

                    model_spec = None
                    if agent_name:
                        model_spec = self.models.get(agent_name) or self.models.get('default')

                    if model_spec and isinstance(model_spec, dict):
                        if 'provider' in model_spec:
                            env['DV_AGENT_MODEL_PROVIDER'] = str(model_spec.get('provider', ''))
                        if 'model' in model_spec:
                            env['DV_AGENT_MODEL_NAME'] = str(model_spec.get('model', ''))
                        if 'temperature' in model_spec:
                            env['DV_AGENT_MODEL_TEMPERATURE'] = str(model_spec.get('temperature', ''))
                        if 'max_tokens' in model_spec:
                            env['DV_AGENT_MODEL_MAX_TOKENS'] = str(model_spec.get('max_tokens', ''))

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
                return result
            except subprocess.TimeoutExpired:
                logging.error(f"Command timed out after {timeout}s: {' '.join(cmd[:3])}...")
                return subprocess.CompletedProcess(
                    cmd, returncode=-1, stdout="", stderr="Timeout expired")
            except OSError as e:
                logging.error(f"Command failed to start: {e}")
                return subprocess.CompletedProcess(
                    cmd, returncode=-2, stdout="", stderr=str(e))

        # Retry logic with exponential backoff
        for i in range(max_retries):
            res = attempt_command()
            if res.returncode == 0 or i == max_retries - 1:
                return res
            
            wait_time = 2 ** i
            logging.warning(f"Command failed (rc={res.returncode}). Retrying in {wait_time}s... (Attempt {i+1}/{max_retries})")
            time.sleep(wait_time)
            
        return res

    @contextlib.contextmanager
    def with_agent_env(self, agent_name: str):
        """Temporarily set environment variables for a specific agent."""
        prev: Dict[str, Optional[str]] = {}
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
