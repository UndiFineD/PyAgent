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
"""Agents package — design and quality framework for PyAgent agents.

Exports the core agent primitives:
  - BaseAgent: abstract base class for all agents
  - AgentLifecycle: lifecycle state machine (IDLE → RUNNING → STOPPED)
  - AgentManifest: metadata descriptor for an agent
"""

from __future__ import annotations

from src.agents.BaseAgent import AgentLifecycle, AgentManifest, BaseAgent

__all__ = ["BaseAgent", "AgentLifecycle", "AgentManifest"]
