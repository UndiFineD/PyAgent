#!/usr/bin/env python3
"""Utility functions for PyAgent."""
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

from typing import List

from chat.models import ChatRoom


def create_personal_room(human: str) -> ChatRoom:
    """Create a personal chat room for *human* with an AI agent added.

    The room name follows the `personal-{human}` convention. The participants
    list contains the human plus at least one agent identifier (e.g.
    "agent-1").
    """
    name = f"personal-{human}"
    # simplistic agent naming; real implementation might generate or look up
    agent_id = f"agent-{human}"
    room = ChatRoom(name, [human, agent_id])
    return room
