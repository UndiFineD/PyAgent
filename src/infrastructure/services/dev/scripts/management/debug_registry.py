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


"""Debug script for inspecting the agent registry."""

from __future__ import annotations

import os

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

__version__ = VERSION

f = FleetManager(os.getcwd())
print(f"Agents in registry: {len(f.agents.keys())}")
print(f"Sample: {f.agents.keys()[:5]}")
print(f"Has CooperativeCommunication? {'CooperativeCommunication' in f.agents}")
print(f"Has cooperative_communication? {'cooperative_communication' in f.agents}")
