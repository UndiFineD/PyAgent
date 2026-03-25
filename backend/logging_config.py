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
"""JSON structured logging configuration for the PyAgent backend."""
from __future__ import annotations

import logging

from pythonjsonlogger.json import JsonFormatter


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure JSON structured logging for the backend.

    Idempotent — if handlers are already attached, the existing logger is returned
    unchanged so that calling this function more than once (e.g. during hot-reload)
    does not double-add handlers.
    """
    logger = logging.getLogger("pyagent.backend")
    if logger.handlers:
        return logger  # already configured

    handler = logging.StreamHandler()
    formatter = JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s %(correlation_id)s %(endpoint)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger


def get_logger(name: str = "pyagent.backend") -> logging.Logger:
    """Return the configured logger by name."""
    return logging.getLogger(name)
