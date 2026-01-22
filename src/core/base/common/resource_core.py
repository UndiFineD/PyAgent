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
Core logic for Resource Quotas and budget enforcement.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

=======
import time
from typing import Any, Tuple, Optional
from dataclasses import dataclass, field
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
import time
from typing import Any, Tuple, Optional
from dataclasses import dataclass, field
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from .base_core import BaseCore


@dataclass
class QuotaConfig:
    """Configuration for agent resource quotas."""
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    max_tokens: Optional[int] = None
    max_time_seconds: Optional[int] = None
    max_cycles: Optional[int] = None


@dataclass
class ResourceUsage:
    """Current resource usage for an agent session."""
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    tokens_input: int = 0
    tokens_output: int = 0
    start_time: float = field(default_factory=time.time)
    cycles: int = 0

    @property
    def total_tokens(self) -> int:
<<<<<<< HEAD
<<<<<<< HEAD
        """Calculate total tokens consumed."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self.tokens_input + self.tokens_output

    @property
    def elapsed_time(self) -> float:
<<<<<<< HEAD
<<<<<<< HEAD
        """Calculate elapsed time in seconds."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return time.time() - self.start_time


class ResourceCore(BaseCore):
    """
    Authoritative engine for resource quota enforcement.
    """

    def __init__(self, config: Optional[QuotaConfig] = None) -> None:
        super().__init__()
        self.config = config or QuotaConfig()
        self.usage = ResourceUsage()
        self._is_interrupted = False
        self._interrupt_reason: Optional[str] = None

<<<<<<< HEAD
<<<<<<< HEAD
    def update_usage(self, tokens_input: int = 0, tokens_output: int = 0, cycles: int = 0) -> bool:
=======
    def update_usage(
        self, tokens_input: int = 0, tokens_output: int = 0, cycles: int = 0
    ) -> bool:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def update_usage(
        self, tokens_input: int = 0, tokens_output: int = 0, cycles: int = 0
    ) -> bool:
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Update current usage metrics."""
        self.usage.tokens_input += tokens_input
        self.usage.tokens_output += tokens_output
        self.usage.cycles += cycles
        return True

    def check_quotas(self) -> Tuple[bool, Optional[str]]:
        """Check if any quotas have been exceeded."""
        if self.config.max_tokens and self.usage.total_tokens >= self.config.max_tokens:
            self._is_interrupted = True
            self._interrupt_reason = f"Token quota exceeded ({self.usage.total_tokens} >= {self.config.max_tokens})"
            return True, self._interrupt_reason

<<<<<<< HEAD
<<<<<<< HEAD
        if self.config.max_time_seconds and self.usage.elapsed_time >= self.config.max_time_seconds:
            self._is_interrupted = True
            self._interrupt_reason = (
                f"Time quota exceeded ({self.usage.elapsed_time:.2f}s >= {self.config.max_time_seconds}s)"
            )
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if (
            self.config.max_time_seconds
            and self.usage.elapsed_time >= self.config.max_time_seconds
        ):
            self._is_interrupted = True
            self._interrupt_reason = f"Time quota exceeded ({self.usage.elapsed_time:.2f}s >= {self.config.max_time_seconds}s)"
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return True, self._interrupt_reason

        if self.config.max_cycles and self.usage.cycles >= self.config.max_cycles:
            self._is_interrupted = True
            self._interrupt_reason = f"Cycle quota exceeded ({self.usage.cycles} >= {self.config.max_cycles})"
            return True, self._interrupt_reason

        return False, None

    @property
    def is_interrupted(self) -> bool:
<<<<<<< HEAD
<<<<<<< HEAD
        """Check if the session has been interrupted."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self._is_interrupted

    @property
    def interrupt_reason(self) -> Optional[str]:
<<<<<<< HEAD
<<<<<<< HEAD
        """Get the reason for interruption, if any."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self._interrupt_reason

    def get_report(self) -> Dict[str, Any]:
        """Returns a summary of resource usage."""
        return {
            "tokens_input": self.usage.tokens_input,
            "tokens_output": self.usage.tokens_output,
            "total_tokens": self.usage.total_tokens,
            "elapsed_time": self.usage.elapsed_time,
            "cycles": self.usage.cycles,
            "interrupted": self._is_interrupted,
            "reason": self._interrupt_reason,
        }
