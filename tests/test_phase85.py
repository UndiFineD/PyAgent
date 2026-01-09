import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classes.specialized.TechDebtAgent import TechDebtAgent

class TestTechDebt(unittest.TestCase):
    def setUp(self):
        self.agent = TechDebtAgent(os.getcwd())
        self.test_file = "test_debt.py"
        with open(self.test_file, "w") as f:
            f.write("def no_docstring():\n    pass\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_analyze_file(self):
        report = self.agent.analyze_file(self.test_file)
        self.assertEqual(report['file'], self.test_file)
        self.assertTrue(any(i['type'] == 'Missing Docstring' for i in report['issues']))

    def test_analyze_workspace(self):
        result = self.agent.analyze_workspace()
        self.assertTrue(result['total_issues'] > 0)
        self.assertTrue(len(result['hotspots']) > 0)

if __name__ == "__main__":
    unittest.main()
