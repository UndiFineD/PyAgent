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
User Space Module

This module contains all user-facing interfaces, personal agents, and human interaction
components. It provides a clean separation between user space and system infrastructure.

Components:
- interface: Web UI, CLI, mobile interfaces
- agents: Personal user agents and assistants
- dashboard: User dashboards and monitoring
- mobile: Mobile-specific interfaces and optimizations
"""

__version__ = "4.0.0"
__all__ = ["interface", "agents", "dashboard", "mobile"]