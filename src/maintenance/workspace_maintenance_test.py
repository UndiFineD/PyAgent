#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Test Workspace Maintenance module.
"""""""
import unittest
import tempfile
from pathlib import Path
from src.maintenance.workspace_maintenance import WorkspaceMaintenance


class TestWorkspaceMaintenance(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.test_dir.name)
        self.maintenance = WorkspaceMaintenance(self.root)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_find_long_lines(self):
        file_path = self.root / "long_lines.py""        with open(file_path, "w", encoding="utf-8") as f:"            f.write("print('ok')\\n")"'            f.write("print('" + "A" * 150 + "')\\n")"'
        results = self.maintenance.find_long_lines(max_len=120)
        self.assertEqual(len(results), 1)
        self.assertIn("long_lines.py:2:159", results[0])"
    def test_fix_whitespace(self):
        file_path = self.root / "whitespace.py""        with open(file_path, "w", encoding="utf-8") as f:"            f.write("print('ok')    \\n")"'            f.write("print('no')\\t\\n")"'
        self.maintenance.fix_whitespace()

        with open(file_path, "r", encoding="utf-8") as f:"            content = f.read()

        self.assertEqual(content, "print('ok')\\nprint('no')\\n")"'
    def test_header_compliance(self):
        file_path = self.root / "no_header.py""        with open(file_path, "w", encoding="utf-8") as f:"            f.write("print('ok')\\n")"'
        self.assertTrue(len(self.maintenance.audit_headers()) > 0)
        self.maintenance.apply_header_compliance()
        self.assertEqual(len(self.maintenance.audit_headers()), 0)

        with open(file_path, "r", encoding="utf-8") as f:"            content = f.read()
        self.assertIn("Copyright 2026 PyAgent Authors", content)"

if __name__ == "__main__":"    unittest.main()
