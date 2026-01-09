#!/usr/bin/env python3

"""Agent for performing web searches and deep research."""

from __future__ import annotations

from src.classes.base_agent.agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function
import logging
import os
import requests
import time
from pathlib import Path
from typing import Optional, List, Dict
from src.classes.base_agent.ConnectivityManager import ConnectivityManager
from src.classes.backend.LocalContextRecorder import LocalContextRecorder

class SearchAgent(BaseAgent):
    """Agent that specializes in researching topics via web search."""

    def __init__(self, context: str) -> None:
        super().__init__(context)
        self.bing_api_key = os.environ.get("BING_SEARCH_V7_SUBSCRIPTION_KEY")
        self.bing_endpoint = os.environ.get("BING_SEARCH_V7_ENDPOINT", "https://api.bing.microsoft.com/v7.0/search")
        self.google_api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
        self.google_cse_id = os.environ.get("GOOGLE_SEARCH_CSE_ID")
        
        # Phase 108: Robustness and Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)
        self.connectivity = ConnectivityManager(work_root)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None
        
        logging.info(f"SearchAgent initialized for topic: {context}")

    def _get_default_content(self) -> str:
        return "# Research Report\n\n## Topic\n[Topic here]\n\n## Findings\n- Pending search...\n"

    def _record(self, provider: str, query: str, result: str) -> None:
        """Harvest search logic for future self-improvement."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "search", "timestamp": time.time()}
                self.recorder.record_interaction(provider, "search-v1", query, result, meta=meta)
            except Exception as e:
                logging.error(f"SearchAgent: Transcription error: {e}")

    def _search_duckduckgo(self, query: str, max_results: int = 5) -> str:
        """Fallback/Default search using DuckDuckGo."""
        if not self.connectivity.is_endpoint_available("duckduckgo"):
            return "DuckDuckGo skipped due to connection cache."

        try:
            from duckduckgo_search import DDGS
            logging.info(f"Performing DuckDuckGo search for: {query}")
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append(f"### {r['title']}\nURL: {r['href']}\n{r['body']}\n")
            
            res_str = "\n".join(results) if results else "No DDG results found."
            self.connectivity.update_status("duckduckgo", True)
            self._record("duckduckgo", query, res_str)
            return res_str
        except Exception as e:
            self.connectivity.update_status("duckduckgo", False)
            return f"DDG search failed: {e}"

    def _search_bing(self, query: str, max_results: int = 5) -> str:
        """Native Bing Search API."""
        if not self.bing_api_key:
            return "Bing API key not configured."
        
        if not self.connectivity.is_endpoint_available("bing"):
            return "Bing skipped due to connection cache."
        
        try:
            headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
            params = {"q": query, "textDecorations": True, "textFormat": "HTML", "count": max_results}
            response = requests.get(self.bing_endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            search_results = response.json()
            
            results = []
            for v in search_results.get("webPages", {}).get("value", []):
                results.append(f"### {v['name']}\nURL: {v['url']}\n{v['snippet']}\n")
            
            res_str = "\n".join(results) if results else "No Bing results found."
            self.connectivity.update_status("bing", True)
            self._record("bing", query, res_str)
            return res_str
        except Exception as e:
            self.connectivity.update_status("bing", False)
            return f"Bing search failed: {e}"

    def _search_google(self, query: str, max_results: int = 5) -> str:
        """Native Google Custom Search API."""
        if not self.google_api_key or not self.google_cse_id:
            return "Google API credentials not configured."
        
        if not self.connectivity.is_endpoint_available("google"):
            return "Google skipped due to connection cache."
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {"key": self.google_api_key, "cx": self.google_cse_id, "q": query, "num": max_results}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            search_results = response.json()
            
            results = []
            for item in search_results.get("items", []):
                results.append(f"### {item['title']}\nURL: {item['link']}\n{item['snippet']}\n")
            
            res_str = "\n".join(results) if results else "No Google results found."
            self.connectivity.update_status("google", True)
            self._record("google", query, res_str)
            return res_str
        except Exception as e:
            self.connectivity.update_status("google", False)
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
