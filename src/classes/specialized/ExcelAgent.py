#!/usr/bin/env python3

"""Agent specializing in structured extraction from Excel files (ExStruct pattern)."""

from src.classes.base_agent import BaseAgent
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class ExcelAgent(BaseAgent):
    """Parses Excel workbooks into structured JSON (tables, shapes, charts)."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Excel Specialist Agent. "
            "Your role is to extract structured data from Excel workbooks. "
            "Beyond raw cell values, you identify tables, charts, and diagrams (shapes) "
            "to provide a semantic understanding of the spreadsheet."
        )

    def extract_structured_data(self, excel_path: str, mode: str = "standard") -> Dict[str, Any]:
        """Simulates the ExStruct extraction process."""
        logging.info(f"ExcelAgent: Extracting data from {excel_path} in '{mode}' mode.")
        
        # Placeholder for real exstruct.extract() call
        return {
            "book_name": Path(excel_path).name,
            "sheets": {
                "Sheet1": {
                    "table_candidates": ["A1:D10"],
                    "charts": [{"type": "Line", "title": "Sales Projection"}],
                    "shapes": [{"text": "Start", "type": "FlowchartProcess"}],
                    "rows_summary": "10 rows, 4 columns identified as a primary table."
                }
            }
        }

    def generate_markdown_summary(self, extraction_result: Dict[str, Any]) -> str:
        """Converts structured Excel JSON into an AI-readable Markdown summary."""
        summary = [f"# Excel Summary: {extraction_result.get('book_name')}"]
        
        for sheet_name, data in extraction_result.get("sheets", {}).items():
            summary.append(f"## Sheet: {sheet_name}")
            summary.append(f"- **Primary Table**: {', '.join(data.get('table_candidates', []))}")
            if data.get("charts"):
                summary.append(f"- **Charts**: {len(data['charts'])} detected (Types: {', '.join(c['type'] for c in data['charts'])})")
            if data.get("shapes"):
                summary.append(f"- **Diagram Elements**: {len(data['shapes'])} shapes found.")
                
        return "\n".join(summary)

    def improve_content(self, task: str) -> str:
        """Handles Excel-related tasks."""
        if "extract" in task.lower() or ".xlsx" in task.lower():
            # In real use, we'd grab the file path from the context
            res = self.extract_structured_data("sample.xlsx")
            return self.generate_markdown_summary(res)
        return "ExcelAgent: Ready to parse spreadsheets."

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(ExcelAgent)
    main()
