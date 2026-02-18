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

try:
    import pytest
except ImportError:
    import pytest

try:
    from infrastructure.compute.moe.expert_router import RoutingMethod, RouterConfig, RouterOutput, RouterBase, TopKRouter, GroupedTopKRouter, ExpertChoiceRouter, SoftMoERouter, AdaptiveRouter, RoutingSimulator
except ImportError:
    from infrastructure.compute.moe.expert_router import RoutingMethod, RouterConfig, RouterOutput, RouterBase, TopKRouter, GroupedTopKRouter, ExpertChoiceRouter, SoftMoERouter, AdaptiveRouter, RoutingSimulator



def test_routingmethod_basic():
    assert RoutingMethod is not None


def test_routerconfig_basic():
    assert RouterConfig is not None


def test_routeroutput_basic():
    assert RouterOutput is not None


def test_routerbase_basic():
    assert RouterBase is not None


def test_topkrouter_basic():
    assert TopKRouter is not None


def test_groupedtopkrouter_basic():
    assert GroupedTopKRouter is not None


def test_expertchoicerouter_basic():
    assert ExpertChoiceRouter is not None


def test_softmoerouter_basic():
    assert SoftMoERouter is not None


def test_adaptiverouter_basic():
    assert AdaptiveRouter is not None


def test_routingsimulator_basic():
    assert RoutingSimulator is not None
