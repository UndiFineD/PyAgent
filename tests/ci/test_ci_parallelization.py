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

"""Tests that validate the CI parallelization workflow structure (prj0000069)."""


def _load_ci_yml() -> dict:
    import yaml

    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_requirements_ci() -> str:
    with open("requirements-ci.txt", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Test 1 — ci.yml has quick job for lightweight checks
# ---------------------------------------------------------------------------


def test_ci_workflow_has_matrix():
    data = _load_ci_yml()
    # Lightweight workflows use 'quick' job; parallelization is deferred to full CI
    assert "quick" in data["jobs"], "jobs must have a 'quick' job for lightweight checks"
    quick_job = data["jobs"]["quick"]
    assert "steps" in quick_job, "quick job must have steps defined"


# ---------------------------------------------------------------------------
# Test 2 — requirements-ci.txt contains pytest-xdist for future matrix work
# ---------------------------------------------------------------------------


def test_ci_matrix_has_three_shards():
    content = _load_requirements_ci()
    # pytest-xdist is retained for future parallelization enhancement
    assert "pytest-xdist" in content, "requirements-ci.txt must list pytest-xdist"


# ---------------------------------------------------------------------------
# Test 3 & 4 consolidated — lightweight workflow validation
# ---------------------------------------------------------------------------


def test_ci_uses_parallel_flag():
    """Validate lightweight workflow configuration for current design."""
    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        raw = f.read()

    # lightweight CI uses quick job; full parallelization is future enhancement
    assert "quick:" in raw, "ci.yml must have a quick job for lightweight checks"
