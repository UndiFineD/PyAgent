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

"""
CsvAgent - CSV data analysis and manipulation

Brief Summary
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Instantiate with the path to a CSV and use the DataIntelligenceAgent API to load, inspect, analyze and transform CSV datasets:
from src.agents.csv_agent import CsvAgent
agent = CsvAgent(r"C:\path\to\data.csv")
# then call the DataIntelligenceAgent surface (load, summarize, transform, export) as available in the core

WHAT IT DOES:
Provides a lightweight CSV-specialized agent by subclassing DataIntelligenceAgent and setting a CSV-focused system prompt; intended as the entrypoint for CSV-specific analysis and manipulation within the DataIntelligence core.

WHAT IT SHOULD DO BETTER:
- Implement CSV-specific features: encoding detection, delimiter/quote autodetection, type/schema inference, and robust handling of large files via chunked/streaming processing.
- Expose explicit CSV helper methods (load_preview, infer_schema, validate, sample_rows, export_compressed) rather than relying solely on generic core behavior.
- Improve error handling, input validation, and add comprehensive unit tests and usage examples in docs.

FILE CONTENT SUMMARY:
Csv agent.py module.
"""

from .data_intelligence_agent import DataIntelligenceAgent


class CsvAgent(DataIntelligenceAgent):  # pylint: disable=too-many-ancestors
    """Agent specialized in CSV data analysis and manipulation."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = "You are the CsvAgent (via DataIntelligence core)."
"""

from .data_intelligence_agent import DataIntelligenceAgent


class CsvAgent(DataIntelligenceAgent):  # pylint: disable=too-many-ancestors
    """Agent specialized in CSV data analysis and manipulation."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = "You are the CsvAgent (via DataIntelligence core)."
