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



from __future__ import annotations

from enum import Enum
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

class SLALevel(Enum):
  # SLA priority levels.
  P0 = 1  # 24 hours
  P1 = 2  # 3 days
  P2 = 3  # 1 week
  P3 = 4  # 2 weeks
  P4 = 5  # 1 month
