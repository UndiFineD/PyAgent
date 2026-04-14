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

"""Replay-specific exception taxonomy."""


class ReplayError(Exception):
    """Base exception for replay subsystem errors."""


class ReplaySchemaError(ReplayError):
    """Raised when replay envelope schema validation fails."""


class ReplaySequenceError(ReplayError):
    """Raised when replay sequence ordering or uniqueness rules fail."""


class ReplayCorruptionError(ReplayError):
    """Raised when persisted replay data is malformed or unreadable."""


class ShadowPolicyViolationError(ReplayError):
    """Raised when a shadow execution envelope requests blocked side effects."""


ShadowPolicyViolation = ShadowPolicyViolationError


class ReplayConfigurationError(ReplayError):
    """Raised when replay components are configured with invalid dependencies."""
