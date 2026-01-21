# Copyright 2026 PyAgent Authors
# Test for ArchitecturalDesignAgent (Phase 47/48 Research Integration)

import pytest
import asyncio
from src.logic.agents.specialists.architectural_design_agent import ArchitecturalDesignAgent, DesignPhase

@pytest.mark.asyncio
async def test_architectural_workflow_logic():
    """
    Verifies that the ArchitecturalDesignAgent follows the expanded 5-phase framework:
    Pre-design Analysis -> Concept Gen -> (Critique) -> Development -> Production -> Post-prod.
    Matches logic from arXiv:2601.10696 and ScienceDirect S2090447925006203 (Jiang et al., 2026).
    """
    agent = ArchitecturalDesignAgent(file_path="test_architect.py")
    
    # Phase 1: Pre-design Analysis
    result_p1 = await agent.process_requirements(brief="Site: 50x50m, Program: Sustainable Library")
    assert result_p1["phase"] == DesignPhase.PRE_DESIGN_ANALYSIS.value
    assert "requirements" in result_p1
    
    # Phase 2: Concept Generation (GAAD loop)
    result_p2 = await agent.generate_spatial_concept()
    assert result_p2["phase"] == DesignPhase.CONCEPT_GENERATION.value
    assert "final_optimized_concept" in result_p2
    assert "internal_critique" in result_p2
    assert len(agent.design_state["concepts"]) > 0
    
    # Critical Engagement Buffer (Must pass before Phase 3)
    await agent.critical_engagement_buffer(critique="The concept is interesting. Please proceed.")
    assert agent.design_state["critique_passed"] is True
    
    # Phase 3: Design Development
    result_p3 = await agent.coordinate_visual_verification(concept_index=0)
    assert result_p3["phase"] == DesignPhase.DESIGN_DEVELOPMENT.value
    assert "verification_strategy" in result_p3
    
    # Phase 4: Design Production
    result_p4 = await agent.finalize_production_specs()
    assert result_p4["phase"] == DesignPhase.DESIGN_PRODUCTION.value
    assert "specs" in result_p4
    assert result_p4["constructability_score"] > 0

    # Phase 5: Post-production
    result_p5 = await agent.synthesize_presentation()
    assert result_p5["phase"] == DesignPhase.POST_PRODUCTION.value
    assert "presentation_link" in result_p5
    
    # Final check on metrics
    assert agent.metrics["aesthetic_delta"] == 0.14
    assert agent.metrics["cognitive_load_index"] > 0

if __name__ == "__main__":
    asyncio.run(test_architectural_workflow_logic())
