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

"""Tests for src/core/providers/FlmModelProbe.py."""

from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest

from src.core.providers.FlmModelProbe import (
    FlmModelProbeResult,
    _parse_models_body,
    probe_models,
    select_model,
)


# ---------------------------------------------------------------------------
# FlmModelProbeResult
# ---------------------------------------------------------------------------


def test_probe_result_reachable_when_no_error() -> None:
    result = FlmModelProbeResult(
        base_url="http://localhost",
        available_models=["m1"],
        selected_model="m1",
        latency_ms=10.0,
    )
    assert result.reachable is True


def test_probe_result_not_reachable_when_error() -> None:
    result = FlmModelProbeResult(
        base_url="http://localhost",
        available_models=[],
        selected_model=None,
        latency_ms=5000.0,
        error="timeout",
    )
    assert result.reachable is False


def test_probe_result_to_dict_keys() -> None:
    result = FlmModelProbeResult(
        base_url="http://localhost",
        available_models=["a", "b"],
        selected_model="a",
        latency_ms=12.3,
    )
    d = result.to_dict()
    assert d["base_url"] == "http://localhost"
    assert d["available_models"] == ["a", "b"]
    assert d["selected_model"] == "a"
    assert d["reachable"] is True
    assert d["error"] is None


# ---------------------------------------------------------------------------
# select_model
# ---------------------------------------------------------------------------


def test_select_model_empty_returns_none() -> None:
    assert select_model([]) is None


def test_select_model_exact_match() -> None:
    assert select_model(["llama3:8b", "phi4"], preferred="phi4") == "phi4"


def test_select_model_prefix_match() -> None:
    assert select_model(["llama3.2:1b", "phi4"], preferred="llama3") == "llama3.2:1b"


def test_select_model_substring_match() -> None:
    result = select_model(["big-llama3-v2", "phi4"], preferred="llama3")
    assert result == "big-llama3-v2"


def test_select_model_no_preferred_returns_first() -> None:
    assert select_model(["phi4", "llama3"]) == "phi4"


def test_select_model_preferred_not_found_returns_first() -> None:
    assert select_model(["phi4", "llama3"], preferred="gpt-4") == "phi4"


# ---------------------------------------------------------------------------
# _parse_models_body
# ---------------------------------------------------------------------------


def test_parse_models_body_happy_path() -> None:
    body = json.dumps({"object": "list", "data": [{"id": "llama3.2:1b"}, {"id": "phi4"}]})
    assert _parse_models_body(body) == ["llama3.2:1b", "phi4"]


def test_parse_models_body_empty_data() -> None:
    body = json.dumps({"object": "list", "data": []})
    assert _parse_models_body(body) == []


def test_parse_models_body_missing_data_key() -> None:
    body = json.dumps({"object": "list"})
    assert _parse_models_body(body) == []


def test_parse_models_body_invalid_json_raises() -> None:
    with pytest.raises(ValueError, match="JSON decode error"):
        _parse_models_body("not-json{{{")


def test_parse_models_body_data_not_list() -> None:
    body = json.dumps({"data": "oops"})
    assert _parse_models_body(body) == []


def test_parse_models_body_ignores_entries_without_id() -> None:
    body = json.dumps({"data": [{"name": "x"}, {"id": "valid"}]})
    assert _parse_models_body(body) == ["valid"]


# ---------------------------------------------------------------------------
# probe_models — async, mocked _http_get
# ---------------------------------------------------------------------------


def _make_models_json(*ids: str) -> str:
    return json.dumps({"object": "list", "data": [{"id": i} for i in ids]})


@pytest.mark.asyncio
async def test_probe_models_success() -> None:
    with patch(
        "src.core.providers.FlmModelProbe._http_get",
        new=AsyncMock(return_value=_make_models_json("llama3.2:1b", "phi4")),
    ):
        result = await probe_models("http://127.0.0.1:52625", preferred="llama3")
    assert result.reachable is True
    assert "llama3.2:1b" in result.available_models
    assert result.selected_model == "llama3.2:1b"
    assert result.latency_ms >= 0


@pytest.mark.asyncio
async def test_probe_models_selects_preferred_exact() -> None:
    with patch(
        "src.core.providers.FlmModelProbe._http_get",
        new=AsyncMock(return_value=_make_models_json("phi4", "llama3.2:1b")),
    ):
        result = await probe_models("http://localhost", preferred="phi4")
    assert result.selected_model == "phi4"


@pytest.mark.asyncio
async def test_probe_models_timeout() -> None:
    async def _slow(*_a, **_kw):
        await asyncio.sleep(10)

    with patch("src.core.providers.FlmModelProbe._http_get", new=_slow):
        result = await probe_models("http://localhost", timeout=0.05)
    assert result.reachable is False
    assert "timed out" in (result.error or "").lower()


@pytest.mark.asyncio
async def test_probe_models_connection_error() -> None:
    async def _fail(*_a, **_kw):
        raise OSError("Connection refused")

    with patch("src.core.providers.FlmModelProbe._http_get", new=_fail):
        result = await probe_models("http://localhost")
    assert result.reachable is False
    assert "Connection error" in (result.error or "")


@pytest.mark.asyncio
async def test_probe_models_parse_error() -> None:
    with patch(
        "src.core.providers.FlmModelProbe._http_get",
        new=AsyncMock(return_value="not-json"),
    ):
        result = await probe_models("http://localhost")
    assert result.reachable is False
    assert "parse error" in (result.error or "").lower()


@pytest.mark.asyncio
async def test_probe_models_base_url_normalisation() -> None:
    """Trailing slash on base_url should not cause a double slash in the URL."""
    captured: list[str] = []

    async def _capture(url: str) -> str:
        captured.append(url)
        return _make_models_json("m1")

    with patch("src.core.providers.FlmModelProbe._http_get", new=_capture):
        await probe_models("http://127.0.0.1:52625/")
    assert "//" not in captured[0].replace("http://", "")
