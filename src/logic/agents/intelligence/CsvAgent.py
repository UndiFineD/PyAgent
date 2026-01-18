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


"""Agent specializing in CSV and tabular data processing."""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import create_main_function

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
