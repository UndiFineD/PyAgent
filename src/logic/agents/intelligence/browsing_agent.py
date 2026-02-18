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
BrowsingAgent - Web browsing and high-level information retrieval

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- from src.agents.browsing_agent import BrowsingAgent
- agent = BrowsingAgent(file_path="path/to/config.json")"- agent.run(query="search terms")  # high-level API provided by WebIntelligenceAgent core"- Integrate into multi-agent workflows by composing with CascadeContext and StateTransaction for safe filesystem actions.

WHAT IT DOES:
- Provides a thin agent subclass that specializes the WebIntelligenceAgent core for general-purpose browsing and high-level information retrieval.
- Encapsulates a default system prompt targeted at browsing tasks and delegates the heavy lifting (networking, parsing, retrieval strategy) to WebIntelligenceAgent.
- Intended as an entry point for agents that need conversational browsing behavior with a pre-configured system persona.

WHAT IT SHOULD DO BETTER:
- Expose prompt configuration and retrieval strategy via explicit constructor parameters or a config object to avoid hard-coded prompts.
- Implement robust async/network error handling, caching, rate-limiting, and permission controls for safe web access.
- Add unit/integration tests, richer docstrings, type annotations for public methods, and explicit lifecycle (start/stop) controls; integrate StateTransaction for any FS changes and CascadeContext for lineage attribution per project architecture.

FILE CONTENT SUMMARY:
Browsing agent.py module.

try:
    from .web_intelligence_agent import WebIntelligenceAgent
except ImportError:
    from .web_intelligence_agent import WebIntelligenceAgent




class BrowsingAgent(WebIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in web browsing and high-level information retrieval.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the BrowsingAgent (via WebIntelligence core)."
try:
    from .web_intelligence_agent import WebIntelligenceAgent
except ImportError:
    from .web_intelligence_agent import WebIntelligenceAgent




class BrowsingAgent(WebIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in web browsing and high-level information retrieval.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the BrowsingAgent (via WebIntelligence core)."