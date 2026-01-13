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

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .TestDataType import TestDataType
from dataclasses import dataclass
from typing import Optional

__version__ = VERSION

@dataclass
class TestDataFactory:
    __test__ = False
    """Factory for generating test data.

    Attributes:
        data_type: Type of data to generate.
        template: Template for generation.
        variations: Number of variations to create.
        seed: Random seed for reproducibility.
    """

    data_type: TestDataType
    template: str = ""
    variations: int = 1
    seed: int | None = None