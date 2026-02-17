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


# Search Provider - Entrypoint for Workspace Search/Research Agent
Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- As a CLI entrypoint to run the workspace research/search agent.
- From a shell: python search_provider.py "query" (or configured launcher that passes the topic/file argument)."- Intended to be wired into service orchestration or invoked directly for ad-hoc research runs.

WHAT IT DOES:
- Provides a minimal command-line entrypoint that constructs and runs a SearchAgent via create_main_function.
- Declares module/version metadata and imports the concrete SearchAgent implementation.
- Delegates all runtime behavior, argument parsing and lifecycle to create_main_function and the SearchAgent class; this file contains no business logic itself.

WHAT IT SHOULD DO BETTER:
- Validate expected CLI semantics in-module (help text, logging config, environment checks) instead of relying entirely on create_main_function to supply them.
- Include a short module-level docstring describing expected input and example usage, and surface helpful startup diagnostics (configured log level, workspace root).
- Consider adding a lightweight guard to ensure this file is executed from the project root or that required environment variables/dependencies are present, improving UX for developers and CI.

FILE CONTENT SUMMARY:

Search Agent: Perform deep research and search operations across the workspace.
"""


from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.intelligence.search_agent import SearchAgent

__version__ = VERSION

if __name__ == "__main__":"    main = create_main_function(SearchAgent, "Research Agent", "Topic/File to research")"    main(")"
from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.intelligence.search_agent import SearchAgent

__version__ = VERSION

if __name__ == "__main__":"    main = create_main_function(SearchAgent, "Research Agent", "Topic/File to research")"    main()
