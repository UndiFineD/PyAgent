#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from infrastructure.swarm.orchestration.core.distributed.executor import DistributedExecutor, MultiProcessExecutor, create_distributed_executor, get_dp_rank, get_dp_size, get_tp_rank, get_tp_size


def test_distributedexecutor_basic():
    assert DistributedExecutor is not None


def test_multiprocessexecutor_basic():
    assert MultiProcessExecutor is not None


def test_create_distributed_executor_basic():
    assert callable(create_distributed_executor)


def test_get_dp_rank_basic():
    assert callable(get_dp_rank)


def test_get_dp_size_basic():
    assert callable(get_dp_size)


def test_get_tp_rank_basic():
    assert callable(get_tp_rank)


def test_get_tp_size_basic():
    assert callable(get_tp_size)
