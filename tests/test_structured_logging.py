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
"""Tests for structured JSON logging (prj0000063)."""
from __future__ import annotations

import logging

from pythonjsonlogger.json import JsonFormatter


def test_logging_config_module_imports():
    """logging_config module is importable and exposes setup_logging / get_logger."""
    from backend.logging_config import get_logger, setup_logging  # noqa: F401

    assert callable(setup_logging)
    assert callable(get_logger)


def test_setup_logging_returns_logger():
    """setup_logging() returns a logging.Logger instance."""
    from backend.logging_config import setup_logging

    result = setup_logging()
    assert isinstance(result, logging.Logger)


def test_get_logger_returns_named_logger():
    """get_logger('pyagent.backend') returns a logger with the correct name."""
    from backend.logging_config import get_logger

    lg = get_logger("pyagent.backend")
    assert isinstance(lg, logging.Logger)
    assert lg.name == "pyagent.backend"


def test_logger_has_json_handler():
    """After setup_logging(), the logger has at least one StreamHandler with JsonFormatter."""
    from backend.logging_config import setup_logging

    lg = setup_logging()
    stream_handlers = [h for h in lg.handlers if isinstance(h, logging.StreamHandler)]
    assert stream_handlers, "Expected at least one StreamHandler"
    json_formatters = [
        h for h in stream_handlers if isinstance(h.formatter, JsonFormatter)
    ]
    assert json_formatters, "Expected at least one handler with JsonFormatter"


def test_correlation_id_middleware_adds_header():
    """GET /health response must include the X-Correlation-ID header."""
    from fastapi.testclient import TestClient

    from backend.app import app

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/health")
    assert response.status_code == 200
    assert "x-correlation-id" in {k.lower() for k in response.headers}
