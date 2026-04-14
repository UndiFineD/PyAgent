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
"""Tests for pipeline execution endpoints.

prj0000062 — live-agent-execution-in-codebuilder
"""

from __future__ import annotations

from fastapi.testclient import TestClient

import backend.auth as _auth
from backend.app import app

# Force dev mode so no auth headers are needed in tests.
_auth.DEV_MODE = True

client = TestClient(app)

PIPELINE_STAGES = [
    "0master",
    "1project",
    "2think",
    "3design",
    "4plan",
    "5test",
    "6code",
    "7exec",
    "8ql",
    "9git",
]


def test_pipeline_run_endpoint_returns_pipeline_id():
    response = client.post("/api/pipeline/run", json={"task": "test task"})
    assert response.status_code == 200
    data = response.json()
    assert "pipeline_id" in data
    assert data["status"] == "running"


def test_pipeline_status_endpoint_returns_pipeline_data():
    run_response = client.post("/api/pipeline/run", json={"task": "test pipeline"})
    assert run_response.status_code == 200
    pipeline_id = run_response.json()["pipeline_id"]

    status_response = client.get(f"/api/pipeline/status/{pipeline_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["id"] == pipeline_id
    assert data["status"] == "running"
    assert data["task"] == "test pipeline"


def test_pipeline_status_404_for_unknown_id():
    response = client.get("/api/pipeline/status/does-not-exist-at-all")
    assert response.status_code == 404


def test_pipeline_has_10_stages():
    run_response = client.post("/api/pipeline/run", json={"task": "check stages"})
    assert run_response.status_code == 200
    pipeline_id = run_response.json()["pipeline_id"]

    status_response = client.get(f"/api/pipeline/status/{pipeline_id}")
    assert status_response.status_code == 200
    stages = status_response.json()["stages"]
    assert len(stages) == 10
    for stage in PIPELINE_STAGES:
        assert stage in stages, f"Expected stage {stage!r} not found in pipeline stages"


def test_pipeline_stages_have_status_and_log_fields():
    run_response = client.post("/api/pipeline/run", json={"task": "check fields"})
    assert run_response.status_code == 200
    pipeline_id = run_response.json()["pipeline_id"]

    status_response = client.get(f"/api/pipeline/status/{pipeline_id}")
    assert status_response.status_code == 200
    stages = status_response.json()["stages"]
    for stage_name, stage_data in stages.items():
        assert "status" in stage_data, f"Stage {stage_name!r} missing 'status' field"
        assert "log" in stage_data, f"Stage {stage_name!r} missing 'log' field"
        assert stage_data["status"] == "pending"
        assert stage_data["log"] == ""
