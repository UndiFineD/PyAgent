# Copyright 2026 PyAgent Authors
# ArchitecturalDesignAgent: Implementation of Multi-Stage Architectural GenAI Framework
# Based on research: arXiv:2601.10696 and ScienceDirect S2090447925006203 (Jiang et al., 2026)

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import json
import asyncio
from typing import Any, Dict, List, Optional
from enum import Enum
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION

class DesignPhase(Enum):
    PRE_DESIGN = "Pre-design/Conceptualization"
    SCHEMATIC = "Schematic Design"
    DEVELOPMENT = "Design Development"
    PRODUCTION = "Production/Detailing"

class ArchitecturalDesignAgent(BaseAgent):
    """
    Agent specializing in hierarchical architectural design workflows.
    Implements the 4-stage framework identified in 2026 empirical studies
    regarding cognitive load reduction and performance enhancement in AI-aided design.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.current_phase = DesignPhase.PRE_DESIGN
        self.design_state: Dict[str, Any] = {
            "requirements": {},
            "concepts": [],
            "layouts": [],
            "visualizations": [],
            "feedback_history": []
        }
        self._system_prompt = (
            "You are the Architectural Design Agent, specializing in the multi-stage "
            "transformation of project requirements into structured architectural designs. "
            "You follow a hierarchical reasoning approach: first defining conceptual spatial "
            "logic, then schematic structures, and finally detailed technical specifications."
        )

    @as_tool
    async def process_requirements(self, brief: str) -> Dict[str, Any]:
        """
        Phase 1: Pre-design. Extracts site conditions and functional requirements.
        Reduces initial cognitive load by automating constraints identification.
        """
        prompt = f"Extract architectural requirements and constraints from this brief: {brief}"
        requirements = await self.run_subagent("extracting requirements", prompt)
        self.design_state["requirements"] = requirements
        self.current_phase = DesignPhase.PRE_DESIGN
        return {"phase": self.current_phase.value, "requirements": requirements}

    @as_tool
    async def generate_spatial_concept(self, refinement: Optional[str] = None) -> Dict[str, Any]:
        """
        Phase 2: Conceptualization. Generates spatial logic and massing options.
        Leverages hierarchical reasoning to maintain global design coherence.
        """
        if not self.design_state["requirements"]:
            return {"error": "Requirements must be processed first."}
            
        prompt = (
            f"Based on requirements: {self.design_state['requirements']}, "
            f"generate 3 spatial concepts. Refinement: {refinement or 'None'}. "
            "Focus on circulation, sun orientation, and volume distribution."
        )
        concepts = await self.run_subagent("generating spatial concepts", prompt)
        self.design_state["concepts"].append(concepts)
        self.current_phase = DesignPhase.SCHEMATIC
        return {"phase": self.current_phase.value, "concepts": concepts}

    @as_tool
    async def coordinate_visual_verification(self, concept_index: int) -> Dict[str, Any]:
        """
        Phase 3: Design Development. Simulates agent coordination for visual output.
        In 2026 frameworks, this involves verifying Diffusion outputs against JSON specs.
        """
        concept = self.design_state["concepts"][concept_index]
        # Simulate interaction with a VisionAgent/DiffusionAgent
        verification_prompt = (
            f"Analyze if the concept '{concept}' meets the requirement "
            f"'{self.design_state['requirements']}'. Provide visual prompting strategy."
        )
        strategy = await self.run_subagent("coordinating visual verification", verification_prompt)
        self.design_state["visualizations"].append({"concept": concept, "strategy": strategy})
        self.current_phase = DesignPhase.DEVELOPMENT
        return {"phase": self.current_phase.value, "verification_strategy": strategy}

    @as_tool
    async def finalize_production_specs(self) -> Dict[str, Any]:
        """
        Phase 4: Production. Generates technical specifications and material schedules.
        Final output stage of the integrated GenAI framework.
        """
        if self.current_phase != DesignPhase.DEVELOPMENT:
             logging.warning("Advancing to Production phase without full development.")
             
        prompt = f"Generate production specs for the following design state: {json.dumps(self.design_state)}"
        specs = await self.run_subagent("finalizing production specs", prompt)
        self.current_phase = DesignPhase.PRODUCTION
        return {"phase": self.current_phase.value, "specs": specs}

    def get_acceleration_metrics(self) -> Dict[str, Any]:
        """
        Returns simulated inference optimization metrics.
        In 2026, agents monitor KV cache efficiency and JCT (Job Completion Time).
        """
        # Placeholders for requested technical concepts
        return {
            "kv_cache_efficiency": "94.2%",  # High reuse due to hierarchical design tokens
            "hierarchical_depth": 4,
            "streaming_status": "enabled",
            "coordination_overhead": "low"
        }
