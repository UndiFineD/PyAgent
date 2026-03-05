#!/usr/bin/env python3
from __future__ import annotations
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

"""
GitHub Models Backend for LLMClient.
"""

import logging
from typing import Any

from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.infrastructure.compute.backend.local_context_recorder import LocalContextRecorder


class GitHubModelsBackend:
    """
    Handles communication with GitHub Models OpenAI-compatible chat endpoints.
    """

    def __init__(
        self, 
        session: Any, 
        connectivity: ConnectivityManager, 
        recorder: LocalContextRecorder | None
    ) -> None:
        """
        Initializes the GitHubModelsBackend.
        """
        self.session = session
        self.connectivity = connectivity
        self.recorder = recorder
        logging.debug("GitHubModelsBackend initialized.")

    def chat(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        cascade_context: CascadeContext | None = None,
        **kwargs,
    ) -> str:
        """
        Sends a chat request to the GitHub Models backend and records the interaction.
        """
        agent_info = f"[{cascade_context.agent_name} | {cascade_context.task_id}] " if cascade_context else ""
        logging.info(f"{agent_info}GitHubModelsBackend: Sending request to model '{model}' with prompt: {prompt[:100]}...")

        # --- Hypothetical API Call (replace with actual implementation) ---
        # response = self.session.post(
        #     "https://api.github.com/models/chat/completions",
        #     json={
        #         "model": model,
        #         "messages": [
        #             {"role": "system", "content": system_prompt},
        #             {"role": "user", "content": prompt},
        #         ],
        #         **kwargs,
        #     },
        # ).json()
        # generated_text = response["choices"][0]["message"]["content"]
        # -----------------------------------------------------------------

        # Simulate a response for demonstration
        generated_text = f"Simulated GitHub Models response for: {prompt[:50]}..."

        logging.info(f"{agent_info}GitHubModelsBackend: Received response: {generated_text[:100]}...")

        if self.recorder:
            self.recorder.record_interaction(
                provider="github_models",
                model=model,
                prompt=prompt,
                result=generated_text,
                meta={
                    "system_prompt": system_prompt,
                    "cascade_context": {
                        "task_id": cascade_context.task_id,
                        "agent_name": cascade_context.agent_name,
                        "agent_path": cascade_context.agent_path,
                        "parent_task_id": cascade_context.parent_task_id,
                    } if cascade_context else {},
                    **kwargs,
                },
            )
        return generated_text
