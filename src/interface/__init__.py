


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


"""
Interface package - User Space Components

This package provides backward compatibility imports for user space components
that have been moved to src/userspace/ for better architectural separation.

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION as VERSION

__version__ = VERSION

# Import user space components for backward compatibility
from src.userspace import interface, agents, dashboard, mobile

# Re-export for backward compatibility
__all__ = ["interface", "agents", "dashboard", "mobile"]"