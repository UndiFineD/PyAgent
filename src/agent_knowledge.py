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
agent_knowledge.py - Knowledge Agent CLI wrapper

A minimal CLI entrypoint that ensures repository root is importable 
and invokes the Knowledge Agent's main() function.
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- From repository root: python agent_knowledge.py
- As a module (preferred long-term): python -m src.logic.agents.cognitive.context.knowledge_main

WHAT IT DOES:
- Adds the project root to sys.path so relative imports resolve, imports main 
from src.logic.agents.cognitive.context.knowledge_main, and calls main() when run as __main__.

WHAT IT SHOULD DO BETTER:
- Replace sys.path manipulation with a proper package entry point (console_scripts) or installable package layout.
- Add CLI argument parsing and help forwarding to the underlying main, and add structured logging and error handling.
- Include unit tests for the wrapper and avoid side-effectful path mutation at import time.

FILE CONTENT SUMMARY:
Wrapper for Knowledge Agent CLI.
"""

import os
import sys

# Ensure the root directory is in sys.path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.logic.agents.cognitive.context.knowledge_main import main  # noqa: E402


if __name__ == "__main__":
    main()
