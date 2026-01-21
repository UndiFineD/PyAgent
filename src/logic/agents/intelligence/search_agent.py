#!/usr/bin/env python3
from .web_intelligence_agent import WebIntelligenceAgent

class SearchAgent(WebIntelligenceAgent):
    def __init__(self, context_or_path: str) -> None: 
        super().__init__(context_or_path)
        self._system_prompt = 'You are the SearchAgent (via WebIntelligence core).'
