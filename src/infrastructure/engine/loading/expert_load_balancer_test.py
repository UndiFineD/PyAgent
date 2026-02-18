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
    from infrastructure.engine.loading.expert_load_balancer import ExpertType, EplbMetrics, ExpertMapping, AbstractEplbPolicy, DefaultEplbPolicy, LocalityAwarePolicy, ExpertLoadBalancer, AsyncExpertRebalancer, compute_balanced_packing_rust, compute_expert_replication_rust, compute_load_imbalance_rust
except ImportError:
    from infrastructure.engine.loading.expert_load_balancer import ExpertType, EplbMetrics, ExpertMapping, AbstractEplbPolicy, DefaultEplbPolicy, LocalityAwarePolicy, ExpertLoadBalancer, AsyncExpertRebalancer, compute_balanced_packing_rust, compute_expert_replication_rust, compute_load_imbalance_rust



def test_experttype_basic():
    assert ExpertType is not None


def test_eplbmetrics_basic():
    assert EplbMetrics is not None


def test_expertmapping_basic():
    assert ExpertMapping is not None


def test_abstracteplbpolicy_basic():
    assert AbstractEplbPolicy is not None


def test_defaulteplbpolicy_basic():
    assert DefaultEplbPolicy is not None


def test_localityawarepolicy_basic():
    assert LocalityAwarePolicy is not None


def test_expertloadbalancer_basic():
    assert ExpertLoadBalancer is not None


def test_asyncexpertrebalancer_basic():
    assert AsyncExpertRebalancer is not None


def test_compute_balanced_packing_rust_basic():
    assert callable(compute_balanced_packing_rust)


def test_compute_expert_replication_rust_basic():
    assert callable(compute_expert_replication_rust)


def test_compute_load_imbalance_rust_basic():
    assert callable(compute_load_imbalance_rust)
