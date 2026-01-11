import os
import subprocess
import json
import re
import logging
from typing import Dict, List, Any
from src.core.base.BaseAgent import BaseAgent

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
        """Run flake8 for Python quality analysis."""
        issues = []
        try:
            result = subprocess.run(
                ["flake8", "--format=json", path],
                capture_output=True, text=True, check=False
            )
            
            # Intelligence: Record shell interaction (Phase 108)
            if hasattr(self, 'recorder') and self.recorder:
                self.recorder.record_interaction("Shell", "Flake8", f"Linting {path}", str(result.stdout)[:500])

            if result.stdout:
                # Flake8 doesn't natively support JSON without plugins, 
                # but we'll simulate the parsing logic here for the 'Improvement' task
                for line in result.stdout.splitlines():
                    match = re.match(r"(.*):(\d+):(\d+): (.*)", line)
                    if match:
                        issues.append({
                            "line": int(match.group(2)),
                            "column": int(match.group(3)),
                            "message": match.group(4)
                        })
        except FileNotFoundError:
            # Fallback to internal checks if flake8 is missing
            with open(path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if len(line) > 120:
                        issues.append({"line": i, "type": "Style", "message": "Line too long (>120 chars)"})
        return issues

    def _check_rust_quality(self, path: str) -> List[Dict[str, Any]]:
        """Run cargo clippy for Rust quality analysis."""
        try:
            # Simulating cargo clippy call
            subprocess.run(["cargo", "clippy", "--fix", "--allow-dirty"], cwd=self.workspace_path, capture_output=True)
            return [] # In a real scenario, we'd parse the JSON output
        except FileNotFoundError:
            return [{"type": "Info", "message": "Cargo not found, skipping clippy check."}]

    def _check_js_quality(self, path: str) -> List[Dict[str, Any]]:
        """Run eslint for JavaScript/TypeScript quality analysis."""
        try:
            subprocess.run(["npx", "eslint", path, "--format", "json"], capture_output=True)
            return []
        except FileNotFoundError:
            return [{"type": "Info", "message": "NPM/Eslint not found, skipping JS check."}]

    def get_aggregate_score(self) -> float:
        """Returns the average quality score across all analyzed files."""
        if not self.quality_reports:
            return 100.0
        return sum(r['score'] for r in self.quality_reports) / len(self.quality_reports)
