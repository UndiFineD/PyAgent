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
LM Studio LLM backend implementation with modular architecture.

Separates concerns into:
- api.py: REST API client with HTTP fallback
- chat.py: Non-streaming chat operations
- chat_stream.py: Streaming chat operations
- mcp_client.py: SDK client and session management
"""

import logging
import time
from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional, Sequence

from ..llm_backend import LLMBackend
from .api import LMStudioAPIClient
from .cache import ModelCache
from .chat import ChatHandler
from .chat_stream import StreamingChatHandler
from .mcp_client import MCPClient
from .models import LMStudioConfig

if TYPE_CHECKING:
    import lmstudio

logger = logging.getLogger(__name__)


class LMStudioBackend(LLMBackend):
    """
    LM Studio LLM Backend with modular architecture.
    
    Delegates to:
    - MCPClient: SDK client management
    - LMStudioAPIClient: REST API client
    - ChatHandler: Non-streaming chat
    - StreamingChatHandler: Streaming chat
    """

    PROVIDER_ID = "lmstudio"

    def __init__(
        self,
        session: Any,
        connectivity_manager: Any,
        recorder: Any = None,
        config: LMStudioConfig | None = None,
    ) -> None:
        """Initialize LM Studio backend."""
        super().__init__(session, connectivity_manager, recorder)

        self.config = config or LMStudioConfig()
        self._model_cache = ModelCache(self.config.cache_ttl)
        self._sdk_available: bool | None = None
        
        # Initialize modular components
        self._api_client = LMStudioAPIClient(
            self.config.base_url,
            getattr(self.config, "api_token", None),
            self.config.default_model,
        )
        self._mcp_client = MCPClient(self.config.base_url, getattr(self.config, "api_token", None))
        self._chat_handler = ChatHandler(self._api_client)
        self._streaming_handler = StreamingChatHandler(self._api_client)

    def _check_sdk(self) -> bool:
        """Check if LM Studio SDK is available."""
        if self._sdk_available is not None:
            return self._sdk_available

        try:
            import lmstudio

            self._sdk_available = True
            logger.debug(f"LM Studio SDK version: {lmstudio.__version__}")
            return True
        except ImportError:
            self._sdk_available = False
            logger.warning("LM Studio SDK not available. Install with: pip install lmstudio")
            return False

    def disconnect(self) -> None:
        """Disconnect clients."""
        self._mcp_client.close()
        self._model_cache.clear()

    def list_loaded_models(self) -> list[str]:
        """List currently loaded models in LM Studio.

        Prefer SDK helpers but fall back to HTTP when SDK is unavailable.
        """
        try:
            import lmstudio

            models = lmstudio.list_loaded_models()
            logger.debug(f"Listed {len(models)} models via LM Studio SDK")
            return [m.path for m in models]
        except Exception as e:
            logger.warning(f"Failed to list loaded models via SDK: {e}; will try HTTP fallback")

        # HTTP fallback
        return self._api_client.list_models()

    def list_downloaded_models(self) -> list[str]:
        """List downloaded models available in LM Studio.

        Use the same fallback strategy as `list_loaded_models`.
        """
        try:
            import lmstudio

            models = lmstudio.list_downloaded_models()
            logger.debug(f"Listed {len(models)} downloaded models via LM Studio SDK")
            return [m.path for m in models]
        except Exception as e:
            logger.warning(
                f"Failed to list downloaded models via SDK: {e}; will try HTTP fallback"
            )

        # HTTP fallback
        return self._api_client.list_models()

    def get_model(self, model: str = "") -> Any:
        """Get a loaded model handle, using cache if available.

        Use MCPClient to manage SDK connections and accessor styles.
        """
        # Check cache first
        cache_key = model or "_default_"
        cached = self._model_cache.get(cache_key)
        if cached is not None:
            return cached.model_info

        # Try SDK first
        try:
            if not self._check_sdk():
                raise RuntimeError("LM Studio SDK not available")
            
            client = self._mcp_client.get_sync_client()
            llm = self._mcp_client.get_llm(client, model)
            
            if self.config.cache_models:
                self._model_cache.set(cache_key, llm)
            
            return llm
        except Exception as e:
            logger.warning(f"LMStudio SDK model fetch failed: {e}; will try HTTP fallback")

        # HTTP fallback: if model is present via REST, return a shim LLM object
        try:
            models = self.list_loaded_models()
            logger.debug(f"HTTP fallback returned models sample: {models[:10]}")
            if models and (model in models or any(model in m for m in models)):
                logger.info(f"Using HTTP fallback LLM for model '{model}'")
                
                class _HTTPFallbackLLM:
                    def __init__(self, backend: "LMStudioBackend", model_id: str):
                        self._backend = backend
                        self._model_id = model_id

                    def respond(self, chat, config=None):
                        # Extract prompt from Chat object
                        prompt = self._backend._extract_prompt_from_chat(chat)
                        return self._backend._chat_handler._http_fallback_chat(
                            prompt, self._model_id, "You are a helpful assistant."
                        )

                fallback_llm = _HTTPFallbackLLM(self, model or self.config.default_model)
                if self.config.cache_models:
                    self._model_cache.set(cache_key, fallback_llm)
                
                try:
                    self._update_status(self.PROVIDER_ID, True)
                except Exception:
                    pass
                
                return fallback_llm
        except Exception:
            pass

        raise RuntimeError(f"Failed to get model '{model}'")

    def _extract_prompt_from_chat(self, chat: Any) -> str:
        """Extract prompt string from Chat object.
        
        Args:
            chat: Chat object from SDK or dict-like.
        
        Returns:
            Extracted prompt text.
        """
        try:
            if hasattr(chat, "user_message"):
                return getattr(chat, "user_message")
            elif hasattr(chat, "messages"):
                msgs = getattr(chat, "messages")
                if isinstance(msgs, (list, tuple)) and msgs:
                    first = msgs[0]
                    if isinstance(first, dict):
                        return first.get("content") or first.get("text") or str(first)
                    return str(first)
            return str(chat)
        except Exception:
            return str(chat)

    def chat(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """Execute a chat completion via LM Studio, with robust HTTP fallback."""
        if not self._is_working(self.PROVIDER_ID):
            logger.debug("LM Studio skipped due to connection cache.")
            return ""

        try:
            llm = None
            if self._check_sdk():
                try:
                    llm = self.get_model(model)
                except Exception as e:
                    logger.debug(f"Failed to get SDK model: {e}")
            
            start_time = time.time()
            result = self._chat_handler.chat(
                llm, prompt, model, system_prompt, self._check_sdk(), **kwargs
            )
            
            if result:
                elapsed = time.time() - start_time
                logger.debug(f"Chat completed in {elapsed:.2f}s: {len(result)} chars")
                self._record(
                    self.PROVIDER_ID,
                    model or "default",
                    prompt,
                    result,
                    system_prompt=system_prompt,
                )
                self._update_status(self.PROVIDER_ID, True)
            
            return result
        except Exception as e:
            logger.error(f"Chat operation failed: {e}")
            self._update_status(self.PROVIDER_ID, False)
            return ""

    def chat_stream(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        on_fragment: Callable[[str], None] | None = None,
        **kwargs,
    ) -> Iterator[str]:
        """Stream chat completion tokens, with HTTP fallback using REST API SSE."""
        try:
            llm = None
            if self._check_sdk():
                try:
                    llm = self.get_model(model)
                except Exception as e:
                    logger.debug(f"Failed to get SDK model for streaming: {e}")
            
            for fragment in self._streaming_handler.chat_stream(
                llm, prompt, model, system_prompt, self._check_sdk(), on_fragment, **kwargs
            ):
                full_response.append(fragment)
                yield fragment
            
            if full_response:
                self._record(
                    self.PROVIDER_ID,
                    model or "default",
                    prompt,
                    "".join(full_response),
                    system_prompt=system_prompt,
                )
                self._update_status(self.PROVIDER_ID, True)
        except Exception as e:
            logger.error(f"Streaming chat failed: {e}")
            self._update_status(self.PROVIDER_ID, False)

    async def _fetch_llm_from_async_client(self, client: Any, model: str = "") -> Any:
        """Fetch an llm object from an async SDK client."""
        return await self._mcp_client.get_async_llm(client, model)

    async def chat_async(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """Async chat completion via LM Studio."""
        if not self._check_sdk():
            return ""

        import lmstudio

        try:
            # Create a fresh AsyncClient for this request
            api_url = self.config.base_url
            if not api_url.startswith("http://") and not api_url.startswith("https://"):
                api_url = "http://" + api_url
            
            async with lmstudio.AsyncClient(api_url) as client:
                llm = await self._fetch_llm_from_async_client(client, model)
                chat = lmstudio.Chat(system_prompt)
                chat.add_user_message(prompt)
                
                config = self._chat_handler._build_prediction_config(True, **kwargs)
                result = await llm.respond(chat, config=config)
                response_text = str(result)

                self._record(
                    self.PROVIDER_ID,
                    model or "default",
                    prompt,
                    response_text,
                    system_prompt=system_prompt,
                )
                self._update_status(self.PROVIDER_ID, True)

                return response_text
        except Exception as e:
            logger.error(f"LM Studio async error: {e}")
            self._update_status(self.PROVIDER_ID, False)
            return ""

    def embed(
        self,
        texts: str | Sequence[str],
        model: str = "",
    ) -> list[list[float]]:
        """Generate embeddings for text(s)."""
        if not self._check_sdk():
            return []

        try:
            client = self._mcp_client.get_sync_client()
            emb_model = self._mcp_client.get_embedding_model(client, model)

            if isinstance(texts, str):
                texts = [texts]

            embeddings = []
            for text in texts:
                vec = emb_model.embed(text)
                embeddings.append(list(vec))

            return embeddings
        except Exception as e:
            logger.error(f"LM Studio embedding error: {e}")
            return []

    def chat_with_tools(
        self,
        prompt: str,
        tools: list[dict[str, Any]],
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> dict[str, Any]:
        """Chat with tool/function calling support."""
        if not self._check_sdk():
            return {"content": "", "tool_calls": []}

        import lmstudio

        try:
            llm = self.get_model(model)
            chat = lmstudio.Chat(system_prompt)
            chat.add_user_message(prompt)

            tool_defs = [
                lmstudio.ToolDefinition(
                    name=t.get("name", ""),
                    description=t.get("description", ""),
                    parameters=t.get("parameters", {}),
                )
                for t in tools
            ]

            config = self._chat_handler._build_prediction_config(True, **kwargs)
            result = llm.respond(chat, tools=tool_defs, config=config)

            tool_calls = []
            if hasattr(result, "tool_calls") and result.tool_calls:
                for tc in result.tool_calls:
                    tool_calls.append(
                        {
                            "name": tc.name,
                            "arguments": tc.arguments,
                        }
                    )

            return {
                "content": str(result),
                "tool_calls": tool_calls,
            }
        except Exception as e:
            logger.error(f"LM Studio tool calling error: {e}")
            return {"content": "", "tool_calls": []}

    def health_check(self) -> bool:
        """Check if LM Studio is reachable and has models loaded."""
        try:
            models = self.list_loaded_models()
            is_healthy = bool(models)
            self._update_status(self.PROVIDER_ID, is_healthy)
            return is_healthy
        except Exception as e:
            logger.debug(f"Health check failed: {e}")
            self._update_status(self.PROVIDER_ID, False)
            return False

    def get_info(self) -> dict[str, Any]:
        """Get backend information, including REST API version and server details."""
        loaded = self.list_loaded_models()
        downloaded = self.list_downloaded_models()
        
        # Fetch server info via API client
        api_info = self._api_client.get_info()

        return {
            "provider": self.PROVIDER_ID,
            "host": self.config.api_host,
            "base_url": self.config.base_url,
            "api_base_url": api_info.get("api_base_url"),
            "sdk_available": self._check_sdk(),
            "api_version": api_info.get("api_version"),
            "loaded_models": loaded,
            "downloaded_models": downloaded,
            "is_healthy": bool(loaded),
        }

