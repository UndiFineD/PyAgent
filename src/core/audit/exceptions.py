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

"""Exception hierarchy for immutable audit-trail operations."""


class AuditTrailError(Exception):
    """Base exception for all audit-trail failures."""


class AuditSerializationError(AuditTrailError):
    """Raised when audit event serialization or deserialization fails."""


class AuditChainLinkError(AuditTrailError):
    """Raised when hash-chain linkage between records is invalid."""


class AuditIntegrityError(AuditTrailError):
    """Raised when a record hash does not match recomputed integrity data."""


class AuditPersistenceError(AuditTrailError):
    """Raised when audit records cannot be persisted or read."""


def validate() -> bool:
    """Return whether module contracts are loadable.

    Returns:
        Always ``True`` when the module can be imported.

    """
    return True


__all__ = [
    "AuditTrailError",
    "AuditSerializationError",
    "AuditChainLinkError",
    "AuditIntegrityError",
    "AuditPersistenceError",
    "validate",
]
