import os
import subprocess
import json
from typing import Dict, List, Any
from src.classes.base_agent import BaseAgent

class CodeQualityAgent(BaseAgent):
    """
    Automated Code Quality Guard: Performs linting, formatting checks, 
    and complexity analysis for Python, Rust, and JavaScript.
    """
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.quality_reports = []

    def analyze_file_quality(self, file_path: str) -> Dict[str, Any]:
        """Analyzes code quality for a specific file based on its extension."""
        print(f"Code Quality: Analyzing {file_path}")
        
        issues = []
        if file_path.endswith('.py'):
            issues = self._check_python_quality(file_path)
        elif file_path.endswith('.rs'):
            issues = self._check_rust_quality(file_path)
        elif file_path.endswith(('.js', '.ts')):
            issues = self._check_js_quality(file_path)
        else:
            issues.append({"type": "Warning", "message": "Unsupported file type for quality analysis."})

        report = {
            "file": file_path,
            "timestamp": os.path.getmtime(file_path) if os.path.exists(file_path) else 0,
            "issues": issues,
            "score": max(0, 100 - (len(issues) * 5))
        }
        self.quality_reports.append(report)
        return report

    def _check_python_quality(self, path: str) -> List[Dict[str, Any]]:
        """Mock Python quality check (simulating flake8/pylint)."""
        issues = []
        # Simulation: check for long lines
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if len(line) > 120:
                        issues.append({"line": i, "type": "Style", "message": "Line too long (>120 chars)"})
        except Exception as e:
            issues.append({"type": "Error", "message": str(e)})
        return issues

    def _check_rust_quality(self, path: str) -> List[Dict[str, Any]]:
        """Mock Rust quality check (simulating cargo clippy)."""
        # For simulation, return a placeholder
        return [{"type": "Suggestion", "message": "Consider using 'if let' instead of 'match' for single pattern."}]

    def _check_js_quality(self, path: str) -> List[Dict[str, Any]]:
        """Mock JS quality check (simulating eslint)."""
        return [{"type": "Insecure", "message": "Avoid using 'var', use 'let' or 'const' instead."}]

    def get_aggregate_score(self) -> float:
        """Returns the average quality score across all analyzed files."""
        if not self.quality_reports:
            return 100.0
        return sum(r['score'] for r in self.quality_reports) / len(self.quality_reports)
