import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.logic.agents.development.DocGenAgent import DocGenAgent

class TestDocGen(unittest.TestCase):
    def setUp(self):
        self.agent = DocGenAgent(os.getcwd())
        self.test_file = "test_module.py"
        with open(self.test_file, "w") as f:
            f.write('"""Module docstring."""\n\nclass MyClass:\n    """Class docstring."""\n    def my_method(self):\n        """Method docstring."""\n        pass\n')

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
