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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""
Shell execution core for agents.
Handles subprocess spawning, environment propagation, and interaction recording.
"""



import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Any, Optional

class ShellExecutor:
    """Safely executes shell commands and records outcomes."""

    @staticmethod
    def run_command(cmd: List[str], workspace_root: str, agent_name: str, 
                    models_config: Optional[Any] = None, recorder: Optional[Any] = None,
                    timeout: int = 120, max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        """Run a command with full environment and telemetry support."""
        logging.debug(f"Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)")
        
        last_error = None
        for attempt in range(max_retries):
            try:
                env = os.environ.copy()
                
                # Model and Parent propagation
                if os.environ.get("DV_AGENT_PARENT"):
                    env['DV_AGENT_PARENT'] = os.environ.get("DV_AGENT_PARENT")

                if models_config:
                    import json
                    env['AGENT_MODELS_CONFIG'] = json.dumps(models_config)

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env,
                    check=False
                )
                
                if recorder:
                    recorder.record_interaction(
                        provider="Shell",
                        model="subprocess",
                        prompt=" ".join(cmd),
                        result=result.stdout + result.stderr,
                        meta={"exit_code": result.returncode, "attempt": attempt + 1}
                    )
                
                return result
            except subprocess.TimeoutExpired as e:
                logging.warning(f"Timeout (attempt {attempt + 1}/{max_retries})")
                last_error = e
            except Exception as e:
                logging.error(f"Execution failure: {e}")
                last_error = e
                
        if isinstance(last_error, subprocess.TimeoutExpired):
             raise last_error
        return subprocess.CompletedProcess(" ".join(cmd), 1, stdout="", stderr=str(last_error))
