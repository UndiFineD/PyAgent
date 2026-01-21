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
Verification logic for agent outputs.
Implements Stanford Reseach 'Anchoring Strength' and Keio University 'Self-Verification' paths.
"""

from __future__ import annotations
from src.core.base.version import VERSION

# Phase 317: Modularized Verification Classes
from .verification.agent_verifier import AgentVerifier as AgentVerifier
from .verification.code_health_auditor import CodeHealthAuditor as CodeHealthAuditor
from .verification.code_integrity_verifier import CodeIntegrityVerifier as CodeIntegrityVerifier

__version__ = VERSION
