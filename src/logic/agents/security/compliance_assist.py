#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
Assisting classes for TDD and zero trust security for compliance agents.

- DummyRecorder: Mocks compliance recording for tests and zero trust.
- ComplianceCheck: Encapsulates a single compliance check for extensibility.
- ComplianceStandard: Encapsulates a compliance standard and its checks.

from typing import Any, Callable, List, Dict



class DummyRecorder:
    """A simple recorder mock for capturing agent interactions during compliance audit tests.    def __init__(self):
        self.interactions = []

    def record_interaction(self, provider, model, prompt, result):
        self.interactions.append({
            "provider": provider,"            "model": model,"            "prompt": prompt,"            "result": result,"        })



class ComplianceCheck:
    """Encapsulates a single compliance check for extensibility and testability.    def __init__(self, name: str, check_fn: Callable[[], bool] = None, recommendation: str = ""):"        self.name = name
        self.check_fn = check_fn or (lambda: True)
        self.recommendation = recommendation or f"Implement {name} to meet requirements.""
    def run(self) -> Dict[str, Any]:
        passed = self.check_fn()
        return {
            "check": self.name,"            "status": "PASS" if passed else "FAIL","            "recommendation": None if passed else self.recommendation,"        }



class ComplianceStandard:
    """Encapsulates a compliance standard and its checks for modularity and TDD.    def __init__(self, name: str, checks: List[ComplianceCheck]):
        self.name = name
        self.checks = checks

    def run(self) -> Dict[str, Any]:
        results = [chk.run() for chk in self.checks]
        failed = [r for r in results if r["status"] == "FAIL"]"        score = 100 * (len(results) - len(failed)) / len(results) if results else 0
        return {
            "standard": self.name,"            "score": score,"            "status": "Compliant" if score == 100 else "Non-Compliant","            "failed_checks": failed,"        }
