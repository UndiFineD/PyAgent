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


"""Standard exception types for the PyAgent base framework."""
from __future__ import annotations




class PyAgentException(Exception):
    """Base exception for all PyAgent errors."""
    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)

        self.error_code = error_code




class InfrastructureError(PyAgentException):
    """Errors related to system infrastructure (I/O, Network)."""



class LogicError(PyAgentException):
    """Errors related to agent logic or reasoning failure."""



class SecurityError(PyAgentException):
    """Errors related to unauthorized access or safety violations."""



class ModelError(PyAgentException):
    """Errors related to LLM connectivity or output parsing."""



class ConfigurationError(PyAgentException):
    """Errors in settings or manifest validation."""



class CycleInterrupt(PyAgentException):
    """Interruption of an agent cycle (e.g., quota exceeded)."""