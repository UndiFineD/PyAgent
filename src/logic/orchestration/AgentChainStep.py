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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from dataclasses import dataclass
from typing import Any
from collections.abc import Callable

__version__ = VERSION


@dataclass
class AgentChainStep:
    """A step in an agent chain.

    Attributes:
        agent_name: Name of the agent to execute.
        input_transform: Optional function to transform input.
        output_transform: Optional function to transform output.
        enabled: Whether this step is enabled.
        condition: Optional condition function to check before execution.
    """

    agent_name: str
    input_transform: Callable[[Any], Any] | None = None
    output_transform: Callable[[Any], Any] | None = None
    enabled: bool = True
    condition: Callable[[Any], bool] | None = None
