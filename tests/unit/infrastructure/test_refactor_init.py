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

"""Unit tests for fleet initialization and lazy orchestrator access."""

import logging
import sys
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

logging.basicConfig(level=logging.INFO)
root = Path(Path(__file__).resolve().parents[3])

try:
    print("Initializing FleetManager...")
    fleet = FleetManager(str(root))
    print("FleetManager initialized successfully.")

    # Try accessing a lazy-loaded orchestrator
    print("Accessing scaling (lazy)...")
    scaling = fleet.scaling
    print(f"Scaling manager: {scaling}")

    # Try accessing a lazy-loaded agent
    print("Accessing Sandbox agent (lazy)...")
    sandbox = fleet.agents.get("Sandbox")
    print(f"Sandbox agent: {sandbox}")

    print("All tests passed!")
except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
    print(f"FAILED: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
