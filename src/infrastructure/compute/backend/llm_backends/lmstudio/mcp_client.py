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
LM Studio MCP client and SDK session management.
"""

import inspect
import logging
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    import lmstudio

logger = logging.getLogger(__name__)


class MCPClient:
    """Manager for LM Studio SDK clients and sessions with Model Context Protocol support."""

    def __init__(self, base_url: str, api_token: Optional[str] = None):
        """Initialize MCP client manager.
        
        Args:
            base_url: Base URL for LM Studio API.
            api_token: Optional API token for authentication.
        """
        self.base_url = base_url
        self.api_token = api_token
        self._sync_client: Optional["lmstudio.Client"] = None
        self._async_client: Optional["lmstudio.AsyncClient"] = None

    def get_sync_client(self) -> "lmstudio.Client":
        """Get or create synchronous SDK client.
        
        Returns:
            lmstudio.Client instance.
        """
        if self._sync_client is not None:
            return self._sync_client
        
        import lmstudio
        
        try:
            api_url = self.base_url
            # Ensure scheme is present
            if not api_url.startswith("http://") and not api_url.startswith("https://"):
                api_url = "http://" + api_url
            
            self._sync_client = lmstudio.Client(api_url)
            logger.info(f"[LMStudio] Connected to LM Studio at {api_url}")
            return self._sync_client
        except Exception as e:
            logger.error(f"[LMStudio] Failed to connect sync client: {e}")
            raise

    def get_async_client(self) -> "lmstudio.AsyncClient":
        """Get or create asynchronous SDK client.
        
        Returns:
            lmstudio.AsyncClient instance.
        """
        if self._async_client is not None:
            return self._async_client
        
        import lmstudio
        
        try:
            api_url = self.base_url
            # Ensure scheme is present
            if not api_url.startswith("http://") and not api_url.startswith("https://"):
                api_url = "http://" + api_url
            
            self._async_client = lmstudio.AsyncClient(api_url)
            logger.info(f"[LMStudio] Created async client to LM Studio at {api_url}")
            return self._async_client
        except Exception as e:
            logger.error(f"[LMStudio] Failed to create async client: {e}")
            raise

    def get_llm(self, client: Any, model: str = "") -> Any:
        """Fetch LLM model from SDK client.
        
        Handles multiple SDK accessor styles:
        - accessor with `.get()` method
        - callable accessor
        - module-level helper fallback
        
        Args:
            client: SDK Client instance.
            model: Model identifier (optional).
        
        Returns:
            LLM model handle.
        """
        import lmstudio
        
        llm_accessor = client.llm
        logger.debug(
            f"[LMStudio] LLM accessor type={type(llm_accessor)} "
            f"has_get={hasattr(llm_accessor, 'get')} callable={callable(llm_accessor)}"
        )
        
        # Try `.get()` method if present
        if hasattr(llm_accessor, "get"):
            llm = llm_accessor.get(model) if model else llm_accessor.get()
            logger.debug(f"[LMStudio] Got LLM via .get() accessor: {type(llm)}")
            return llm
        
        # Try callable accessor
        if callable(llm_accessor):
            try:
                llm = llm_accessor(model) if model else llm_accessor()
                logger.debug(f"[LMStudio] Got LLM via callable accessor: {type(llm)}")
                return llm
            except TypeError:
                logger.debug("[LMStudio] Callable accessor failed, trying module-level helper")
        
        # Fallback to module-level helper
        llm = lmstudio.llm(model) if model else lmstudio.llm()
        logger.debug(f"[LMStudio] Got LLM via module-level helper: {type(llm)}")
        return llm

    async def get_async_llm(self, client: Any, model: str = "") -> Any:
        """Fetch LLM model from async SDK client.
        
        Handles multiple SDK accessor styles with async support.
        
        Args:
            client: Async SDK Client instance.
            model: Model identifier (optional).
        
        Returns:
            Async LLM model handle.
        """
        import lmstudio
        
        llm_accessor = client.llm
        
        # Try async `.get()` method if present
        if hasattr(llm_accessor, "get"):
            maybe = llm_accessor.get(model) if model else llm_accessor.get()
            if inspect.isawaitable(maybe):
                return await maybe
            return maybe
        
        # Try callable accessor which may return awaitable
        if callable(llm_accessor):
            try:
                maybe = llm_accessor(model) if model else llm_accessor()
                if inspect.isawaitable(maybe):
                    return await maybe
                return maybe
            except TypeError:
                logger.debug("[LMStudio] Async callable accessor failed, trying module-level helper")
        
        # Fallback to module-level helper (returns sync model)
        return lmstudio.llm(model) if model else lmstudio.llm()

    def get_embedding_model(self, client: Any, model: str = "") -> Any:
        """Fetch embedding model from SDK client.
        
        Args:
            client: SDK Client instance.
            model: Model identifier (optional).
        
        Returns:
            Embedding model handle.
        """
        import lmstudio
        
        if hasattr(client, "embedding_model"):
            emb_accessor = client.embedding_model
            if hasattr(emb_accessor, "get"):
                return emb_accessor.get(model) if model else emb_accessor.get()
            if callable(emb_accessor):
                try:
                    return emb_accessor(model) if model else emb_accessor()
                except TypeError:
                    pass
        
        # Fallback to module-level helper
        return lmstudio.embedding_model(model) if model else lmstudio.embedding_model()

    def close(self) -> None:
        """Close all SDK clients."""
        if self._sync_client is not None:
            try:
                self._sync_client.close()
            except Exception as e:
                logger.warning(f"[LMStudio] Error closing sync client: {e}")
            self._sync_client = None
        
        if self._async_client is not None:
            self._async_client = None
