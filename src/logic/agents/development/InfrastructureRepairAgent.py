#!/usr/bin/env python3

"""Agent for automated infrastructure and environment repair.
Detects and fixes environment issues like missing dependencies or broken paths.
"""

import subprocess
import logging
import sys
from src.core.base.BaseAgent import BaseAgent

class InfrastructureRepairAgent(BaseAgent):
    """Monitors and repairs the agent's execution environment."""

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.name = "InfrastructureRepair"

    def audit_environment(self) -> dict:
        """Checks for common environment issues."""
        issues = []
        
        # Check for common packages
        try:
            import pandas
        except ImportError:
            issues.append({"type": "missing_package", "package": "pandas"})
            
        try:
            import yaml
        except ImportError:
            issues.append({"type": "missing_package", "package": "pyyaml"})

        return {"status": "clean" if not issues else "degraded", "issues": issues}

    def repair_issue(self, issue: dict) -> str:
        """Attempts to fix a detected environment issue."""
        if issue["type"] == "missing_package":
            package = issue["package"]
            logging.info(f"Environment: Attempting to install {package}...")
            cmd_str = f"pip install {package}"
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                self._record(cmd_str, "Success", provider="Shell", model="pip")
                return f"Successfully installed {package}."
            except Exception as e:
                self._record(cmd_str, f"Failed: {str(e)}", provider="Shell", model="pip")
                return f"Failed to install {package}: {e}"
        
        return "Unknown issue type."

    def auto_repair(self) -> str:
        """Runs audit and attempts to fix all issues found."""
        report = self.audit_environment()
        if report["status"] == "clean":
            return "Environment is healthy."
            
        results = []
        for issue in report["issues"]:
            res = self.repair_issue(issue)
            results.append(res)
            
        return "\n".join(results)
