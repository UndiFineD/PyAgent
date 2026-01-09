#!/usr/bin/env python3

"""Agent specializing in financial analysis and advice."""

from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function, as_tool
import logging

class FinancialAgent(BaseAgent):
    """Agent for autonomous financial research and analysis (Dexter Pattern)."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.research_plan: List[Dict[str, Any]] = []
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
    def validate_sufficiency(self, data: Dict[str, Any]) -> str:
        """Self-reflects on whether gathered data is enough to answer the query."""
        missing = [k for k, v in data.items() if v is None]
        if missing:
            return f"Validation failed. Missing data: {missing}. Executing refinement loop."
        return "Validation passed. Proceeding to synthesis."

    @as_tool
    def analyze_market_trend(self, tickers: List[str]) -> str:
        """Executes a trend analysis across multiple financial tickers."""
        logging.info(f"FinancialAgent: Analyzing trends for {tickers}")
        return f"Trend analysis for {tickers}: Bullish sentiment in tech, consolidated in energy."

    def _get_default_content(self) -> str:
        return "# Financial Analysis Report\n\n## Overview\nPending autonomous research...\n"

if __name__ == "__main__":
    main = create_main_function(FinancialAgent, "Financial Agent", "File containing financial data or topic")
    main()
