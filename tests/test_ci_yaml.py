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
"""TDD test that .github/workflows/quality.yml exists and contains the expected jobs."""

import yaml


def test_ci_yaml_has_python_job() -> None:
    """quality.yml must define both 'python' and 'rust' jobs."""
    with open(".github/workflows/quality.yml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    jobs = cfg.get("jobs", {})
    assert "python" in jobs, "'python' job missing from quality.yml"
    assert "rust" in jobs, "'rust' job missing from quality.yml"


def test_ci_yaml_python_job_has_steps() -> None:
    """Python job must contain at least a lint and a test step."""
    with open(".github/workflows/quality.yml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    python_steps = [
        s.get("name", "") for s in cfg["jobs"]["python"].get("steps", [])
    ]
    step_text = " ".join(python_steps).lower()
    assert "lint" in step_text or "ruff" in step_text, "No lint step found in python job"
    assert "test" in step_text or "pytest" in step_text, "No test step found in python job"


def test_ci_yaml_triggers_on_push_and_pr() -> None:
    """quality.yml must trigger on push and pull_request events."""
    with open(".github/workflows/quality.yml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    on_events = cfg.get("on", cfg.get(True, {}))
    assert "push" in on_events, "quality.yml missing 'push' trigger"
    assert "pull_request" in on_events, "quality.yml missing 'pull_request' trigger"
