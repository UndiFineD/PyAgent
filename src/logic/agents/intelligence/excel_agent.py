#!/usr/bin/env python3
from .data_intelligence_agent import DataIntelligenceAgent

class ExcelAgent(DataIntelligenceAgent):
    def __init__(self, file_path: str) -> None: 
        super().__init__(file_path)
        self._system_prompt = 'You are the ExcelAgent (via DataIntelligence core).'
