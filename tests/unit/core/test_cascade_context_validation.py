"""
Test Cascade Context Validation.
"""

import pytest
from src.core.base.common.models.communication_models import CascadeContext

def test_cascade_context_initialization_limit():
    """Test that initializing context with depth > limit raises error."""
    with pytest.raises(RecursionError):
        CascadeContext(cascade_depth=11, depth_limit=10)

def test_cascade_context_next_level_limit():
    """Test that next_level enforces limit."""
    ctx = CascadeContext(cascade_depth=9, depth_limit=10)

    # 9 -> 10 (Allowed, as logic is >= check in next_level)
    # Wait, code says: if self.cascade_depth >= self.depth_limit: raise
    # So if depth=9, limit=10, 9 < 10. OK.

    next_ctx = ctx.next_level("agent_1")
    assert next_ctx.cascade_depth == 10

    # Now depth=10. check 10 >= 10. Should raise.
    with pytest.raises(RecursionError):
        next_ctx.next_level("agent_2")

def test_circular_dependency_detection():
    """Test circular dependency detection."""
    ctx = CascadeContext(agent_lineage=["agent_A", "agent_B"])

    # Delegating to agent_C (new)
    next_ctx = ctx.next_level("agent_C")
    assert "agent_C" in next_ctx.agent_lineage

    # Delegating to agent_A (existing) -> Should raise
    with pytest.raises(RecursionError) as excinfo:
        ctx.next_level("agent_A")

    assert "Circular Dependency Detected" in str(excinfo.value)

def test_lineage_propagation():
    """Test lineage propagation."""
    ctx0 = CascadeContext()
    ctx1 = ctx0.next_level("agent_1")
    ctx2 = ctx1.next_level("agent_2")

    assert ctx2.agent_lineage == ["agent_1", "agent_2"]
    assert ctx2.parent_agent_id == "agent_2"
    assert ctx2.cascade_depth == 2
