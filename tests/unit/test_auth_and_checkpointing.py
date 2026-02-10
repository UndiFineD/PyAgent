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
import asyncio
from src.infrastructure.security.auth.webauthn_manager import WebAuthnManager
from src.infrastructure.swarm.resilience.checkpoint_manager import CheckpointManager

@pytest.mark.asyncio
async def test_webauthn_options_generation():
    manager = WebAuthnManager(rp_id="localhost", rp_name="PyAgentTest")
    username = "testuser"
    
    options = manager.get_registration_options(username)
    assert "challenge" in options
    assert "rp" in options
    assert options["rp"]["name"] == "PyAgentTest"
    assert username in manager.challenges

@pytest.mark.asyncio
async def test_oauth_initialization():
    manager = WebAuthnManager()
    assert manager.oauth is not None
    assert 'github' in manager.oauth._clients

@pytest.mark.asyncio
async def test_rdma_checkpoint_basic():
    # We use rank 0/2 to test buddy logic
    manager = CheckpointManager(rank=0, world_size=2)
    assert manager.peer_rank == 1
    
    state = b'{"agents": ["coder"], "version": "4.0.0"}'
    checkpoint_id = await manager.create_checkpoint(state)
    
    assert checkpoint_id.startswith("ckpt-")
    latest = manager.get_latest_checkpoint()
    assert latest is not None
    assert latest.id == checkpoint_id
    assert latest.data_size == len(state)

@pytest.mark.asyncio
async def test_rdma_recovery_stub():
    manager = CheckpointManager(rank=0, world_size=2)
    recovered = await manager.recover_from_checkpoint("ckpt-dummy")
    assert recovered == b"RECOVERED_STATE_STUB"
