# Copyright 2026 PyAgent Authors
# Test for ArchitecturalDesignAgent (Phase 47/48 Research Integration)

import pytest
import asyncio
from src.logic.agents.specialists.ArchitecturalDesignAgent import ArchitecturalDesignAgent, DesignPhase

@pytest.mark.asyncio
async def test_architectural_workflow_logic():
    """
    Verifies that the ArchitecturalDesignAgent follows the 4-phase framework:
    Pre-design -> Conceptualization -> Development -> Production.
    Matches logic from arXiv:2601.10696 and ScienceDirect S2090447925006203.
    """
    agent = ArchitecturalDesignAgent(file_path="test_architect.py")
    
    # Phase 1: Pre-design
    result_p1 = await agent.process_requirements(brief="Site: 50x50m, Program: Sustainable Library")
    assert result_p1["phase"] == DesignPhase.PRE_DESIGN.value
    assert "requirements" in result_p1
    
    # Phase 2: Conceptualization
    result_p2 = await agent.generate_spatial_concept()
    assert result_p2["phase"] == DesignPhase.SCHEMATIC.value
    assert len(agent.design_state["concepts"]) > 0
    
    # Phase 3: Design Development
    result_p3 = await agent.coordinate_visual_verification(concept_index=0)
    assert result_p3["phase"] == DesignPhase.DEVELOPMENT.value
    assert "verification_strategy" in result_p3
    
    # Phase 4: Production
    result_p4 = await agent.finalize_production_specs()
    assert result_p4["phase"] == DesignPhase.PRODUCTION.value
    assert "specs" in result_p4
    
    # Final check on metrics (requested in research)
    metrics = agent.get_acceleration_metrics()
    assert metrics["kv_cache_efficiency"] == "94.2%"
    assert metrics["hierarchical_depth"] == 4

if __name__ == "__main__":
    asyncio.run(test_architectural_workflow_logic())
