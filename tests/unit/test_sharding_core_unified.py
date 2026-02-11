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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from src.core.base.common.sharding_core import ShardingCore

def test_sharding_core_calculate_splits():
    core = ShardingCore(cluster_size=4)
    shape = [1024, 1024]
    num_nodes = 2
    splits = core.calculate_splits(shape, num_nodes)

    assert len(splits) == 2
    # If rust is active, it might use node_id as keys (0 and 1)
    # Python fallback uses 0 and 1 as well.
    assert splits[0][-1] == 512
    assert splits[1][-1] == 512

def test_sharding_core_assign_workload():
    core = ShardingCore()
    loads = [0.1, 0.9, 0.2, 0.5]
    best_node = core.assign_workload(loads)

    # P2C or Min should pick 0 or 2 (0.1 or 0.2)
    assert best_node in [0, 2]

def test_sharding_core_calculate_shard_id():
    core = ShardingCore(cluster_size=10)
    key = "test_key"
    shard_id = core.calculate_shard_id(key)

    assert 0 <= shard_id < 10
    # Determinism
    assert shard_id == core.calculate_shard_id(key)

def test_sharding_core_verify_sync():
    core = ShardingCore()
    assert core.verify_sync([True, True, True]) is True
    assert core.verify_sync([True, False, True]) is False
