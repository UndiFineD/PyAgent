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

"""Per-module red tests for the FuzzResult contract module."""

from __future__ import annotations

from tests.test_fuzzing_core import _build_case, _require_symbol


def test_fuzz_result_aggregator_contract_from_case_results() -> None:
    """Verify FuzzCampaignResult can aggregate typed case results."""
    case_result_cls = _require_symbol("FuzzResult", "FuzzCaseResult")
    campaign_cls = _require_symbol("FuzzResult", "FuzzCampaignResult")
    case = _build_case(case_id="case-result")
    campaign = campaign_cls.from_case_results(
        [case_result_cls(case=case, status="success", duration_ms=1, bytes_sent=4, error=None)]
    )
    assert campaign.summary_counts["success"] == 1
