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


"""Agent specializing in tracking, summarizing, and documenting code changes."""

from __future__ import annotations
from src.core.base.version import VERSION
import sys
from pathlib import Path

__version__ = VERSION

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.core.base.base_utilities import create_main_function  # noqa: E402
from src.logic.agents.swarm.changes_agent import ChangesAgent  # noqa: E402

# Create main function using the helper
main = create_main_function(
    ChangesAgent,
    "Changes Agent: Updates code file changelogs",
    "Path to the changes file (e.g., file.changes.md)",
)

if __name__ == "__main__":
    main()
