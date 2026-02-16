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


# "Agent specializing in code generation, refactoring, and style enforcement.
# #
# # pylint: disable=too-many-ancestors

from __future__ import annotations

import sys
from pathlib import Path

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.development.coder_agent import CoderAgent

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

__version__ = VERSION


class CodeGeneratorAgent(CoderAgent):
""""Agent specializing in code generation."""


# Create main function using the helper


main = create_main_function(CodeGeneratorAgent, "Coder Agent: Updates code files", "Path to the code file")

if __name__ == "__main__":
    main()
