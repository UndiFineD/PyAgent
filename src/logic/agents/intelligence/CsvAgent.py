#!/usr/bin/env python3

"""Agent specializing in CSV and tabular data processing."""

from src.core.base.version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function
import logging

__version__ = VERSION

class CsvAgent(BaseAgent):
    """Agent for CSV data cleaning, analysis, and transformation."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are a Data Analyst and CSV Expert. "
            "Focus on tabular data integrity, cleaning, and transformation. "
            "Identify missing values, deal with encoding issues, and suggest "
            "optimal structures for data interoperability (e.g., preparing for SQL import)."
        )

    def _get_default_content(self) -> str:
        return "header1,header2\nvalue1,value2\n"

if __name__ == "__main__":
    main = create_main_function(CsvAgent, "CSV Agent", "Path to CSV file (.csv)")
    main()
