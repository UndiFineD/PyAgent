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

"""Shadow mode routing wrapper for parity verification."""

from __future__ import annotations

from src.core.routing.prompt_routing_facade import PromptRoutingFacade
from src.core.routing.routing_models import PromptRoutingRequest, RouteDecisionRecord


class ShadowModeRouter:
    """Run routing in shadow mode with identical decision contract."""

    def __init__(self, facade: PromptRoutingFacade) -> None:
        """Initialize shadow mode router.

        Args:
            facade: Routing facade used by active path.

        """
        self._facade = facade

    async def route(self, request: PromptRoutingRequest) -> RouteDecisionRecord:
        """Route request in shadow mode.

        Args:
            request: Routing request.

        Returns:
            Same decision contract as active mode.

        """
        return await self._facade.route(request)
