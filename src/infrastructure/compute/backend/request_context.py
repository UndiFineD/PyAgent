#!/usr/bin/env python3
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
Auto-extracted class from agent_backend.py
"""


from __future__ import annotations


try:
    import time
except ImportError:
    import time

try:
    import uuid
except ImportError:
    import uuid

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .request_priority import RequestPriority
except ImportError:
    from .request_priority import RequestPriority


__version__ = VERSION


@dataclass
class RequestContext:
    """Context for a backend request.
    Attributes:
        request_id: Unique identifier for tracking.
        correlation_id: ID for tracing across services.
        priority: Request priority level.
        created_at: Timestamp when request was created.
        metadata: Additional request metadata.
    """
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str | None = None
    priority: RequestPriority = RequestPriority.NORMAL
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=lambda: {})
