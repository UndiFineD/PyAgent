
"""
Test Phase60 Async Spec module.
"""
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Tests for Phase 60: Speculative Async Output Pipeline

import pytest
from unittest.mock import MagicMock, AsyncMock
from src.infrastructure.engine.speculative.async_pipeline import SpeculativeAsyncPipeline
from src.core.base.common.models.communication_models import (
    AsyncSpeculativeToken, PipelineCorrection, VerificationOutcome
)

@pytest.mark.asyncio
async def test_async_pipeline_success_flow():
    # Mock orchestrator
    mock_orch = MagicMock()

    # Mock outcome (accepted)
    outcome = VerificationOutcome(
        proposal_id="test",
        accepted=True,
        final_content="Sure, here is the answer: 42.",
        accepted_length=20,
        correction_applied=False,
        verifier_id="target"
    )

    mock_orch.execute_speculative_task = AsyncMock(return_value=outcome)

    pipeline = SpeculativeAsyncPipeline(mock_orch)

    tokens = []
    async for item in pipeline.generate_stream("test task", "draft", "target"):
        if isinstance(item, AsyncSpeculativeToken):
            tokens.append(item)

    # Check that we received draft tokens followed by verified tokens
    assert any(t.is_draft for t in tokens)
    assert any(not t.is_draft for t in tokens)
    assert "42." in "".join([t.token for t in tokens])

@pytest.mark.asyncio
async def test_async_pipeline_rollback_flow():
    mock_orch = MagicMock()

    # Mock outcome (REJECTED)
    outcome = VerificationOutcome(
        proposal_id="test",
        accepted=False,
        final_content="Actually, that is incorrect.",
        accepted_length=0,
        correction_applied=True,
        verifier_id="target"
    )

    mock_orch.execute_speculative_task = AsyncMock(return_value=outcome)

    pipeline = SpeculativeAsyncPipeline(mock_orch)

    events = []
    async for item in pipeline.generate_stream("bad task", "draft", "target"):
        events.append(item)

    # We should have received several draft tokens AND a PipelineCorrection
    assert any(isinstance(e, PipelineCorrection) for e in events)
    correction = next(e for e in events if isinstance(e, PipelineCorrection))
    assert correction.rollback_to_index == 0
    assert "Actually," == correction.correct_tokens[0]