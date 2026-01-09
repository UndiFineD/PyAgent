#!/usr/bin/env python3

"""Agent specializing in autonomous web navigation and information extraction."""

import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool
from src.classes.coder.SecurityGuardAgent import SecurityGuardAgent

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

    @as_tool
    def fetch_page_content(self, url: str) -> str:
        """Fetches and simplifies content from a URL with safety scanning."""
        logging.info(f"WebAgent fetching URL: {url}")
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Safety Scan
            injections = self.security_guard.scan_for_injection(text)
            if injections:
                logging.warning(f"WebAgent blocked content from {url} due to safety risks: {injections}")
                return f"ERROR: Content from {url} was blocked for safety reasons: {', '.join(injections)}"
            
            return text[:5000] # Limit to avoid context overflow
        except Exception as e:
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
