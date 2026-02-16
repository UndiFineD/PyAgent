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

import pytest
from infrastructure.services.dev.scripts.analysis.run_profiled_self_improvement import RustFunctionStats, RustProfiler, ComprehensiveProfileAnalyzer, save_profile_report


def test_rustfunctionstats_basic():
    assert RustFunctionStats is not None


def test_rustprofiler_basic():
    assert RustProfiler is not None


def test_comprehensiveprofileanalyzer_basic():
    assert ComprehensiveProfileAnalyzer is not None


def test_save_profile_report_basic():
    assert callable(save_profile_report)
