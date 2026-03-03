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
Logic Package - Core implementation of agent reasoning and utilities.
"""

from .acceleration_manager import NeuralPruningEngine  # noqa: F401
from .agent_plugin_base import AgentPluginBase  # noqa: F401
from .agent_verification import (AgentVerifier, CodeHealthAuditor,  # noqa: F401
                                 CodeIntegrityVerifier)
from .circuit_breaker import CircuitBreaker  # noqa: F401
from .connectivity_manager import ConnectivityManager  # noqa: F401
from .dependency_graph import DependencyGraph  # noqa: F401
from .incremental_processor import IncrementalProcessor  # noqa: F401
from .logging_config import setup_logging  # noqa: F401
from .sandbox_manager import SandboxManager  # noqa: F401

__all__ = [
    "NeuralPruningEngine",
    "AgentPluginBase",
    "AgentVerifier",
    "CodeHealthAuditor",
    "CodeIntegrityVerifier",
    "CircuitBreaker",
    "ConnectivityManager",
    "DependencyGraph",
    "IncrementalProcessor",
    "setup_logging",
    "SandboxManager",
]
