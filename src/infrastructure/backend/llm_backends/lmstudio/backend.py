# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
LM Studio LLM backend implementation.
"""

import logging
import time
from typing import (
    Any,
    Callable,
    Iterator,
    Optional,
    Sequence,
    TYPE_CHECKING,
)

from ..llm_backend import LLMBackend
from .models import LMStudioConfig
from .cache import ModelCache

if TYPE_CHECKING:
    import lmstudio

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
        self._client: Optional["lmstudio.Client"] = None
        self._async_client: Optional["lmstudio.AsyncClient"] = None
        self._sdk_available: bool | None = None
    
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
    
    def _get_client(self) -> "lmstudio.Client":
        """Get or create sync client."""
        if self._client is not None:
            return self._client
        
        if not self._check_sdk():
            raise RuntimeError("LM Studio SDK not available")
        
        import lmstudio
        
        try:
            self._client = lmstudio.Client(self.config.api_host)
            logger.info(f"Connected to LM Studio at {self.config.api_host}")
            return self._client
        except Exception as e:
            logger.error(f"Failed to connect to LM Studio: {e}")
            self._update_status(self.PROVIDER_ID, False)
            raise
    
    def _get_async_client(self) -> "lmstudio.AsyncClient":
        """Get or create async client."""
        if self._async_client is not None:
            return self._async_client
        
        if not self._check_sdk():
            raise RuntimeError("LM Studio SDK not available")
        
        import lmstudio
        
        try:
            self._async_client = lmstudio.AsyncClient(self.config.api_host)
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
            self._async_client = None
        
        self._model_cache.clear()
    
    def list_loaded_models(self) -> list[str]:
        """List currently loaded models in LM Studio."""
        try:
            import lmstudio
            models = lmstudio.list_loaded_models()
            return [m.path for m in models]
        except Exception as e:
            logger.debug(f"Failed to list loaded models: {e}")
            return []
    
    def list_downloaded_models(self) -> list[str]:
        """List downloaded models available in LM Studio."""
        try:
            import lmstudio
            models = lmstudio.list_downloaded_models()
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
            if model:
                llm = lmstudio.llm(model)
            else:
                llm = lmstudio.llm()
            
            if self.config.cache_models:
                self._model_cache.set(cache_key, llm)
            
            return llm
        except lmstudio.LMStudioModelNotFoundError:
            logger.warning(f"Model '{model}' not found in LM Studio")
            raise
        except Exception as e:
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
            chat = lmstudio.Chat(system_prompt)
            chat.add_user_message(prompt)
            config = self._build_prediction_config(**kwargs)
            
            start_time = time.time()
            result = llm.respond(chat, config=config)
            elapsed = time.time() - start_time
            
            response_text = str(result)
            
            logger.debug(f"LM Studio response in {elapsed:.2f}s: {len(response_text)} chars")
            
            self._record(
                self.PROVIDER_ID,
                model or "default",
                prompt,
                response_text,
                system_prompt=system_prompt,
            )
            self._update_status(self.PROVIDER_ID, True)
            
            return response_text
            
        except lmstudio.LMStudioModelNotFoundError as e:
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
        except lmstudio.LMStudioTimeoutError as e:
            logger.warning(f"LM Studio timeout: {e}")
            self._update_status(self.PROVIDER_ID, False)
            return ""
        except lmstudio.LMStudioError as e:
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
        except Exception as e:
            logger.debug(f"LM Studio call failed: {e}")
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
        """Stream chat completion tokens."""
        if not self._check_sdk():
            return
        
        import lmstudio
        
        try:
            llm = self.get_model(model)
            chat = lmstudio.Chat(system_prompt)
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
            async with lmstudio.AsyncClient(self.config.api_host) as client:
                llm = await client.llm.get(model) if model else await client.llm.get()
                
                chat = lmstudio.Chat(system_prompt)
                chat.add_user_message(prompt)
                config = self._build_prediction_config(**kwargs)
                
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
        
        import lmstudio
        
        try:
            if model:
                emb_model = lmstudio.embedding_model(model)
            else:
                emb_model = lmstudio.embedding_model()
            
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
            
            config = self._build_prediction_config(**kwargs)
            
            result = llm.respond(chat, tools=tool_defs, config=config)
            
            tool_calls = []
            if hasattr(result, "tool_calls") and result.tool_calls:
                for tc in result.tool_calls:
                    tool_calls.append({
                        "name": tc.name,
                        "arguments": tc.arguments,
                    })
            
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
        
        return lmstudio.LlmPredictionConfig(
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            top_p=kwargs.get("top_p", self.config.top_p),
            stop_strings=kwargs.get("stop", []),
        )
    
    def health_check(self) -> bool:
        """Check if LM Studio is reachable and has models loaded."""
        try:
            models = self.list_loaded_models()
            is_healthy = bool(models)
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
            "is_healthy": bool(loaded),
        }
