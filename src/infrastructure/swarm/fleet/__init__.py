# Put future import at module top
from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Fleet package."""

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .async_fleet_manager import AsyncFleetManager
except ImportError:
    from .async_fleet_manager import AsyncFleetManager

try:
    from .fleet_manager import FleetManager
except ImportError:
    from .fleet_manager import FleetManager

try:
    from .workflow_state import WorkflowState
except ImportError:
    from .workflow_state import WorkflowState



__version__ = VERSION
__all__ = ["VERSION", "FleetManager", "AsyncFleetManager", "WorkflowState"]