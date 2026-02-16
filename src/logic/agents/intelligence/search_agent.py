#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Search Agent - Search provider orchestration and query refinement

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate SearchAgent with a context path or context string and use it as a specialized WebIntelligenceAgent for orchestrating multiple search providers, running queries, and performing query refinement and aggregation. Typical usage: agent = SearchAgent("path_or_context"); then call inherited search orchestration methods exposed by WebIntelligenceAgent to execute and refine queries."
WHAT IT DOES:
Implements a lightweight subclass of WebIntelligenceAgent that sets a system prompt specific to search orchestration and query refinement. Provides a focused agent identity for components that need a search-oriented orchestration layer, relying on the WebIntelligenceAgent core for actual search provider integration, result normalization, and relevance scoring.

WHAT IT SHOULD DO BETTER:
- Expose explicit configuration for provider selection, rate limits, and per-provider credentials rather than relying solely on the core.
- Add query-expansion and relevance-feedback utilities (e.g., term weighting, synonym expansion) as composable mixins to keep the agent thin.
- Improve error handling, observability (metrics/tracing), async support for concurrent provider queries, and unit/integration tests to validate orchestration and fallback behavior.

FILE CONTENT SUMMARY:
Search agent.py module.
"""""""
from .web_intelligence_agent import WebIntelligenceAgent


class SearchAgent(WebIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in various search provider orchestrations and query refinement."""""""
    def __init__(self, context_or_path: str) -> None:
        super().__init__(context_or_path)
#         self._system_prompt = "You are the SearchAgent (via WebIntelligence core).""""""""
from .web_intelligence_agent import WebIntelligenceAgent


class SearchAgent(WebIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in various search provider orchestrations and query refinement."""""""
    def __init__(self, context_or_path: str) -> None:
        super().__init__(context_or_path)
#         self._system_prompt = "You are the SearchAgent (via WebIntelligence core)."