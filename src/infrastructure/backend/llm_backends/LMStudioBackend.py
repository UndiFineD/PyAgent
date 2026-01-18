"""
LM Studio Backend
==================

Phase 21: LM Studio integration using the official lmstudio SDK.
Provides both sync and async chat completions with streaming support.

Features:
- Native WebSocket-based communication (via httpx-ws)
- Msgspec for high-performance serialization
- Automatic model discovery and loading
- Streaming predictions with callbacks
- Tool/function calling support
- Embedding model support

Dependencies:
- lmstudio (1.5.0+)
- httpx-ws
- msgspec
- wsproto
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Iterator,
    Optional,
    Sequence,
    TYPE_CHECKING,
)

from .LLMBackend import LLMBackend

if TYPE_CHECKING:
    import lmstudio


# =============================================================================
# Configuration
# =============================================================================


@dataclass
class LMStudioConfig:
    """Configuration for LM Studio connection."""
    
    # Connection settings
    host: str = field(default_factory=lambda: os.environ.get("LMSTUDIO_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.environ.get("LMSTUDIO_PORT", "1234")))
    
    # Timeout settings
    timeout: float = 60.0
    connect_timeout: float = 10.0
    
    # Model settings
    default_model: str = ""  # Empty means use any loaded model
    auto_load: bool = True  # Auto-load model if not loaded
    
    # Prediction settings
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95
    
    # Caching
    cache_models: bool = True
    cache_ttl: float = 300.0  # 5 minutes
    
    @property
    def api_host(self) -> str:
        """Return host:port string."""
        return f"{self.host}:{self.port}"


# =============================================================================
# Model Cache
# =============================================================================


@dataclass
class CachedModel:
    """Cached model reference with TTL."""
    
    model_id: str
    model_info: Any
    loaded_at: float
    last_used: float = field(default_factory=time.time)
    
    def is_expired(self, ttl: float) -> bool:
        """Check if cache entry is expired."""
        return time.time() - self.last_used > ttl
    
    def touch(self) -> None:
        """Update last used timestamp."""
        self.last_used = time.time()


class ModelCache:
    """Simple model cache with TTL."""
    
    def __init__(self, ttl: float = 300.0):
        self._cache: dict[str, CachedModel] = {}
        self._ttl = ttl
    
    def get(self, model_id: str) -> CachedModel | None:
        """Get cached model if not expired."""
        entry = self._cache.get(model_id)
        if entry is None:
            return None
        if entry.is_expired(self._ttl):
            del self._cache[model_id]
            return None
        entry.touch()
        return entry
    
    def set(self, model_id: str, model_info: Any) -> CachedModel:
        """Cache a model reference."""
        entry = CachedModel(
            model_id=model_id,
            model_info=model_info,
            loaded_at=time.time(),
        )
        self._cache[model_id] = entry
        return entry
    
    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()
    
    def prune_expired(self) -> int:
        """Remove expired entries, return count removed."""
        expired = [k for k, v in self._cache.items() if v.is_expired(self._ttl)]
        for k in expired:
            del self._cache[k]
        return len(expired)


# =============================================================================
# LM Studio Backend
# =============================================================================


class LMStudioBackend(LLMBackend):
    """
    LM Studio LLM Backend using the official SDK.
    
    Provides high-performance local inference via WebSocket connection
    to LM Studio's API server.
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
    
    # -------------------------------------------------------------------------
    # SDK Availability
    # -------------------------------------------------------------------------
    
    def _check_sdk(self) -> bool:
        """Check if LM Studio SDK is available."""
        if self._sdk_available is not None:
            return self._sdk_available
        
        try:
            import lmstudio
            self._sdk_available = True
            logging.debug(f"LM Studio SDK version: {lmstudio.__version__}")
            return True
        except ImportError:
            self._sdk_available = False
            logging.warning("LM Studio SDK not available. Install with: pip install lmstudio")
            return False
    
    # -------------------------------------------------------------------------
    # Client Management
    # -------------------------------------------------------------------------
    
    def _get_client(self) -> "lmstudio.Client":
        """Get or create sync client."""
        if self._client is not None:
            return self._client
        
        if not self._check_sdk():
            raise RuntimeError("LM Studio SDK not available")
        
        import lmstudio
        
        try:
            self._client = lmstudio.Client(self.config.api_host)
            logging.info(f"Connected to LM Studio at {self.config.api_host}")
            return self._client
        except Exception as e:
            logging.error(f"Failed to connect to LM Studio: {e}")
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
            logging.info(f"Async connected to LM Studio at {self.config.api_host}")
            return self._async_client
        except Exception as e:
            logging.error(f"Failed to create async LM Studio client: {e}")
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
            # Async client should be closed in async context
            self._async_client = None
        
        self._model_cache.clear()
    
    # -------------------------------------------------------------------------
    # Model Management
    # -------------------------------------------------------------------------
    
    def list_loaded_models(self) -> list[str]:
        """List currently loaded models in LM Studio."""
        try:
            import lmstudio
            models = lmstudio.list_loaded_models()
            return [m.path for m in models]
        except Exception as e:
            logging.debug(f"Failed to list loaded models: {e}")
            return []
    
    def list_downloaded_models(self) -> list[str]:
        """List downloaded models available in LM Studio."""
        try:
            import lmstudio
            models = lmstudio.list_downloaded_models()
            return [m.path for m in models]
        except Exception as e:
            logging.debug(f"Failed to list downloaded models: {e}")
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
                # Specific model requested
                llm = lmstudio.llm(model)
            else:
                # Get any loaded model
                llm = lmstudio.llm()
            
            # Cache the model handle
            if self.config.cache_models:
                self._model_cache.set(cache_key, llm)
            
            return llm
        except lmstudio.LMStudioModelNotFoundError:
            logging.warning(f"Model '{model}' not found in LM Studio")
            raise
        except Exception as e:
            logging.error(f"Failed to get model '{model}': {e}")
            raise
    
    # -------------------------------------------------------------------------
    # Chat Completion (Sync)
    # -------------------------------------------------------------------------
    
    def chat(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """
        Execute a chat completion via LM Studio.
        
        Args:
            prompt: User message
            model: Model identifier (empty = any loaded model)
            system_prompt: System message
            **kwargs: Additional options (temperature, max_tokens, etc.)
        
        Returns:
            Generated response text
        """
        if not self._is_working(self.PROVIDER_ID):
            logging.debug("LM Studio skipped due to connection cache.")
            return ""
        
        if not self._check_sdk():
            return ""
        
        import lmstudio
        
        try:
            # Get model handle
            llm = self.get_model(model)
            
            # Build chat history
            chat = lmstudio.Chat(system_prompt)
            chat.add_user_message(prompt)
            
            # Build prediction config
            config = self._build_prediction_config(**kwargs)
            
            # Execute prediction
            start_time = time.time()
            result = llm.respond(chat, config=config)
            elapsed = time.time() - start_time
            
            # Extract response text
            response_text = str(result)
            
            logging.debug(f"LM Studio response in {elapsed:.2f}s: {len(response_text)} chars")
            
            # Record interaction
            self._record(
                self.PROVIDER_ID,
                model or "default",
                prompt,
                response_text,
                system_prompt=system_prompt,
            )
            
            # Update status
            self._update_status(self.PROVIDER_ID, True)
            
            return response_text
            
        except lmstudio.LMStudioModelNotFoundError as e:
            logging.warning(f"LM Studio model not found: {e}")
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
            logging.warning(f"LM Studio timeout: {e}")
            self._update_status(self.PROVIDER_ID, False)
            return ""
            
        except lmstudio.LMStudioError as e:
            logging.error(f"LM Studio error: {e}")
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
            logging.debug(f"LM Studio call failed: {e}")
            self._update_status(self.PROVIDER_ID, False)
            return ""
    
    # -------------------------------------------------------------------------
    # Streaming Chat (Sync)
    # -------------------------------------------------------------------------
    
    def chat_stream(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        on_fragment: Callable[[str], None] | None = None,
        **kwargs,
    ) -> Iterator[str]:
        """
        Stream chat completion tokens.
        
        Args:
            prompt: User message
            model: Model identifier
            system_prompt: System message
            on_fragment: Optional callback for each fragment
            **kwargs: Additional options
        
        Yields:
            Response text fragments
        """
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
            
            # Record complete response
            self._record(
                self.PROVIDER_ID,
                model or "default",
                prompt,
                "".join(full_response),
                system_prompt=system_prompt,
            )
            self._update_status(self.PROVIDER_ID, True)
            
        except Exception as e:
            logging.error(f"LM Studio streaming error: {e}")
            self._update_status(self.PROVIDER_ID, False)
    
    # -------------------------------------------------------------------------
    # Async Chat Completion
    # -------------------------------------------------------------------------
    
    async def chat_async(
        self,
        prompt: str,
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """
        Async chat completion via LM Studio.
        
        Args:
            prompt: User message
            model: Model identifier
            system_prompt: System message
            **kwargs: Additional options
        
        Returns:
            Generated response text
        """
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
            logging.error(f"LM Studio async error: {e}")
            self._update_status(self.PROVIDER_ID, False)
            return ""
    
    # -------------------------------------------------------------------------
    # Embeddings
    # -------------------------------------------------------------------------
    
    def embed(
        self,
        texts: str | Sequence[str],
        model: str = "",
    ) -> list[list[float]]:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text or list of texts
            model: Embedding model identifier
        
        Returns:
            List of embedding vectors
        """
        if not self._check_sdk():
            return []
        
        import lmstudio
        
        try:
            # Get embedding model
            if model:
                emb_model = lmstudio.embedding_model(model)
            else:
                emb_model = lmstudio.embedding_model()
            
            # Normalize input
            if isinstance(texts, str):
                texts = [texts]
            
            # Generate embeddings
            embeddings = []
            for text in texts:
                vec = emb_model.embed(text)
                embeddings.append(list(vec))
            
            return embeddings
            
        except Exception as e:
            logging.error(f"LM Studio embedding error: {e}")
            return []
    
    # -------------------------------------------------------------------------
    # Tool Calling
    # -------------------------------------------------------------------------
    
    def chat_with_tools(
        self,
        prompt: str,
        tools: list[dict[str, Any]],
        model: str = "",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> dict[str, Any]:
        """
        Chat with tool/function calling support.
        
        Args:
            prompt: User message
            tools: List of tool definitions
            model: Model identifier
            system_prompt: System message
            **kwargs: Additional options
        
        Returns:
            Dict with 'content' and optional 'tool_calls'
        """
        if not self._check_sdk():
            return {"content": "", "tool_calls": []}
        
        import lmstudio
        
        try:
            llm = self.get_model(model)
            chat = lmstudio.Chat(system_prompt)
            chat.add_user_message(prompt)
            
            # Convert tools to LM Studio format
            tool_defs = [
                lmstudio.ToolDefinition(
                    name=t.get("name", ""),
                    description=t.get("description", ""),
                    parameters=t.get("parameters", {}),
                )
                for t in tools
            ]
            
            config = self._build_prediction_config(**kwargs)
            
            # Execute with tools
            result = llm.respond(chat, tools=tool_defs, config=config)
            
            # Check for tool calls
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
            logging.error(f"LM Studio tool calling error: {e}")
            return {"content": "", "tool_calls": []}
    
    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    
    def _build_prediction_config(self, **kwargs) -> "lmstudio.LlmPredictionConfig":
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


# =============================================================================
# Convenience Functions
# =============================================================================


def lmstudio_chat(
    prompt: str,
    model: str = "",
    system_prompt: str = "You are a helpful assistant.",
    **kwargs,
) -> str:
    """
    Convenience function for quick LM Studio chat.
    
    Example:
        >>> response = lmstudio_chat("What is Python?")
        >>> print(response)
    """
    try:
        import lmstudio
        
        llm = lmstudio.llm(model) if model else lmstudio.llm()
        chat = lmstudio.Chat(system_prompt)
        chat.add_user_message(prompt)
        
        result = llm.respond(chat)
        return str(result)
        
    except Exception as e:
        logging.error(f"lmstudio_chat error: {e}")
        return ""


def lmstudio_stream(
    prompt: str,
    model: str = "",
    system_prompt: str = "You are a helpful assistant.",
) -> Iterator[str]:
    """
    Convenience function for streaming LM Studio chat.
    
    Example:
        >>> for chunk in lmstudio_stream("Tell me a story"):
        ...     print(chunk, end="", flush=True)
    """
    try:
        import lmstudio
        
        llm = lmstudio.llm(model) if model else lmstudio.llm()
        chat = lmstudio.Chat(system_prompt)
        chat.add_user_message(prompt)
        
        for fragment in llm.respond_stream(chat):
            yield str(fragment)
            
    except Exception as e:
        logging.error(f"lmstudio_stream error: {e}")


async def lmstudio_chat_async(
    prompt: str,
    model: str = "",
    system_prompt: str = "You are a helpful assistant.",
    host: str = "localhost:1234",
) -> str:
    """
    Async convenience function for LM Studio chat.
    
    Example:
        >>> response = await lmstudio_chat_async("What is async?")
    """
    try:
        import lmstudio
        
        async with lmstudio.AsyncClient(host) as client:
            llm = await client.llm.get(model) if model else await client.llm.get()
            
            chat = lmstudio.Chat(system_prompt)
            chat.add_user_message(prompt)
            
            result = await llm.respond(chat)
            return str(result)
            
    except Exception as e:
        logging.error(f"lmstudio_chat_async error: {e}")
        return ""
