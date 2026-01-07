#!/usr/bin/env python3

"""Agent specializing in financial analysis and advice."""

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function
import logging

class FinancialAgent(BaseAgent):
    """Agent for financial data analysis and advisory reports."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are a Senior Financial Advisor and Quantitative Analyst. "
            "Analyze financial data, market trends, and investment strategies. "
            "Provide evidence-based reports focusing on risk assessment, yield optimization, "
            "and long-term financial health. Note: You should specify that your reports "
            "are for informational purposes and not legal financial advice."
        )

    def _get_default_content(self) -> str:
        return "# Financial Analysis Report\n\n## Overview\nPending analysis...\n"

if __name__ == "__main__":
    main = create_main_function(FinancialAgent, "Financial Agent", "File containing financial data or topic")
    main()
