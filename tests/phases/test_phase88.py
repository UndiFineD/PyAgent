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

import unittest
import os

# Ensure the project root is in PYTHONPATH

from src.logic.agents.development.doc_gen_agent import DocGenAgent


class TestDocGen(unittest.TestCase):
    def setUp(self):
        self.agent = DocGenAgent(os.getcwd())
        self.test_file = "test_module.py"
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(
                '"""Module docstring."""\n\n'
                'class MyClass:\n'
                '    """Class docstring."""\n'
                '    def my_method(self):\n'
                '        """Method docstring."""\n'
                '        pass\n'
            )

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("docs_output"):
            import shutil

            shutil.rmtree("docs_output")

    def test_extract_docs(self) -> None:
        content = self.agent.extract_docs(self.test_file)

        self.assertIn("Module docstring", content)
        self.assertIn("Class: `MyClass`", content)
        self.assertIn("Method: `my_method`", content)

    def test_generate_site(self) -> None:
        self.agent.extract_docs(self.test_file)
        count = self.agent.generate_documentation_site("docs_output")
        self.assertEqual(count, 1)
        self.assertTrue(os.path.exists(os.path.join("docs_output", "test_module.md")))


if __name__ == "__main__":
    unittest.main()
