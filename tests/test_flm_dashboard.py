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
"""Tests for GET /api/metrics/flm endpoint.

prj0000060 — flm-token-throughput-dashboard.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app import app

_CLIENT = TestClient(app)


def test_flm_metrics_endpoint_returns_200() -> None:
    """GET /api/metrics/flm must return HTTP 200."""
    response = _CLIENT.get("/api/metrics/flm")
    assert response.status_code == 200


def test_flm_response_has_samples_key() -> None:
    """Response JSON must contain a 'samples' key."""
    response = _CLIENT.get("/api/metrics/flm")
    data = response.json()
    assert "samples" in data


def test_flm_samples_count_is_10() -> None:
    """The 'samples' list must have exactly 10 entries."""
    response = _CLIENT.get("/api/metrics/flm")
    data = response.json()
    assert len(data["samples"]) == 10


def test_flm_sample_has_required_fields() -> None:
    """Each sample must contain timestamp, tokens_per_second, model, queue_depth."""
    response = _CLIENT.get("/api/metrics/flm")
    data = response.json()
    sample = data["samples"][0]
    assert "timestamp" in sample
    assert "tokens_per_second" in sample
    assert "model" in sample
    assert "queue_depth" in sample


def test_flm_avg_tokens_is_numeric() -> None:
    """avg_tokens_per_second must be a numeric value (float or int)."""
    response = _CLIENT.get("/api/metrics/flm")
    data = response.json()
    avg = data["avg_tokens_per_second"]
    assert isinstance(avg, (int, float))
