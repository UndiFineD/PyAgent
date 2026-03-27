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

"""Typed exception hierarchy for fuzzing core failures."""


class FuzzingError(Exception):
    """Base exception for all fuzzing domain failures."""


class FuzzConfigurationError(FuzzingError):
    """Raised when fuzzing components receive invalid configuration."""


class FuzzExecutionError(FuzzingError):
    """Raised for runtime execution failures during campaign orchestration."""


class FuzzPolicyViolation(FuzzingError):  # noqa: N818
    """Raised when a request violates local safety or budget policy."""


class UnknownMutationOperatorError(FuzzConfigurationError):
    """Raised when a mutator operator is not registered."""
