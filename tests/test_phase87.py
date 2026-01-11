import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classes.specialized.CodeQualityAgent import CodeQualityAgent

class TestCodeQuality(unittest.TestCase):
    def setUp(self):
        self.agent = CodeQualityAgent(os.getcwd())
        self.py_file = "test_quality.py"
        with open(self.py_file, "w") as f:
            f.write("# " + "A" * 150 + "\n") # Line too long

    def tearDown(self):
        if os.path.exists(self.py_file):
            os.remove(self.py_file)

    def test_python_quality(self) -> None:
        report = self.agent.analyze_file_quality(self.py_file)
        self.assertEqual(report['file'], self.py_file)
        self.assertTrue(any("too long" in i['message'] for i in report['issues']))
        self.assertTrue(report['score'] < 100)

    def test_rust_quality(self) -> None:
        report = self.agent.analyze_file_quality("main.rs")
        self.assertTrue(any("clippy" in i['message'].lower() or "Suggestion" in i['type'] for i in report['issues']))

    def test_aggregate_score(self) -> None:
        self.agent.analyze_file_quality(self.py_file)
        score = self.agent.get_aggregate_score()
        self.assertTrue(score < 100)

if __name__ == "__main__":
    unittest.main()
