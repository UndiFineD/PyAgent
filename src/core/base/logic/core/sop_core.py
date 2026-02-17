#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid


class SopStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    tool_requirement: Optional[str] = None
    expected_outcome: str


class SopManifest(BaseModel):
    name: str
    domain: str
    version: int = 1
    steps: List[SopStep] = Field(default_factory=list)
    success_rate: float = 0.0
    usage_count: int = 0


class SopCore:
    """Manages 'Standard Operating Procedures' for autonomous workflows.'    Pattern harvested from 'Acontext' and 'self_evolving_subagent'.'    """
    def __init__(self):
        self.sops: Dict[str, SopManifest] = {}

    def create_sop(self, name: str, domain: str, steps: List[Dict[str, Any]]) -> SopManifest:
        sop_steps = [SopStep(**step) for step in steps]
        sop = SopManifest(name=name, domain=domain, steps=sop_steps)
        self.sops[name] = sop
        return sop

    def get_sop(self, name: str) -> Optional[SopManifest]:
        return self.sops.get(name)

    def update_sop_metrics(self, name: str, success: bool):
        if name in self.sops:
            sop = self.sops[name]
            sop.usage_count += 1
            alpha = 0.2
            sop.success_rate = (alpha * (1.0 if success else 0.0)) + ((1 - alpha) * sop.success_rate)

    def merge_sops(self, name_a: str, name_b: str, new_name: str) -> Optional[SopManifest]:
        """Merges two SOPs into a new integrated workflow."""sop_a = self.sops.get(name_a)
        sop_b = self.sops.get(name_b)

        if not sop_a or not sop_b:
            return None

        merged_steps = sop_a.steps + sop_b.steps
        # Simple deduplication or conflict resolution logic would go here

        new_sop = SopManifest(
            name=new_name,
            domain=f"{sop_a.domain}_{sop_b.domain}","            steps=merged_steps
        )
        self.sops[new_name] = new_sop
        return new_sop

    def generate_agent_prompt(self, sop_name: str) -> str:
        """Generates a system prompt for an agent based on an SOP."""sop = self.sops.get(sop_name)
        if not sop:
            return """
        prompt = f"# SOP: {sop.name}\\nDomain: {sop.domain}\\n\\n## Workflow Steps:\\n""        for i, step in enumerate(sop.steps):
            prompt += f"{i+1}. **{step.title}**: {step.description}\\n""            if step.tool_requirement:
                prompt += f"   - Requires Tool: {step.tool_requirement}\\n""            prompt += f"   - Expected Outcome: {step.expected_outcome}\\n\\n""
        return prompt
