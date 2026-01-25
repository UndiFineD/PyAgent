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
Test Phase85 module.
"""

import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.classes.specialized.TechDebtAgent import TechDebtAgent

class TestTechDebt(unittest.TestCase):
    def setUp(self):
        self.agent = TechDebtAgent(os.getcwd())
        self.test_file = "test_debt.py"
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("def no_docstring():\n    pass\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_analyze_file(self) -> None:
        report = self.agent.analyze_file(self.test_file)
        self.assertEqual(report['file'], self.test_file)
        self.assertTrue(any(i['type'] == 'Missing Docstring' for i in report['issues']))

    def test_analyze_workspace(self) -> None:
        result = self.agent.analyze_workspace()
        self.assertTrue(result['total_issues'] > 0)
        self.assertTrue(len(result['hotspots']) > 0)

if __name__ == "__main__":
    unittest.main()