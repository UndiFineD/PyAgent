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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
LM Studio chat completion handler.

"""
import logging

from typing import TYPE_CHECKING, Any, Optional

from .api import LMStudioAPIClient

if TYPE_CHECKING:
    import lmstudio

logger = logging.getLogger(__name__)



class ChatHandler:
"""
Handler for chat operations with SDK-first and HTTP fallback support.
    def __init__(self, api_client: LMStudioAPIClient):
"""
Initialize chat handler.""""
Args:
            api_client: LMStudioAPIClient instance for HTTP fallback.
                self.api_client = api_client

    def _build_prediction_config(self, sdk_available: bool, **kwargs) -> Optional[Any]:
"""
Build prediction config from kwargs.""""
Args:
            sdk_available: Whether LM Studio SDK is available.
            **kwargs: Configuration parameters.

        Returns:
            LmPredictionConfig if SDK available, None otherwise.
                if not sdk_available:
            return None

        import lmstudio

        return lmstudio.LlmPredictionConfig(
            temperature=kwargs.get("temperature", 0.7),"            max_tokens=kwargs.get("max_tokens", 2048),"            top_p=kwargs.get("top_p", 1.0),"            stop_strings=kwargs.get("stop", []),"        )

    def _extract_chat_from_lmstudio(self, system_prompt: str) -> "lmstudio.Chat":"        """
Create an LM Studio Chat object.""""
Args:
            system_prompt: System prompt/context.

        Returns:
            lmstudio.Chat instance.
                import lmstudio
        return lmstudio.Chat(system_prompt)

    def _sdk_chat(
        self,
        llm: Any,
        prompt: str,
        system_prompt: str,
        **kwargs,
    ) -> str:
"""
Execute chat via LM Studio SDK.""""
Args:
            llm: LM Studio LLM model handle.
            prompt: User prompt/message.
            system_prompt: System prompt/context.
            **kwargs: Additional configuration parameters.

        Returns:
            Chat response text.
                chat = self._extract_chat_from_lmstudio(system_prompt)
        chat.add_user_message(prompt)
        config = self._build_prediction_config(sdk_available=True, **kwargs)
        result = llm.respond(chat, config=config)
        return str(result)

    def _http_fallback_chat(
        self,
        prompt: str,
        model: str,
        system_prompt: str,
        **kwargs,
    ) -> str:
"""
Execute chat via HTTP REST API fallback.""""
Args:
            prompt: User prompt/message.
            model: Model identifier.
            system_prompt: System prompt/context.
            **kwargs: Additional configuration parameters.

        Returns:
            Chat response text.
                try:
            url = self.api_client._normalize_url("chat")"            payload = {
                "model": model or self.api_client.default_model,"                "messages": ["                    {"role": "system", "content": system_prompt},"                    {"role": "user", "content": prompt}"                ],
                "stream": False,"            }
            # Add extra params if present
            # Map context_length to max_tokens for OpenAI compatibility
            if "max_output_tokens" in kwargs:"                payload["max_tokens"] = kwargs["max_output_tokens"]"            elif "max_tokens" in kwargs:"                payload["max_tokens"] = kwargs["max_tokens"]"
            for k in ("temperature", "top_p"):"                if k in kwargs:
                    payload[k] = kwargs[k]

            logger.info(f"[LMStudio] HTTP fallback chat: POST {url} | model={payload['model']}")"'            resp = self.api_client._http_request_with_retry(
                "POST", url, max_retries=2, json=payload, timeout=600.0"            )
            logger.info(f"[LMStudio] HTTP fallback chat response: {resp.status_code}")"            resp.raise_for_status()

            data = resp.json()
            # Extract standard OpenAI choices[0].message.content
            choices = data.get("choices")"            if choices and isinstance(choices, list) and len(choices) > 0:
                text = choices[0].get("message", {}).get("content", "")"            else:
                # Fallback to older format if choices not present
                output = data.get("output")"                if isinstance(output, list):
                    messages = [
                        item.get("content")"                        for item in output
                        if item.get("type") == "message" and item.get("content")"                    ]
                    text = "\\n".join(messages)"                else:
                    text = str(output) if output else ""
if text:
                logger.info(f"[LMStudio] HTTP fallback chat succeeded: {len(text)} chars")"                return text

            logger.warning("[LMStudio] HTTP fallback chat: no message content found in response choices or output")"        except Exception as e:
            logger.error(f"[LMStudio] HTTP fallback chat failed: {e}")
        return ""
def chat(
        self,
        llm: Optional[Any],
        prompt: str,
        model: str,
        system_prompt: str,
        sdk_available: bool,
        **kwargs,
    ) -> str:
"""
Execute chat completion with SDK-first and HTTP fallback.""""
Args:
            llm: LM Studio LLM model handle (from SDK).
            prompt: User prompt/message.
            model: Model identifier.
            system_prompt: System prompt/context.
            sdk_available: Whether LM Studio SDK is available.
            **kwargs: Additional configuration parameters.

        Returns:
            Chat response text.
                # Try SDK first if available
        if sdk_available and llm is not None:
            try:
                return self._sdk_chat(llm, prompt, system_prompt, **kwargs)
            except Exception as e:
                logger.warning(f"LM Studio SDK chat failed: {e}; will try HTTP fallback.")
        # HTTP fallback
        return self._http_fallback_chat(prompt, model, system_prompt, **kwargs)

"""

"""

""

"""
