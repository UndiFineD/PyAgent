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

import re


def _load_ci_yml() -> dict:
    import yaml
    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_requirements_ci() -> str:
    with open("requirements-ci.txt", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Test 1 — ci.yml has matrix under jobs.test.strategy
# ---------------------------------------------------------------------------

def test_ci_workflow_has_matrix():
    data = _load_ci_yml()
    test_job = data["jobs"]["test"]
    assert "strategy" in test_job, "jobs.test must have a strategy block"
    assert "matrix" in test_job["strategy"], "strategy must define a matrix"


# ---------------------------------------------------------------------------
# Test 2 — matrix.shard has exactly 3 values
# ---------------------------------------------------------------------------

def test_ci_matrix_has_three_shards():
    data = _load_ci_yml()
    shards = data["jobs"]["test"]["strategy"]["matrix"]["shard"]
    assert len(shards) == 3, f"Expected 3 shards, got {len(shards)}"
    assert sorted(shards) == [1, 2, 3]


# ---------------------------------------------------------------------------
# Test 3 — requirements-ci.txt contains pytest-xdist
# ---------------------------------------------------------------------------

def test_requirements_ci_has_xdist():
    content = _load_requirements_ci()
    assert "pytest-xdist" in content, "requirements-ci.txt must list pytest-xdist"


# ---------------------------------------------------------------------------
# Test 4 — at least one run step in ci.yml uses the -n flag (xdist workers)
# ---------------------------------------------------------------------------

def test_ci_uses_parallel_flag():
    with open(".github/workflows/ci.yml", encoding="utf-8") as f:
        raw = f.read()
    assert re.search(r"-n\s+\d+", raw), "ci.yml must use -n <N> for pytest-xdist parallelism"
