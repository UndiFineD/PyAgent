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

import unittest
import logging
from src.infrastructure.swarm.resilience.checkpoint_manager import CheckpointManager

logging.basicConfig(level=logging.INFO)

class TestCheckpointRDMA(unittest.IsolatedAsyncioTestCase):
    async def test_checkpoint_lifecycle(self):
        """Verify the RDMA checkpoint and recovery lifecycle (Phase 330)."""
        manager = CheckpointManager(rank=0, world_size=2)

        # 1. Create Checkpoint
        state_data = b"MOCK_AGENT_STATE_V4_OPTIMIZED"
        checkpoint_id = await manager.create_checkpoint(state_data)

        self.assertTrue(checkpoint_id.startswith("ckpt-"), "Checkpoint ID should be generated")

        latest = manager.get_latest_checkpoint()
        self.assertIsNotNone(latest)
        self.assertEqual(latest.id, checkpoint_id)
        self.assertEqual(latest.data_size, len(state_data))

        # 2. Verify Recovery (Stubbed)
        recovered = await manager.recover_from_checkpoint(checkpoint_id)
        self.assertIsNotNone(recovered, "Recovery should return state stub")
        self.assertEqual(recovered, b"RECOVERED_STATE_STUB")

        logging.info(f"RDMA Checkpoint lifecycle verified for ID: {checkpoint_id}")

    async def test_multi_rank_config(self):
        """Verify peer rank calculation for ring buddy system."""
        mgr0 = CheckpointManager(rank=0, world_size=4)
        mgr3 = CheckpointManager(rank=3, world_size=4)

        self.assertEqual(mgr0.peer_rank, 1)
        self.assertEqual(mgr3.peer_rank, 0)

        logging.info("RDMA Peer Buddy ranks verified.")

if __name__ == "__main__":
    unittest.main()
