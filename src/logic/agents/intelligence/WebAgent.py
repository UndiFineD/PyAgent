#!/usr/bin/env python3

"""Agent specializing in autonomous web navigation and information extraction."""

import logging
import requests
import time
from src.core.base.version import VERSION
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.logic.agents.development.SecurityGuardAgent import SecurityGuardAgent
from src.core.base.ConnectivityManager import ConnectivityManager
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
from src.logic.agents.intelligence.WebCore import WebCore

__version__ = VERSION

class WebAgent(BaseAgent):
    """Enables the fleet to perform autonomous research and interact with web services."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.security_guard = SecurityGuardAgent(file_path) # Reuse path for context
        self._system_prompt = (
            "You are the Web Navigation Agent. "
            "Your role is to browse the internet, extract relevant information, and interact with web forms. "
            "Prioritize accuracy and safety when crawling untrusted sites."
        )
        
        # Phase 108: Robustness and Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)
        self.connectivity = ConnectivityManager(work_root)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None
        self.core = WebCore()

    def _record(self, url: str, content: str) -> None:
        """Harvest web extraction logic for future self-improvement."""
        if self.recorder:
            try:
                meta = {"phase": 116, "type": "web_fetch", "timestamp": time.time()}
                self.recorder.record_interaction("web", url, "fetch_page_content", content[:1000], meta=meta)
            except Exception as e:
                logging.error(f"WebAgent: Transcription error: {e}")

    @as_tool
    def fetch_page_content(self, url: str) -> str:
        """Fetches and simplifies content from a URL with safety scanning."""
        import urllib.parse
        domain = urllib.parse.urlparse(url).netloc
        
        if not self.connectivity.is_endpoint_available(domain):
            return f"ERROR: Connection to {domain} skipped due to connection cache (offline)."

        logging.info(f"WebAgent fetching URL: {url}")
        try:
            # Use a session to limit redirects and enforce security (Phase 115 Security Patch)
            with requests.Session() as session:
                session.max_redirects = 10
                response = session.get(url, timeout=15, stream=True)
                
                # Decompression bomb safeguard: check content length if available
                content_length = response.headers.get('Content-Length')
                if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
                     return f"ERROR: Page content too large ({content_length} bytes). Aborting for safety."

                response.raise_for_status()
                
                # Update connectivity status on success
                self.connectivity.update_status(domain, True)
                
                # Use Core for cleaning
                text = self.core.clean_html(response.text)
                
                # Safety Scan
                injections = self.security_guard.scan_for_injection(text)
                if injections:
                    logging.warning(f"WebAgent blocked content from {url} due to safety risks: {injections}")
                    return f"ERROR: Content from {url} was blocked for safety reasons: {', '.join(injections)}"
                
                extracted = text[:5000]
                self._record(url, extracted)
                return extracted # Limit to avoid context overflow
        except Exception as e:
            self.connectivity.update_status(domain, False)
            return f"Error fetching {url}: {e}"

    @as_tool
    def search_web(self, query: str) -> List[str]:
        """Simulates a web search and returns top results (stub for real API integration)."""
        logging.info(f"WebAgent searching for: {query}")
        # In a real implementation, this would call Google/DuckDuckGo/Serper
        return [
            f"https://github.com/search?q={query}",
            f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        ]

    def improve_content(self, prompt: str) -> str:
        """Handle web-related requests."""
        if "fetch" in prompt.lower() or "read" in prompt.lower():
            # Basic parsing of URL from prompt
            import re
            urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', prompt)
            if urls:
                return self.fetch_page_content(urls[0])
        return f"WebAgent processed: {prompt}"
