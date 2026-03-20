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
"""TDD test that the main CI workflow exists and contains the expected jobs."""

import yaml


def test_ci_yaml_has_test_job() -> None:
    """ci.yml must define a 'test' job that runs the test suite."""
    with open(".github/workflows/ci.yml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    jobs = cfg.get("jobs", {})
    assert "test" in jobs, "'test' job missing from ci.yml"


def test_ci_yaml_test_job_has_install_step() -> None:
    """The test job should include a dependency installation step."""
    with open(".github/workflows/ci.yml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    steps = cfg["jobs"]["test"].get("steps", [])
    step_text = " ".join([step.get("run", "") for step in steps]).lower()
    assert "pip install" in step_text, "No install step found in ci.yml test job"


def test_ci_yaml_triggers_on_push_and_pr() -> None:
    """ci.yml must trigger on push and pull_request events."""
    with open(".github/workflows/ci.yml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    on_events = cfg.get("on", cfg.get(True, {}))
    assert "push" in on_events, "ci.yml missing 'push' trigger"
    assert "pull_request" in on_events, "ci.yml missing 'pull_request' trigger"
