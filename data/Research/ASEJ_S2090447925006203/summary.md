# A Multistage Framework for AI-Assisted Architectural Design
**ASEJ Reference**: S2090447925006203
**Journal**: Ain Shams Engineering Journal
**Date**: January 2026

## Summary
This paper establishes a "Multistage Framework" for architectural GenAI, focusing on bridging the gap between flat prompts and high-fidelity 3D documentation. It identifies a **7-phase design workflow** as the optimal path for agent-human collaboration.

## The 7-Phase GAAD Workflow
1.  **Phase 1: Pre-design Analysis**: Automated gathering of site data, zoning, and project constraints.
2.  **Phase 2: Generative Concept Ideation**: Fast exploration of metaphorical or formal concepts (2D Image generation).
3.  **Phase 3: Schematic Synthesis**: Mapping 2D concepts into 3D massing/voxels.
4.  **Phase 4: Design Development**: Iterative refinement of facades and spatial layouts using GAN refinement.
5.  **Phase 5: Technical Integration**: Mapping structural components and material palettes.
6.  **Phase 6: Adversarial Review**: A dedicated **Critic Agent** audits the design for code compliance and aesthetic coherence ($14\%$ Delta check).
7.  **Phase 7: Final Production**: Generating BIM documentation and high-quality renders.

## Implementation Details for PyAgent
- **Agent**: `ArchitecturalDesignAgent`
- **Logic**: 
    - `DesignPhaseManager`: Moves the agent through the 7-phase state machine.
    - `CriticLoop`: Implements Ph6 (Adversarial Review) before allowing output to Ph7.

## References
- [ScienceDirect S2090447925006203](https://www.sciencedirect.com/science/article/pii/S2090447925006203)
