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

"""Contract tests for adapter contract version compatibility gates."""

from __future__ import annotations

import pytest

from src.agents.specialization.contract_versioning import ensure_supported, parse_major
from src.agents.specialization.errors import ContractVersionError


def test_parse_major_accepts_semver() -> None:
    """Semantic parser should return major version for valid semver."""
    assert parse_major("1.2.3") == 1


def test_ensure_supported_rejects_unsupported_major() -> None:
    """Major-version mismatch should be rejected with typed reason."""
    with pytest.raises(ContractVersionError) as exc:
        ensure_supported("2.0.0")

    assert exc.value.reason_code == "unsupported_contract_major"


def test_parse_major_rejects_invalid_version_format() -> None:
    """Invalid version formats should fail deterministically."""
    with pytest.raises(ContractVersionError) as exc:
        parse_major("v1")

    assert exc.value.reason_code == "invalid_contract_version"
