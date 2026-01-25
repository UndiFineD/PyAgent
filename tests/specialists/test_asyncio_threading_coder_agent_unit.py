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
Test Asyncio Threading Coder Agent Unit module.
"""

import unittest
from src.logic.agents.specialized.asyncio_threading_coder_agent import (
    AsyncioThreadingCoderAgent,
)
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TestAsyncioThreadingCoderAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = AsyncioThreadingCoderAgent("dummy_path.py")

    def test_initialization(self) -> None:
        self.assertIsNotNone(self.agent)
        self.assertIn("AsyncioThreadingCoderAgent", self.agent.__class__.__name__)


if __name__ == "__main__":
    unittest.main()