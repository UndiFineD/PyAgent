# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_owl.py\owl.py\camel.py\agents.py\base_b2217d6adef2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-owl\owl\camel\agents\base.py

# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

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

# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

from abc import ABC, abstractmethod

from typing import Any


class BaseAgent(ABC):
    r"""An abstract base class for all CAMEL agents."""

    @abstractmethod
    def reset(self, *args: Any, **kwargs: Any) -> Any:
        r"""Resets the agent to its initial state."""

        pass

    @abstractmethod
    def step(self, *args: Any, **kwargs: Any) -> Any:
        r"""Performs a single step of the agent."""

        pass
