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


"""Expertise Mixin (Phase 61).
Allows agents to declare their domains and performance metrics for MoE routing.
"""


from typing import Any, List, Optional

from src.core.base.common.models.communication_models import ExpertProfile


class ExpertiseMixin:
    """Mixin for agents that participate in Cross-Model MoE.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.expertise_profile: Optional[ExpertProfile] = None


    def declare_expertise(
        self, domains: List[str], performance_score: float = 1.0, model_family: str = "unknown"
    ) -> None:
        """Registers the agent's expertise profile."""
        # Note: agent_id should be available on the base agent
        agent_id: Any | str = getattr(self, "agent_id", "unknown_agent")
        self.expertise_profile = ExpertProfile(
            agent_id=agent_id, domains=domains, performance_score=performance_score, model_family=model_family
        )


    def get_expert_profile(self) -> Optional[ExpertProfile]:
        """Returns the current expertise profile."""
        return self.expertise_profile
