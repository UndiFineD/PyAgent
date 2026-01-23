#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 68: Expert Specialization Evolution

import pytest
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.swarm.orchestration.swarm.expert_evolution import ExpertEvolutionService
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.core.base.common.models.communication_models import ExpertProfile, ExpertEvaluation

@pytest.mark.asyncio
async def test_expert_evolution_score_adjustment():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    # Set high learning rate for obvious test results
    evolution_service = ExpertEvolutionService(gatekeeper, learning_rate=0.5)

    # 1. Register expert with baseline score
    expert_id = "test_expert"
    gatekeeper.register_expert(ExpertProfile(
        agent_id=expert_id,
        domains=["general"],
        performance_score=1.0
    ))

    # 2. Process negative evaluation (Expert failed task)
    fail_eval = ExpertEvaluation(
        expert_id=expert_id,
        task_id="task1",
        is_correct=False,
        quality_score=0.2
    )
    # Target = 0.2 * 0.5 = 0.1
    # New Score = (0.5 * 1.0) + (0.5 * 0.1) = 0.55
    evolution_service.process_evaluation(fail_eval)

    assert gatekeeper.experts[expert_id].performance_score == 0.55

    # 3. Process positive evaluation (Expert recovered)
    success_eval = ExpertEvaluation(
        expert_id=expert_id,
        task_id="task2",
        is_correct=True,
        quality_score=0.9
    )
    # Target = 0.9
    # New Score = (0.5 * 0.55) + (0.5 * 0.9) = 0.275 + 0.45 = 0.725
    evolution_service.process_evaluation(success_eval)

    assert gatekeeper.experts[expert_id].performance_score == pytest.approx(0.725)

@pytest.mark.asyncio
async def test_evolution_impacts_routing():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    # Very high learning rate to ensure immediate change
    evolution_service = ExpertEvolutionService(gatekeeper, learning_rate=0.99)

    # Register two identical experts with identical domains
    # We clear the cache to be safe
    gatekeeper.register_expert(ExpertProfile(agent_id="e1", domains=["tech"], performance_score=1.0))
    gatekeeper.register_expert(ExpertProfile(agent_id="e2", domains=["tech"], performance_score=1.0))

    # Tank e1's health
    for _ in range(5): # Multiple evals to really hammer it down
        evolution_service.process_evaluation(ExpertEvaluation(
            expert_id="e1", task_id="t1", is_correct=False, quality_score=0.0
        ))

    # Route for a task matching "tech"
    decision2 = await gatekeeper.route_task("coding tech problem", top_k=2)

    # e2 (score ~1.0) should be way ahead of e1 (score ~0.1)
    assert decision2.selected_experts[0] == "e2"
