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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent for performing web searches and deep research."""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function
import logging
import os
import requests
import time
from pathlib import Path
from typing import Optional
from src.core.base.ConnectivityManager import ConnectivityManager
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
from .SearchCore import SearchCore

__version__ = VERSION

class SearchAgent(BaseAgent):
    """Agent that specializes in researching topics via web search."""

    def __init__(self, context: str) -> None:
        super().__init__(context)
        self.bing_api_key: str | None = os.environ.get("BING_SEARCH_V7_SUBSCRIPTION_KEY")
        self.bing_endpoint: str = os.environ.get("BING_SEARCH_V7_ENDPOINT", "https://api.bing.microsoft.com/v7.0/search")
        self.google_api_key: str | None = os.environ.get("GOOGLE_SEARCH_API_KEY")
        self.google_cse_id: str | None = os.environ.get("GOOGLE_SEARCH_CSE_ID")
        
        # Phase 108: Robustness and Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)
        self.connectivity: ConnectivityManager = ConnectivityManager(work_root)
        self.recorder: LocalContextRecorder | None = LocalContextRecorder(Path(work_root)) if work_root else None
        self.core: SearchCore = SearchCore()
        
        logging.info(f"SearchAgent initialized for topic: {context}")

    def _get_default_content(self) -> str:
        return "# Research Report\n\n## Topic\n[Topic here]\n\n## Findings\n- Pending search...\n"

    def _record(self, provider: str, query: str, result: str) -> None:
        """Harvest search logic for future self-improvement."""
        if self.recorder:
            try:
                meta = {"phase": 116, "type": "search", "timestamp": time.time()}
                self.recorder.record_interaction(provider, "search-v2", query, result, meta=meta)
            except Exception as e:
                logging.error(f"SearchAgent: Transcription error: {e}")

    def _search_duckduckgo(self, query: str, max_results: int = 5) -> str:
        """Fallback/Default search using DuckDuckGo."""
        if not self.connectivity.is_endpoint_available("duckduckgo"):
            return "DuckDuckGo skipped due to connection cache (offline)."

        try:
            from duckduckgo_search import DDGS
            logging.info(f"Performing DuckDuckGo search for: {query}")
            
            with DDGS() as ddgs:
                raw_results = list(ddgs.text(query, max_results=max_results))
                results = self.core.parse_ddg_results(raw_results)
            
            res_str = self.core.format_results_block(results, "DDG")
            self.connectivity.update_status("duckduckgo", True)
            self._record("duckduckgo", query, res_str)
            return res_str
        except Exception as e:
            self.connectivity.update_status("duckduckgo", False)
            logging.error(f"DDG search failed: {e}")
            return f"DDG search failed (offline or rate-limited): {e}"

    def _search_bing(self, query: str, max_results: int = 5) -> str:
        """Native Bing Search API."""
        if not self.bing_api_key:
            return "Bing API key not configured."
        
        if not self.connectivity.is_endpoint_available("bing"):
            return "Bing skipped due to connection cache (offline)."
        
        try:
            # Use a session with limited redirects for security (Phase 115 Patch)
            with requests.Session() as session:
                session.max_redirects = 5
                headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key or ""}
                params = {"q": query, "textDecorations": True, "textFormat": "HTML", "count": max_results}
                response = session.get(self.bing_endpoint, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                search_results = response.json()
            
            results = self.core.parse_bing_results(search_results)
            res_str = self.core.format_results_block(results, "Bing")
            
            self.connectivity.update_status("bing", True)
            self._record("bing", query, res_str)
            return res_str
        except Exception as e:
            self.connectivity.update_status("bing", False)
            logging.error(f"Bing search failed: {e}")
            return f"Bing search failed: {e}"

    def _search_google(self, query: str, max_results: int = 5) -> str:
        """Native Google Custom Search API."""
        if not self.google_api_key or not self.google_cse_id:
            return "Google API credentials not configured."
        
        if not self.connectivity.is_endpoint_available("google"):
            return "Google skipped due to connection cache (offline)."
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {"key": self.google_api_key, "cx": self.google_cse_id, "q": query, "num": max_results}
            with requests.Session() as session:
                session.max_redirects = 5
                response = session.get(url, params=params, timeout=10)
                response.raise_for_status()
                search_results = response.json()
            
            results = self.core.parse_google_results(search_results)
            res_str = self.core.format_results_block(results, "Google")
            
            self.connectivity.update_status("google", True)
            self._record("google", query, res_str)
            return res_str
        except Exception as e:
            self.connectivity.update_status("google", False)
            logging.error(f"Google search failed: {e}")
            return f"Google search failed: {e}"

    def perform_search(self, query: str) -> str:
        """Perform a web search trying multiple backends.
        
        Prioritizes Google -> Bing -> DuckDuckGo.
        """
        logging.info(f"Initiating multi-backend search for: {query}")
        
        # Try Google
        if self.google_api_key and self.google_cse_id:
            res = self._search_google(query)
            if "failed" not in res.lower() and "not configured" not in res.lower():
                return res
        
        # Try Bing
        if self.bing_api_key:
            res = self._search_bing(query)
            if "failed" not in res.lower() and "not configured" not in res.lower():
                return res
        
        # Fallback to DDG
        return self._search_duckduckgo(query)

    def improve_content(self, prompt: str) -> str:
        """Perform research based on the topic and prompt."""
        # Step 1: Perform real search
        search_results = self.perform_search(prompt)
        
        # Step 2: Use AI to synthesize the results
        research_prompt = (
            f"You are a Research Agent. Your task is to perform deep research on the following topic: {self.file_path}\n"
            f"Specific focus: {prompt}\n\n"
            f"Here are REAL search results retrieved for your query:\n\n{search_results}\n\n"
            "Based on these results and your internal knowledge, provide a comprehensive report."
        )
        return super().improve_content(research_prompt)

if __name__ == "__main__":
    main = create_main_function(SearchAgent, "Research Agent", "Topic/File to research")
    main()