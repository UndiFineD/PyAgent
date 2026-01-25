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

from typing import Any

try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass


def test_sha256_text(report_module: Any) -> None:
    """Test SHA256 calculation."""
    from src.observability.reports.ReportGeneratorCLI import _sha256_text

    text = "hello world"
    # echo -n "hello world" | sha256sum
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert _sha256_text(text) == expected
