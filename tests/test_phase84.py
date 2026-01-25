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
Test Phase84 module.
"""

import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.classes.specialized.SecurityAuditAgent import SecurityAuditAgent

class TestSecurityAudit(unittest.TestCase):
    def setUp(self):
        self.agent = SecurityAuditAgent(os.getcwd())
        self.test_file = "test_security_audit.py"
<<<<<<< HEAD:tests/test_phase84.py
        with open(self.test_file, "w") as f:
=======

        with open(self.test_file, 'w', encoding='utf-8') as f:
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/phases/test_phase84.py
            f.write("api_key = 'sk-12345'\n")
            f.write("eval('print(1)')\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_scan_file(self) -> None:
        findings = self.agent.scan_file(self.test_file)
        self.assertTrue(any(f['type'] == 'Hardcoded Secret' for f in findings))
        self.assertTrue(any(f['type'] == 'Insecure Pattern' and 'eval' in f['detail'] for f in findings))

    def test_audit_workspace(self) -> None:
        # Full scan might take time but should return findings due to our test file
        result = self.agent.audit_workspace()
        self.assertEqual(result['status'], "Complete")
        self.assertTrue(result['findings_count'] > 0)

if __name__ == "__main__":
    unittest.main()