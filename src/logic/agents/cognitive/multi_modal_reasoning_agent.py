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


# "Agent capable of analyzing visual inputs to complement textual code analysis.
# #
# from __future__ import annotations

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from .core.vision_core import VisionCore

__version__ = VERSION


# pylint: disable=too-many-ancestors
class MultiModalReasoningAgent(BaseAgent):
    Agent capable of analyzing visual inputs (screenshots, diagrams)
    to complement textual code analysis.
# #

    def __init__(self, file_path: str, **kwargs) -> None:
        super().__init__(file_path=file_path, **kwargs)
        self.vision_core = VisionCore()
