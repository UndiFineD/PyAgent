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


"""
Context Agent: Maintains and improves context/description files.
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION
from src.core.base.common.base_utilities import create_main_function
from src.logic.agents.cognitive.context_agent import ContextAgent

__version__ = VERSION

# Create main function using the helper
main = create_main_function(
    ContextAgent,
    "Context Agent: Maintains and improves context/description files",
    "Path to the context file (e.g., file.description.md)",
)

if __name__ == "__main__":
    main()
