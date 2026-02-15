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

"""
Logging config.py module.
"""

import logging
import os

from src.infrastructure.services.logging.core.log_rotation_core import \
    LogRotationCore


def setup_fleet_logging(log_dir: str = "data/logs", health_score: float = 1.0) -> None:
    """
    Sets up the fleet logging with rotation and dynamic levels.
    """
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "fleet.log")

    core = LogRotationCore(log_dir)

    # Check for rotation
    if core.should_rotate(log_file):
        core.rotate_and_compress(log_file)

    log_level_str = core.calculate_log_level(health_score)
    log_level = getattr(logging, log_level_str)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        force=True,
    )
    logging.info(f"Fleet logging initialized at level: {log_level_str}")


if __name__ == "__main__":
    setup_fleet_logging(health_score=0.5)
