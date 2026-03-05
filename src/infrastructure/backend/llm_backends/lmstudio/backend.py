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

import logging
import time
from typing import (
    Any,
    Callable,
    Iterator,
    Optional,
    Sequence,
)

from src.infrastructure.compute.backend.llm_backends.llm_backend import LLMBackend
from .models import LMStudioConfig
from .cache import ModelCache

try:
    import lmstudio
except ImportError:
    lmstudio = None

logger = logging.getLogger(__name__)


class LMStudioBackend(LLMBackend):
    """
    LM Studio LLM Backend using the official SDK.
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
        self._client: Optional[Any] = None
        self._async_client: Optional[Any] = None
        self._sdk_available: bool | None = None

    def _check_sdk(self) -> bool:
        """Check if LM Studio SDK is available."""
        if self._sdk_available is not None:
            return self._sdk_available

        try:
            import lmstudio

            self._sdk_available = True
            version = getattr(lmstudio, "__version__", "unknown")
            logger.debug(f"LM Studio SDK available (version: {version})")
            return True
        except ImportError:
            self._sdk_available = False
            logger.warning(
                "LM Studio SDK not available. Install with: pip install lmstudio"
            )
            return False

    def _get_client(self) -> "Any":
        """Get or create sync client."""
        if self._client is not None:
            return self._client

        if not self._check_sdk():
            raise RuntimeError("LM Studio SDK not available")

            import lmstudio

        try:
            client_class = getattr(lmstudio, "Client", None)
            if client_class is None:
                raise AttributeError("lmstudio.Client not found in SDK")
            if not callable(client_class):
                raise TypeError("lmstudio.Client is not callable")
            self._client: Any = client_class(self.config.api_host)  # type: ignore[misc]
            logger.info(f"Connected to LM Studio at {self.config.api_host}")
            return self._client
        except Exception as e:
            logger.error(f"Failed to connect to LM Studio: {e}")
            self._update_status(self.PROVIDER_ID, False)
            raise

    def _get_async_client(self) -> "Any":
        """Get or create async client."""
        if self._async_client is not None:
            return self._async_client

        if not self._check_sdk():
            raise RuntimeError("LM Studio SDK not available")

            import lmstudio

        try:
            # Attempt to get AsyncClient, fall back to Client if not available
            async_client_class = getattr(lmstudio, "AsyncClient", None)
            if async_client_class is not None:
                self._async_client = async_client_class(self.config.api_host)
            else:
                client_class = getattr(lmstudio, "Client", None)
                if client_class is not None:
                    self._async_client = client_class(self.config.api_host)
                else:
                    raise AttributeError(
                        "lmstudio.AsyncClient or lmstudio.Client not found in SDK"
                    )
            logger.info(f"Async connected to LM Studio at {self.config.api_host}")
            return self._async_client
        except Exception as e:
            logger.error(f"Failed to create async LM Studio client: {e}")
            raise

    def disconnect(self) -> None:
        """Disconnect clients."""
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

        if self._async_client is not None:
            try:
                self._async_client.close()
            except Exception:
                pass
            self._async_client = None

        self._model_cache.clear()

    def list_loaded_models(self) -> list[str]:
        """List currently loaded models in LM Studio."""
        try:
            client = self._get_client()
            models = client.llm.list_loaded()
            return [m.path for m in models]
        except Exception as e:
            logger.debug(f"Failed to list loaded models: {e}")
            return []

    def list_downloaded_models(self) -> list[str]:
        """List downloaded models available in LM Studio."""
        try:
            client = self._get_client()
            models = client.llm.list_available()
            return [m.path for m in models]
        except Exception as e:
            logger.debug(f"Failed to list downloaded models: {e}")
            return []

    def get_model(self, model: str = "") -> Any:
        """Get a loaded model handle, using cache if available."""
        # Check cache first
        cache_key = model or "_default_"
        cached = self._model_cache.get(cache_key)
        if cached is not None:
            return cached.model_info

        import lmstudio

        try:
            client = self._get_client()
            if model:
                llm = client.llm.get(model)
            else:
                llm = client.llm.get()

            if self.config.cache_models:
                self._model_cache.set(cache_key, llm)
            return llm

        except Exception as e:
            if "not found" in str(e).lower() or "model" in str(e).lower():
                logger.warning(f"Model '{model}' not found in LM Studio")
            else:
                logger.error(f"Failed to get model '{model}': {e}")
            raise

    def chat(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """Execute a chat completion via LM Studio."""
        if not self._is_working(self.PROVIDER_ID):
            logger.debug("LM Studio skipped due to connection cache.")
            return ""

        if not self._check_sdk():
            return ""
        import lmstudio

        try:
            llm = self.get_model(model)
            chat = llm.create_chat_session()
            chat.add_system_message(system_prompt)
            chat.add_user_message(prompt)
            config = self._build_prediction_config(**kwargs)
            start_time = time.time()
            result = llm.respond(chat, config=config)
            elapsed = time.time() - start_time
            response_text = str(result)
            logger.debug(
                f"LM Studio response in {elapsed:.2f}s: {len(response_text)} chars"
            )
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
            if "timeout" in str(e).lower():
                logger.warning(f"LM Studio timeout: {e}")
                self._update_status(self.PROVIDER_ID, False)
                return ""
            elif "not found" in str(e).lower() or "model" in str(e).lower():
                logger.warning(f"LM Studio model not found: {e}")
                self._update_status(self.PROVIDER_ID, False)
                self._record(
                    self.PROVIDER_ID,
                    model or "default",
                    prompt,
                    f"ERROR: Model not found - {e}",
                    system_prompt=system_prompt,
                )
                return ""
            else:
                logger.error(f"LM Studio error: {e}")
                self._update_status(self.PROVIDER_ID, False)
                self._record(
                    self.PROVIDER_ID,
                    model or "default",
                    prompt,
                    f"ERROR: {e}",
                    system_prompt=system_prompt,
                )
                return ""

    def chat_stream(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        on_fragment: Callable[[str], None] | None = None,
        **kwargs,
    ) -> Iterator[str]:
        """Stream chat completion tokens."""
        if not self._check_sdk():
            return
        import lmstudio

        try:
            llm = self.get_model(model)
            chat = llm.create_chat_session()
            chat.add_system_message(system_prompt)
            chat.add_user_message(prompt)
            config = self._build_prediction_config(**kwargs)

            full_response = []
            for fragment in llm.respond_stream(chat, config=config):
                text = str(fragment)
                full_response.append(text)
                if on_fragment:
                    on_fragment(text)

                yield text

            self._record(
                self.PROVIDER_ID,
                model or "default",
                prompt,
                "".join(full_response),
                system_prompt=system_prompt,
            )
            self._update_status(self.PROVIDER_ID, True)

        except Exception as e:
            logger.error(f"LM Studio streaming error: {e}")
            self._update_status(self.PROVIDER_ID, False)
            if self._async_client is not None:
                try:
                    self._async_client.close()
                except Exception:
                    pass
                self._async_client = None

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
            # LM Studio SDK may not have AsyncClient; fall back to sync client
            if hasattr(lmstudio, "AsyncClient"):
                async_client = self._get_async_client()
                llm = (
                    await async_client.llm.get(model)
                    if model
                    else await async_client.llm.get()
                )
                chat = llm.create_chat_session()
                chat.add_system_message(system_prompt)
                chat.add_user_message(prompt)
                config = self._build_prediction_config(**kwargs)
                result = await llm.respond(chat, config=config)
                response_text = str(result)
            else:
                # Fall back to sync client in async context
                client = self._get_client()
                llm = client.llm.get(model) if model else client.llm.get()
                chat = llm.create_chat_session()
                chat.add_system_message(system_prompt)
                chat.add_user_message(prompt)
                config = self._build_prediction_config(**kwargs)
                result = llm.respond(chat, config=config)
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

        import lmstudio

        try:
            client = self._get_client()
            if model:
                emb_model = client.embedding_model.get(model)
            else:
                emb_model = client.embedding_model.get()

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
            chat = llm.create_chat_session()
            chat.add_system_message(system_prompt)
            chat.add_user_message(prompt)

            tool_defs = [
                {
                    "name": t.get("name", ""),
                    "description": t.get("description", ""),
                    "parameters": t.get("parameters", {}),
                }
                for t in tools
            ]

            config = self._build_prediction_config(**kwargs)
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

    def _build_prediction_config(self, **kwargs) -> Any:
        """Build prediction config from kwargs."""
        import lmstudio

        # Build config dict for lmstudio SDK
        config_dict = {
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "top_p": kwargs.get("top_p", self.config.top_p),
            "stop": kwargs.get("stop", []),
        }
        # Return dict or construct proper config object based on SDK version
        if hasattr(lmstudio, "PredictionConfig"):
            return getattr(lmstudio, "PredictionConfig")(**config_dict)
        if hasattr(lmstudio, "LLMPredictionConfig"):
            return getattr(lmstudio, "LLMPredictionConfig")(**config_dict)
        # Return dict if no config class available
        return config_dict

    def health_check(self) -> bool:
        """Check if LM Studio is reachable and has models loaded."""
        try:
            models = self.list_loaded_models()
            is_healthy = len(models) > 0
            self._update_status(self.PROVIDER_ID, is_healthy)
            return is_healthy
        except Exception:
            self._update_status(self.PROVIDER_ID, False)
            return False

    def get_info(self) -> dict[str, Any]:
        """Get backend information."""
        loaded = self.list_loaded_models()
        downloaded = self.list_downloaded_models()
        return {
            "provider": self.PROVIDER_ID,
            "host": self.config.api_host,
            "sdk_available": self._check_sdk(),
            "loaded_models": loaded,
            "downloaded_models": downloaded,
            "is_healthy": len(loaded) > 0,
        }
