import unittest
from unittest.mock import patch
import json
import os

# Ensure the project root is in PYTHONPATH

from src.logic.agents.analysis.code_quality_agent import CodeQualityAgent


class TestCodeQuality(unittest.TestCase):
    def setUp(self):
        self.agent = CodeQualityAgent(os.getcwd())
        self.py_file = "test_quality.py"
        with open(self.py_file, "w") as f:
            f.write("# " + "A" * 150 + "\n")  # Line too long

        self.rs_file = "main.rs"
        with open(self.rs_file, "w") as f:
            f.write(
                "fn main() { let x = 5; }"
            )  # Unused variable should trigger warning

        self.cargo_file = "Cargo.toml"
        with open(self.cargo_file, "w") as f:
            f.write(
                '[package]\nname = "test_project"\nversion = "0.1.0"\nedition = "2021"\n\n[[bin]]\nname = "test_project"\npath = "main.rs"\n\n[dependencies]\n'
            )

    def tearDown(self):
        if os.path.exists(self.py_file):
            os.remove(self.py_file)
        if os.path.exists(self.rs_file):
            os.remove(self.rs_file)
        if os.path.exists(self.cargo_file):
            os.remove(self.cargo_file)

    def test_python_quality(self) -> None:
        report = self.agent.analyze_file_quality(self.py_file)
        self.assertEqual(report["file"], self.py_file)
        self.assertTrue(any("too long" in i["message"] for i in report["issues"]))
        self.assertTrue(report["score"] < 100)

    @patch("subprocess.run")
    def test_rust_quality(self, mock_run) -> None:
        # Mock response mimicking cargo clippy output

        clippy_msg = {
            "reason": "compiler-message",
            "message": {
                "level": "warning",
                "message": "unused variable: `x`",
                "spans": [{"line_start": 1, "column_start": 5}],
            },
        }
        mock_run.return_value.stdout = json.dumps(clippy_msg)

        mock_run.return_value.returncode = 0

        report = self.agent.analyze_file_quality("main.rs")
        self.assertTrue(
            any(
                "clippy" in i["message"].lower() or "Suggestion" in i["type"]
                for i in report["issues"]
            )
        )

    def test_aggregate_score(self) -> None:
        self.agent.analyze_file_quality(self.py_file)
        score = self.agent.get_aggregate_score()
        self.assertTrue(score < 100)


if __name__ == "__main__":
    unittest.main()
