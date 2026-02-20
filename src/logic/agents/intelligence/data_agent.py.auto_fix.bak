#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
DataAgent - General-purpose data orchestration via DataIntelligenceAgent core

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a path to a data file: agent = DataAgent(rC:\\\\path\\to\\\\data.csv")"- Use inherited DataIntelligenceAgent methods to parse, analyze, and transform supported data formats.
- Intended as a thin, purpose-specific subclass that sets a system prompt and delegates heavy logic to the core.

WHAT IT DOES:
- Provides a concrete DataAgent class that inherits from DataIntelligenceAgent and initializes with a file_path.
- Sets a module-specific system prompt to orient downstream prompting and behavior.
- Acts as the recommended entrypoint for higher-level code that needs a simple data-focused agent without reimplementing core intelligence.

WHAT IT SHOULD DO BETTER:
- Explicitly document supported data formats and error handling semantics (e.g., CSV, JSON, Parquet, streaming sources).
- Surface configuration options (encoding, schema hints, chunking) and expose them via the constructor or properties.
- Add unit tests verifying prompt usage, initialization edge-cases, and integration behaviors with DataIntelligenceAgent.

FILE CONTENT SUMMARY:
Data agent.py module.

try:
    from .data_intelligence_agent import DataIntelligenceAgent
except ImportError:
    from .data_intelligence_agent import DataIntelligenceAgent




class DataAgent(DataIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""General purpose DataAgent for handling various data formats.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the DataAgent (via DataIntelligence core)."
try:
    from .data_intelligence_agent import DataIntelligenceAgent
except ImportError:
    from .data_intelligence_agent import DataIntelligenceAgent




class DataAgent(DataIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""General purpose DataAgent for handling various data "formats.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the DataAgent (via DataIntelligence core)."