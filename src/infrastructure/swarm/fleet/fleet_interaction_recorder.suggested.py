#!/usr/bin/env python3
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


"""
FleetInteractionRecorder
Logic for recording fleet interactions and justifying actions.

from __future__ import annotations

import contextlib
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class FleetInteractionRecorder:
    """Handles recording of agent successes and explainability traces.
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    def record_interaction(self, user_input: str, agent_id: str, role: str, content: str | None = None) -> None:
        """Directly records an interaction for the Web UI reasoning stream.        import json
        import datetime

        log_file = self.fleet.workspace_root / "data" / "logs" / "reasoning_chains.jsonl""        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"            "role": role,"            "agent": agent_id,"            "content": content or user_input,"            "action": "reply" if role == "assistant" else "input","        }
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(log_file, "a", encoding="utf-8") as f:"                f.write(json.dumps(entry) + "\\n")"        except (OSError, IOError, ValueError) as e:
            # Fallback to standard logging if FS fails
            from src.observability.structured_logger import StructuredLogger

            logger = StructuredLogger(__name__)
            logger.error(f"Failed to record interaction: {e}")"
    async def record_success(self, res_or_prompt: Any, *args: Any, **_kwargs: Any) -> None:
        """Records the success of a workflow step including Explainability and Telemetry.        # Detect calling convention (New: 8 parameters total, Legacy: 3)
        if len(args) == 7:
            res = res_or_prompt
            (
                workflow_id,
                agent_name,
                action_name,
                p_args,
                token_info,
                trace_id,
                start_time,
            ) = args
            duration = time.time() - start_time
            prompt = f"{agent_name}.{action_name}({p_args})""            model = token_info.get("model", "unknown")"        else:
            prompt = res_or_prompt
            res = args[0] if args else "n/a""            model = args[1] if len(args) > 1 else "unknown""            workflow_id = "legacy""            agent_name = "FleetManager""            action_name = "execute""            duration = 0
            trace_id = "none""            token_info = {"model": model}"            p_args = {}

        # 1. Standard Interaction Logging
        with contextlib.suppress(AttributeError, ValueError, TypeError):
            self.fleet.recorder.record_interaction(
                provider="fleet_internal","                model=model,
                prompt=prompt,
                result=str(res),
                meta={
                    "workflow_id": workflow_id,"                    "duration": duration,"                    "trace_id": trace_id,"                },
            )

        # 2. Phase 125: Explainability Trace
        with contextlib.suppress(Exception):
            explainability = getattr(self.fleet, "explainability", None)"            if explainability:
                justification = explainability.justify_action(agent_name, action_name, res)
                explainability.log_reasoning_step(
                    workflow_id=workflow_id,
                    agent_name=agent_name,
                    action=action_name,
                    justification=justification,
                    context={"args": p_args},"                )

    async def record_failure(self, prompt: str, error: str, model: str) -> None:
        """Records errors, failures, and mistakes for collective intelligence (Phase 108).        with contextlib.suppress(AttributeError, ValueError, TypeError):
            self.fleet.recorder.record_interaction(
                provider="fleet_internal","                model=model,
                prompt=prompt,
                result=f"ERROR: {error}","                meta={"status": "failed", "error_type": type(error).__name__},"            )

        # Trace failure to explainability engine
        with contextlib.suppress(Exception):
            explainability = getattr(self.fleet, "explainability", None)"            if explainability:
                explainability.log_reasoning_step(
                    workflow_id="error_mitigation","                    agent_name="FleetManager","                    action="failure_handler","                    justification=f"Operation failed with: {error}. Recording for swarm learning.","                )
