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

import pytest
from core.base.logic.core.satellite_reconnaissance_core import SatelliteAsset, SatelliteReconResult, SatelliteReconConfig, SatelliteReconnaissanceCore


def test_satelliteasset_basic():
    assert SatelliteAsset is not None


def test_satellitereconresult_basic():
    assert SatelliteReconResult is not None


def test_satellitereconconfig_basic():
    assert SatelliteReconConfig is not None


def test_satellitereconnaissancecore_basic():
    assert SatelliteReconnaissanceCore is not None
