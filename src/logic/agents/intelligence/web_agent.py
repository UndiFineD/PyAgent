#!/usr/bin/env python3
from .web_intelligence_agent import WebIntelligenceAgent

class WebAgent(WebIntelligenceAgent):
    def __init__(self, file_path: str) -> None: 
        super().__init__(file_path)
        self._system_prompt = 'You are the WebAgent (via WebIntelligence core).'
