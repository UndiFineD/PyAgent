#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
import os
import numpy as np
from src.infrastructure.swarm.orchestration.swarm.audit_logger import SwarmAuditLogger
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.swarm.orchestration.swarm.expert_fusion import WeightedExpertFusion
from src.core.base.common.models.communication_models import ExpertProfile

class MockSimilarity:
    async def get_embedding(self, text: str):
        return np.random.randn(384).astype(np.float32)

    async def get_embeddings(self, text: list):
        return [np.random.randn(384).astype(np.float32) for _ in text]

@pytest.mark.asyncio
async def test_swarm_audit_trail_flow():
    """
    Verifies that routing and fusion events are correctly captured in the audit log.
    """
    storage_path = "data/logs/test_audit.jsonl"
    if os.path.exists(storage_path):
        os.remove(storage_path)

    audit_logger = SwarmAuditLogger(storage_path=storage_path)
    similarity = MockSimilarity()

    # 1. Test Gateway Auditing
    gatekeeper = MoEGatekeeper(similarity_service=similarity, audit_logger=audit_logger)
    gatekeeper.register_expert(ExpertProfile(
        agent_id="agent_alpha",
        domains=["coding"],
        performance_score=0.9
    ))

    decision = await gatekeeper.route_task("Write a python script", top_k=1)
    task_id = decision.task_id

    # 2. Test Fusion Auditing
    fusion = WeightedExpertFusion(audit_logger=audit_logger)
    await fusion.fuse_outputs(
        outputs=["Result 1", "Result 1"],
        weights=[0.9, 0.8],
        expert_ids=["agent_alpha", "agent_beta"],
        mode="weighted_plurality",
        task_id=task_id
    )

    # 3. Verify Logs
    logs = audit_logger.get_trail(task_id)
    assert len(logs) == 2

    event_types = [event.step for event in logs]
    assert "routing_decision" in event_types
    assert "expert_fusion" in event_types

    # Check persistence
    assert os.path.exists(storage_path)
    with open(storage_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert len(lines) >= 2

    print(f"\nAudit trail for {task_id} verified with {len(logs)} events.")

@pytest.mark.asyncio
async def test_audit_logger_retention():
    """Verifies that the audit logger correctly fetches the latest trail."""
    audit_logger = SwarmAuditLogger(storage_path="data/logs/test_retention.jsonl")
    task_id = "test_task_retention"

    audit_logger.log_event(task_id, "start", "Task started", {"meta": "begin"})
    audit_logger.log_event(task_id, "step_1", "Doing something", {"val": 42})
    audit_logger.log_event(task_id, "end", "Task finished", {"status": "ok"})

    trail = audit_logger.get_trail(task_id)
    assert len(trail) == 3
    assert trail[0].step == "start"
    assert trail[2].step == "end"
