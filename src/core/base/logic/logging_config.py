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


"""Logging configuration for PyAgent."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import os
from typing import Dict

__version__ = VERSION

def setup_logging(verbosity_arg: int = 0) -> None:
    """Configure logging based on environment variable and argument.

    Sets up Python's logging system with level determined by environment
    variable (DV_AGENT_VERBOSITY) and / or command - line argument.

    Args:
        verbosity_arg: Verbosity level from --verbose argument (0-3).
                      Levels: 0=ERROR, 1=WARNING, 2=INFO, 3=DEBUG.
                      Defaults to 0 (ERROR).

    Returns:
        None. Configures the global logging system.

    Environment Variables:
        DV_AGENT_VERBOSITY: Can be set to 'quiet', 'minimal', 'normal', or 'elaborate'.

    Note:
        - verbosity_arg takes precedence when provided and forces DEBUG level
        - Environment variable is used as fallback
        - Defaults to INFO level if neither is set
    """
    env_verbosity: str | None = os.environ.get('DV_AGENT_VERBOSITY')
    levels: dict[str, int] = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
        '0': logging.ERROR,
        '1': logging.WARNING,
        '2': logging.INFO,
        '3': logging.DEBUG,
    }
    # Determine level from environment
    if env_verbosity:
        level: int = levels.get(env_verbosity.lower(), logging.WARNING)
    else:
        # Default to WARNING to reduce noise, as requested by self-improvement phase
        level: int = logging.WARNING
    # If argument is provided, it forces DEBUG (elaborate)
    if verbosity_arg > 0:
        level: int = logging.DEBUG
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    logging.debug(f"Logging configured at level: {logging.getLevelName(level)}")