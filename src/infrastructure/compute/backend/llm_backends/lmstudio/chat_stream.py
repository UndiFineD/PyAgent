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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
LM Studio streaming chat completion handler.
"""

import json
import logging
from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional

from .api import LMStudioAPIClient

if TYPE_CHECKING:
    import lmstudio

logger = logging.getLogger(__name__)


class StreamingChatHandler:
    """Handler for streaming chat operations with SDK-first and HTTP fallback support."""

    def __init__(self, api_client: LMStudioAPIClient):
        """Initialize streaming chat handler.
        
        Args:
            api_client: LMStudioAPIClient instance for HTTP fallback.
        """
        self.api_client = api_client

    def _build_prediction_config(self, sdk_available: bool, **kwargs) -> Optional[Any]:
        """Build prediction config from kwargs.
        
        Args:
            sdk_available: Whether LM Studio SDK is available.
            **kwargs: Configuration parameters.
        
        Returns:
            LmPredictionConfig if SDK available, None otherwise.
        """
        if not sdk_available:
            return None
        
        import lmstudio
        
        return lmstudio.LlmPredictionConfig(
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
            top_p=kwargs.get("top_p", 1.0),
            stop_strings=kwargs.get("stop", []),
        )

    def _extract_chat_from_lmstudio(self, system_prompt: str) -> "lmstudio.Chat":
        """Create an LM Studio Chat object.
        
        Args:
            system_prompt: System prompt/context.
        
        Returns:
            lmstudio.Chat instance.
        """
        import lmstudio
        return lmstudio.Chat(system_prompt)

    def _sdk_chat_stream(
        self,
        llm: Any,
        prompt: str,
        system_prompt: str,
        on_fragment: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> Iterator[str]:
        """Stream chat via LM Studio SDK.
        
        Args:
            llm: LM Studio LLM model handle.
            prompt: User prompt/message.
            system_prompt: System prompt/context.
            on_fragment: Optional callback for each fragment.
            **kwargs: Additional configuration parameters.
        
        Yields:
            Chat response text fragments.
        """
        import lmstudio
        
        chat = self._extract_chat_from_lmstudio(system_prompt)
        chat.add_user_message(prompt)
        config = self._build_prediction_config(sdk_available=True, **kwargs)
        
        for fragment in llm.respond_stream(chat, config=config):
            text = str(fragment)
            if on_fragment:
                on_fragment(text)
            yield text

    def _http_fallback_chat_stream(
        self,
        prompt: str,
        model: str,
        system_prompt: str,
        on_fragment: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> Iterator[str]:
        """Stream chat via HTTP REST API fallback with SSE.
        
        Args:
            prompt: User prompt/message.
            model: Model identifier.
            system_prompt: System prompt/context.
            on_fragment: Optional callback for each fragment.
            **kwargs: Additional configuration parameters.
        
        Yields:
            Chat response text fragments.
        """
        import httpx
        
        try:
            import sseclient
        except ImportError:
            logger.error("[LMStudio] sseclient not available for streaming fallback")
            return
        
        try:
            url = self.api_client._normalize_url("chat")
            payload = {
                "model": model or self.api_client.default_model,
                "input": prompt,
                "system_prompt": system_prompt,
                "stream": True,
            }
            for k in ("temperature", "top_p", "max_output_tokens", "context_length"):
                if k in kwargs:
                    payload[k] = kwargs[k]
            
            logger.info(f"[LMStudio] HTTP fallback chat_stream: POST {url} | model={payload['model']}")
            headers = self.api_client._get_headers()
            
            with httpx.stream("POST", url, json=payload, headers=headers, timeout=60) as resp:
                resp.raise_for_status()
                logger.info(f"[LMStudio] HTTP fallback chat_stream response: {resp.status_code}")
                
                # Use SSE client to parse events
                client = sseclient.SSEClient(resp.iter_text())
                for event in client.events():
                    if event.event == "message.delta":
                        data = event.data
                        try:
                            content = json.loads(data).get("content", "")
                        except Exception:
                            content = data
                        if content:
                            if on_fragment:
                                on_fragment(content)
                            yield content
                    elif event.event == "chat.end":
                        # Final event
                        logger.debug("[LMStudio] HTTP fallback chat_stream received chat.end event")
                        break
                
                logger.info("[LMStudio] HTTP fallback chat_stream completed successfully")
                
        except Exception as e:
            logger.error(f"[LMStudio] HTTP fallback streaming error: {e}")

    def chat_stream(
        self,
        llm: Optional[Any],
        prompt: str,
        model: str,
        system_prompt: str,
        sdk_available: bool,
        on_fragment: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> Iterator[str]:
        """Stream chat completion with SDK-first and HTTP fallback.
        
        Args:
            llm: LM Studio LLM model handle (from SDK).
            prompt: User prompt/message.
            model: Model identifier.
            system_prompt: System prompt/context.
            sdk_available: Whether LM Studio SDK is available.
            on_fragment: Optional callback for each fragment.
            **kwargs: Additional configuration parameters.
        
        Yields:
            Chat response text fragments.
        """
        # Try SDK first if available
        if sdk_available and llm is not None:
            try:
                yield from self._sdk_chat_stream(llm, prompt, system_prompt, on_fragment, **kwargs)
                return
            except Exception as e:
                logger.warning(f"LM Studio SDK chat_stream failed: {e}; will try HTTP fallback.")
        
        # HTTP fallback
        yield from self._http_fallback_chat_stream(prompt, model, system_prompt, on_fragment, **kwargs)
