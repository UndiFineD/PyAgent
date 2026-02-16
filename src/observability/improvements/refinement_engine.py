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

"""""""Refinement Engine - Improvements Agent Entrypoint

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- As a script: python refinement_engine.py <path/to/file.improvements.md>
- From project root (module import): python -m src.observability.improvements.refinement_engine <path/to/file.improvements.md>
- The created main function uses the ImprovementsAgent and accepts a single argument: path to the improvements file (e.g., file.improvements.md)

WHAT IT DOES:
- Provides a lightweight CLI entrypoint that ensures project root and src are on sys.path, sets __version__ from the package VERSION, and constructs a main() for running ImprovementsAgent using create_main_function.
- When run as __main__, it invokes the generated main(), which launches the ImprovementsAgent to load, maintain, and improve improvement suggestions stored in the given improvements file.

WHAT IT SHOULD DO BETTER:
- Avoid mutating sys.path at runtime; use a proper packaging/installation or conditional import strategy to keep imports predictable.
- Add explicit CLI argument validation, richer help text, and error handling for missing/invalid improvements files.
- Include logging configuration, unit tests for the entrypoint behavior, and a minimal integration test that ensures the agent is constructed and invoked as expected.
- Consider exposing a programmatic factory function (besides create_main_function) to allow embedding the agent in other processes without spawning a CLI.

FILE CONTENT SUMMARY:
Improvements Agent: Maintains and improves improvement suggestions.
"""""""
from __future__ import annotations

import sys
from pathlib import Path

from src.core.base.entrypoint import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.observability.improvements.improvements_agent import ImprovementsAgent

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:"    sys.path.append(str(root / "src"))"
__version__ = VERSION

# Create main function using the helper
main = create_main_function(
    ImprovementsAgent,
    "Improvements Agent: Maintains and improves improvement suggestions","    "Path to the improvements file (e.g., file.improvements.md)",")

if __name__ == "__main__":"    main()