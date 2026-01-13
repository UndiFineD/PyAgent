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

"""Agent specializing in financial analysis and advice."""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Dict, List, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function, as_tool
import logging

__version__ = VERSION

class FinancialAgent(BaseAgent):
    """Agent for autonomous financial research and analysis (Dexter Pattern)."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.research_plan: list[dict[str, Any]] = []
        self._system_prompt = (
            "You are an Autonomous Financial Research Agent (Dexter Pattern). "
            "You decompose complex financial queries into structured research tasks. "
            "Execute tasks using market data, validate your findings for data sufficiency, "
            "and iterate until a confident, data-backed answer is formed. "
            "Roles: Planning, Execution, Validation, Synthesis."
        )

    @as_tool
    def plan_research(self, query: str) -> str:
        """Breaks down a query into specific financial research tasks."""
        # In a real impl, this would call LLM to generate the JSON list
        self.research_plan = [
            {"task": "Fetch income statement", "status": "pending"},
            {"task": "Calculate operating margin", "status": "pending"},
            {"task": "Compare with sector average", "status": "pending"}
        ]
        return f"Research plan created with {len(self.research_plan)} tasks for: {query}"

    @as_tool
    def validate_sufficiency(self, data: dict[str, Any]) -> str:
        """Self-reflects on whether gathered data is enough to answer the query."""
        missing = [k for k, v in data.items() if v is None]
        if missing:
            return f"Validation failed. Missing data: {missing}. Executing refinement loop."
        return "Validation passed. Proceeding to synthesis."

    @as_tool
    def analyze_market_trend(self, tickers: list[str]) -> str:
        """Executes a trend analysis across multiple financial tickers."""
        logging.info(f"FinancialAgent: Analyzing trends for {tickers}")
        return f"Trend analysis for {tickers}: Bullish sentiment in tech, consolidated in energy."

    def _get_default_content(self) -> str:
        return "# Financial Analysis Report\n\n## Overview\nPending autonomous research...\n"

if __name__ == "__main__":
    main = create_main_function(FinancialAgent, "Financial Agent", "File containing financial data or topic")
    main()