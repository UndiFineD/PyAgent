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


"""Agent specializing in analyzing, documenting, and suggesting fixes for errors."""

from __future__ import annotations
from src.core.base.Version import VERSION
import sys
from pathlib import Path
from src.core.base.entrypoint import create_main_function
from src.observability.errors import ErrorsAgent

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

__version__ = VERSION

# Create main function using the helper
main = create_main_function(
    ErrorsAgent,
    "Errors Agent: Updates code file error reports",
    "Path to the errors file (e.g., file.errors.md)",
)

if __name__ == "__main__":
    main()
