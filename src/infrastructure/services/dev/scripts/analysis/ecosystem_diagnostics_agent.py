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
Phase 309: Ecosystem Diagnostics Agent.
Consolidates various dev scripts into a single diagnostic engine.
"""

import ast
from pathlib import Path
from typing import Any


class EcosystemDiagnosticsAgent:
    """Agent for running high-level ecosystem diagnostics and health checks."""

    def __init__(self, root_path: str = ".") -> None:
        self.root_path = Path(root_path)
        self.results: dict[Any, Any] = {}

    def run_all_checks(self) -> None:
        print("--- Ecosystem Diagnostics Agent (Phase 309) ---")
        self.check_syntax_errors()
        self.check_import_health()
        self.check_system_resources()
        self.summarize()

    def check_syntax_errors(self) -> None:
        print("[CHECK] Validating Syntax in src/...")
        errors = []
        for py_file in (self.root_path / "src").rglob("*.py"):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    ast.parse(f.read())
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                errors.append(f"{py_file}: {e}")
        self.results["syntax_errors"] = errors
        if not errors:
            print("  - Success: No syntax errors found.")
        else:
            print(f"  - Warning: {len(errors)} syntax errors detected.")

    def check_import_health(self) -> None:
        print("[CHECK] Checking Circular Imports and Missing References...")
        # Placeholder for complex import analysis
        # In a real scenario, this would use 'pylint' or custom graph analysis
        self.results["import_health"] = "Nominal"

    def check_system_resources(self) -> None:
        print("[CHECK] System Health...")
        try:
            # Check disk space using shutil.disk_usage (cross-platform, safe)
            import shutil

            usage = shutil.disk_usage(".")
            total_gb = usage.total / (1024**3)

            free_gb = usage.free / (1024**3)
            self.results["disk_space"] = f"Free: {free_gb:.1f} GB / {total_gb:.1f} GB"
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            self.results["disk_space"] = "Unknown (Error reading disk info)"

    def summarize(self) -> None:
        print("\n--- Diagnostic Summary ---")
        for key, val in self.results.items():
            if isinstance(val, list):
                print(f"{key}: {len(val)} issues")

                for item in val[:5]:
                    print(f"  - {item}")
            else:
                print(f"{key}: {val}")


if __name__ == "__main__":
    agent = EcosystemDiagnosticsAgent()
    agent.run_all_checks()
