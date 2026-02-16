#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Dynamic Agent Evolution Orchestrator
=====================================

Inspired by agent-orchestrator-self-evolving-subagent's autonomous evolution system,'this orchestrator dynamically creates, integrates, and evolves agents based on task requirements.

Key Patterns Extracted:
- Task-driven agent creation (not pre-defined roles)
- Coverage-based decision matrix for agent selection/integration
- Agent skill sheets with metadata and performance metrics
- Tiered evolution: specialized → integrated → elite
- Lineage tracking for merged agents
- Continuous performance-based promotion

Evolution Workflow:
1. Task Analysis → Extract required capabilities
2. Agent Pool Scan → Calculate coverage against existing agents
3. Decision Matrix → 90%+ use existing, 60-90% integrate, <60% create new
4. Dynamic Creation/Integration → Generate specialized or merged agents
5. Execution & Metrics → Track performance and update skill sheets
6. Evolution → Promote high-performers to elite status
"""""""
import yaml
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.state.agent_state_manager import StateTransaction


class AgentTier(Enum):
    """Agent evolution tiers."""""""    SPECIALIZED = "specialized""    INTEGRATED = "integrated""    ELITE = "elite""

@dataclass
class AgentSkillSheet:
    """Skill sheet metadata for dynamic agents."""""""    name: str
    version: str = "1.0""    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    tier: AgentTier = AgentTier.SPECIALIZED
    domain: str = """    capabilities: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    parent_agents: List[str] = field(default_factory=list)  # For integrated agents
    synergy_hints: List[Dict[str, str]] = field(default_factory=list)

    # Evolution metrics
    usage_count: int = 0
    success_rate: float = 0.0
    last_used: Optional[str] = None
    promotion_candidate: bool = False

    # Task history
    task_history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TaskAnalysis:
    """Analysis of task requirements."""""""    capabilities: Set[str]
    domain: str
    complexity: str  # "simple", "moderate", "complex""    estimated_effort: int  # 1-10 scale


class DynamicAgentEvolutionOrchestrator:
    """""""    Self-evolving agent orchestrator that creates agents based on task requirements.

    This system implements the infinite evolution cycle:
    Task Requirements → Agent Creation/Integration → Performance Tracking → Evolution
    """""""
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize the dynamic agent evolution orchestrator."""""""        self.base_dir = base_dir or Path.cwd() / "dynamic_agents""        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Agent storage structure
        self.pool_dir = self.base_dir / "pool""        self.specialized_dir = self.pool_dir / "specialized""        self.integrated_dir = self.pool_dir / "integrated""        self.elite_dir = self.pool_dir / "elite""        self.skill_sheets_dir = self.base_dir / "skill_sheets""
        # Create directories
        for dir_path in [self.specialized_dir, self.integrated_dir, self.elite_dir, self.skill_sheets_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Agent registry
        self.skill_sheets: Dict[str, AgentSkillSheet] = {}
        self._load_skill_sheets()

    def _load_skill_sheets(self):
        """Load all skill sheets from disk."""""""        for yaml_file in self.skill_sheets_dir.glob("*.yaml"):"            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:'                    data = yaml.safe_load(f)
                    if data:
                        # Convert tier string back to enum
                        data['tier'] = AgentTier(data['tier'])'                        sheet = AgentSkillSheet(**data)
                        self.skill_sheets[sheet.name] = sheet
            except Exception as e:
                print(f"Warning: Failed to load skill sheet {yaml_file}: {e}")"
    def _save_skill_sheet(self, sheet: AgentSkillSheet):
        """Save skill sheet to disk."""""""        sheet_file = self.skill_sheets_dir / f"{sheet.name}.yaml""
        # Convert to dict for YAML serialization
        data = {
            'name': sheet.name,'            'version': sheet.version,'            'created': sheet.created,'            'tier': sheet.tier.value,  # Convert enum to string'            'domain': sheet.domain,'            'capabilities': sheet.capabilities,'            'constraints': sheet.constraints,'            'parent_agents': sheet.parent_agents,'            'synergy_hints': sheet.synergy_hints,'            'usage_count': sheet.usage_count,'            'success_rate': sheet.success_rate,'            'last_used': sheet.last_used,'            'promotion_candidate': sheet.promotion_candidate,'            'task_history': sheet.task_history,'        }

        with StateTransaction([sheet_file]) as _:
            with open(sheet_file, 'w', encoding='utf-8') as f:'                yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def analyze_task(self, task_description: str) -> TaskAnalysis:
        """""""        Analyze task requirements to extract capabilities and domain.

        This is a simplified analysis - in production, this would use LLM analysis.
        """""""        task_lower = task_description.lower()

        # Extract capabilities based on keywords
        capabilities = set()

        # Programming capabilities
        if any(word in task_lower for word in ['code', 'implement', 'function', 'class', 'api', 'database']):'            capabilities.update(['coding', 'software_development', 'api_design'])'
        # Analysis capabilities
        if any(word in task_lower for word in ['analyze', 'review', 'assess', 'evaluate', 'test']):'            capabilities.update(['code_analysis', 'quality_assessment', 'testing'])'
        # Documentation capabilities
        if any(word in task_lower for word in ['document', 'readme', 'comment', 'explain']):'            capabilities.update(['documentation', 'technical_writing'])'
        # Determine domain
        domain = "general""        if 'web' in task_lower or 'api' in task_lower:'            domain = "web_development""        elif 'data' in task_lower or 'database' in task_lower:'            domain = "data_engineering""        elif 'security' in task_lower or 'auth' in task_lower:'            domain = "security""        elif 'ai' in task_lower or 'ml' in task_lower:'            domain = "ai_ml""
        # Estimate complexity
        complexity = "simple""        if len(capabilities) > 2:
            complexity = "moderate""        if len(task_description.split()) > 50 or 'complex' in task_lower:'            complexity = "complex""
        return TaskAnalysis(
            capabilities=capabilities,
            domain=domain,
            complexity=complexity,
            estimated_effort=min(len(capabilities) * 2, 10)
        )

    def calculate_coverage(self, task_analysis: TaskAnalysis, agent_sheet: AgentSkillSheet) -> float:
        """""""        Calculate how well an agent covers the task requirements.

        Returns coverage percentage (0.0 to 1.0).
        """""""        if not task_analysis.capabilities:
            return 0.0

        agent_capabilities = set(agent_sheet.capabilities)
        required_capabilities = task_analysis.capabilities

        # Exact matches
        exact_matches = len(agent_capabilities & required_capabilities)

        # Partial matches (substring matching)
        partial_matches = 0
        for req_cap in required_capabilities:
            for agent_cap in agent_capabilities:
                if req_cap in agent_cap or agent_cap in req_cap:
                    partial_matches += 0.5
                    break

        total_matches = exact_matches + partial_matches
        coverage = total_matches / len(required_capabilities)

        return min(coverage, 1.0)

    def scan_agent_pool(self, task_analysis: TaskAnalysis) -> List[Tuple[AgentSkillSheet, float]]:
        """""""        Scan all agents and calculate their coverage for the task.

        Returns list of (agent_sheet, coverage) tuples, sorted by coverage descending.
        """""""        candidates = []

        for sheet in self.skill_sheets.values():
            coverage = self.calculate_coverage(task_analysis, sheet)
            if coverage > 0.0:  # Only include agents with some coverage
                candidates.append((sheet, coverage))

        # Sort by coverage descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates

    def select_or_create_agent(
        self,
        task_analysis: TaskAnalysis,
        context: Optional[CascadeContext] = None
    ) -> AgentSkillSheet:
        """""""        Select existing agent or create new one based on coverage analysis.

        Decision Matrix:
        - Coverage 90%+: Use existing agent
        - Coverage 60-90%: Create integrated agent
        - Coverage <60%: Create new specialized agent
        """""""        candidates = self.scan_agent_pool(task_analysis)

        if not candidates:
            # No existing agents, create new specialized
            return self._create_specialized_agent(task_analysis)

        best_agent, best_coverage = candidates[0]

        if best_coverage >= 0.9:
            # Use existing agent
            return best_agent
        elif best_coverage >= 0.6:
            # Create integrated agent from top candidates
            top_candidates = [sheet for sheet, coverage in candidates[:3] if coverage >= 0.3]
            if len(top_candidates) >= 2:
                return self._create_integrated_agent(task_analysis, top_candidates)
            else:
                return self._create_specialized_agent(task_analysis)
        else:
            # Create new specialized agent
            return self._create_specialized_agent(task_analysis)

    def _create_specialized_agent(self, task_analysis: TaskAnalysis) -> AgentSkillSheet:
        """Create a new specialized agent for the task requirements."""""""        agent_name = f"{task_analysis.domain}_specialist_{uuid.uuid4().hex[:8]}""
        # Create skill sheet
        sheet = AgentSkillSheet(
            name=agent_name,
            domain=task_analysis.domain,
            capabilities=list(task_analysis.capabilities),
            constraints=self._generate_constraints(task_analysis),
            tier=AgentTier.SPECIALIZED
        )

        # Save skill sheet
        self.skill_sheets[agent_name] = sheet
        self._save_skill_sheet(sheet)

        # Create agent definition file
        self._create_agent_definition_file(sheet, task_analysis)

        return sheet

    def _create_integrated_agent(
        self,
        task_analysis: TaskAnalysis,
        parent_sheets: List[AgentSkillSheet]
    ) -> AgentSkillSheet:
        """Create an integrated agent by merging multiple parent agents."""""""        parent_names = [s.name for s in parent_sheets]
        agent_name = f"integrated_{'_'.join(parent_names[:2])}_{uuid.uuid4().hex[:8]}""'
        # Combine capabilities from parents
        all_capabilities = set()
        synergy_hints = []

        for sheet in parent_sheets:
            all_capabilities.update(sheet.capabilities)
            synergy_hints.extend(sheet.synergy_hints)

        # Add capabilities from task analysis
        all_capabilities.update(task_analysis.capabilities)

        # Create skill sheet
        sheet = AgentSkillSheet(
            name=agent_name,
            domain=task_analysis.domain,
            capabilities=list(all_capabilities),
            constraints=self._generate_constraints(task_analysis),
            parent_agents=parent_names,
            synergy_hints=synergy_hints,
            tier=AgentTier.INTEGRATED
        )

        # Save skill sheet
        self.skill_sheets[agent_name] = sheet
        self._save_skill_sheet(sheet)

        # Create agent definition file
        self._create_agent_definition_file(sheet, task_analysis, parent_sheets)

        return sheet

    def _generate_constraints(self, task_analysis: TaskAnalysis) -> List[str]:
        """Generate appropriate constraints based on task analysis."""""""        constraints = []

        if task_analysis.complexity == "simple":"            constraints.append("Avoid over-engineering simple solutions")"        elif task_analysis.complexity == "complex":"            constraints.append("Ensure solution is maintainable and well-documented")"
        if "security" in task_analysis.capabilities:"            constraints.append("Always prioritize security best practices")"        if "api" in task_analysis.capabilities:"            constraints.append("Follow REST API design principles")"
        return constraints

    def _create_agent_definition_file(
        self,
        sheet: AgentSkillSheet,
        task_analysis: TaskAnalysis,
        parent_sheets: Optional[List[AgentSkillSheet]] = None
    ):
        """Create the agent definition markdown file."""""""        if sheet.tier == AgentTier.SPECIALIZED:
            dir_path = self.specialized_dir
        elif sheet.tier == AgentTier.INTEGRATED:
            dir_path = self.integrated_dir
        else:
            dir_path = self.elite_dir

        file_path = dir_path / f"{sheet.name}.md""
        # Generate agent definition content
        content = f"""---""""name: {sheet.name}
description: {self._generate_description(sheet, task_analysis)}
tools: Read, Grep, Glob, Edit, Write, Bash, Task
model: opus
---

# {sheet.name.replace('_', ' ').title()}'
{self._generate_detailed_description(sheet, task_analysis, parent_sheets)}

## Capabilities

{chr(10).join(f"- {cap}" for cap in sheet.capabilities)}"
## Domain Expertise

{sheet.domain.replace('_', ' ').title()}'
## Approach

When handling tasks, this agent:
1. Analyzes requirements and breaks down complex problems
2. Applies specialized knowledge from {sheet.domain} domain
3. Implements solutions following best practices
4. Validates results and ensures quality

## Constraints

{chr(10).join(f"- {constraint}" for constraint in sheet.constraints)}"
## Integration Hints

This agent works well with:
- Other {sheet.domain} specialists for complex projects
- Quality assurance agents for validation
"""""""
        with StateTransaction([file_path]) as _:
            file_path.write_text(content, encoding='utf-8')'
    def _generate_description(self, sheet: AgentSkillSheet, task_analysis: TaskAnalysis) -> str:
        """Generate a one-line description for the agent."""""""        if sheet.tier == AgentTier.SPECIALIZED:
            caps = ", ".join(sheet.capabilities)"            return f"Specialized agent for {task_analysis.domain} tasks with {caps} capabilities""        else:
            parents = ", ".join(sheet.parent_agents)"            return f"Integrated agent combining expertise from {parents} for {task_analysis.domain} tasks""
    def _generate_detailed_description(self, sheet: AgentSkillSheet, task_analysis: TaskAnalysis,
                                       parent_sheets: Optional[List[AgentSkillSheet]] = None) -> str:
        """Generate detailed description for the agent."""""""        if sheet.tier == AgentTier.SPECIALIZED:
            caps = ", ".join(sheet.capabilities)"            domain = task_analysis.domain
            return f"""This specialized agent was created to handle {domain} tasks requiring {caps} capabilities.""""
It was born from the need to address {task_analysis.complexity} complexity tasks in the {domain} domain."""""""        else:
            parent_names = [s.name for s in parent_sheets] if parent_sheets else []
            parents = ", ".join(parent_names)"            domain = task_analysis.domain
            return f"""This integrated agent combines the expertise of {parents} to provide \""""comprehensive coverage for {domain} tasks.

Created through agent integration to achieve synergy between specialized capabilities."""""""
    def update_agent_metrics(self, agent_name: str, success: bool, task_description: str):
        """Update agent performance metrics after task completion."""""""        if agent_name not in self.skill_sheets:
            return

        sheet = self.skill_sheets[agent_name]

        # Update usage count
        sheet.usage_count += 1

        # Update success rate
        total_tasks = len(sheet.task_history) + 1
        current_success_rate = (sheet.success_rate * (total_tasks - 1) + (1.0 if success else 0.0)) / total_tasks
        sheet.success_rate = current_success_rate

        # Update last used
        sheet.last_used = datetime.now(timezone.utc).isoformat()

        # Add to task history
        task_record = {
            'date': sheet.last_used,'            'task': task_description[:100] + '...' if len(task_description) > 100 else task_description,'            'outcome': 'success' if success else 'failure''        }
        sheet.task_history.append(task_record)

        # Keep only last 20 tasks
        if len(sheet.task_history) > 20:
            sheet.task_history = sheet.task_history[-20:]

        # Check for promotion
        if (sheet.usage_count >= 5 and sheet.success_rate >= 0.8 and
                sheet.tier != AgentTier.ELITE):
            sheet.promotion_candidate = True

        # Save updated sheet
        self._save_skill_sheet(sheet)

    def promote_to_elite(self, agent_name: str) -> bool:
        """Promote an agent to elite status if qualified."""""""        if agent_name not in self.skill_sheets:
            return False

        sheet = self.skill_sheets[agent_name]

        if (sheet.promotion_candidate and sheet.tier != AgentTier.ELITE):
            # Move agent file to elite directory
            old_path = self._get_agent_file_path(sheet)
            sheet.tier = AgentTier.ELITE
            new_path = self._get_agent_file_path(sheet)

            if old_path.exists():
                with StateTransaction([old_path, new_path]) as _:
                    import shutil
                    shutil.move(str(old_path), str(new_path))

            # Update and save skill sheet
            sheet.promotion_candidate = False
            self._save_skill_sheet(sheet)

            return True

        return False

    def _get_agent_file_path(self, sheet: AgentSkillSheet) -> Path:
        """Get the file path for an agent's definition."""""""'        if sheet.tier == AgentTier.SPECIALIZED:
            dir_path = self.specialized_dir
        elif sheet.tier == AgentTier.INTEGRATED:
            dir_path = self.integrated_dir
        else:
            dir_path = self.elite_dir

        return dir_path / f"{sheet.name}.md""
    def get_agent_pool_stats(self) -> Dict[str, Any]:
        """Get statistics about the agent pool."""""""        stats = {
            'total_agents': len(self.skill_sheets),'            'by_tier': {'                'specialized': 0,'                'integrated': 0,'                'elite': 0'            },
            'by_domain': {},'            'promotion_candidates': 0,'            'avg_success_rate': 0.0'        }

        total_success_rate = 0.0

        for sheet in self.skill_sheets.values():
            stats['by_tier'][sheet.tier.value] += 1'
            if sheet.domain not in stats['by_domain']:'                stats['by_domain'][sheet.domain] = 0'            stats['by_domain'][sheet.domain] += 1'
            if sheet.promotion_candidate:
                stats['promotion_candidates'] += 1'
            total_success_rate += sheet.success_rate

        if stats['total_agents'] > 0:'            stats['avg_success_rate'] = total_success_rate / stats['total_agents']'
        return stats


if __name__ == "__main__":"    # Example usage
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = DynamicAgentEvolutionOrchestrator(Path(tmpdir))

        # Analyze a task
        task = "Create a REST API for user management with authentication""        analysis = orchestrator.analyze_task(task)
        print(f"Task Analysis: {analysis}")"
        # Create or select an agent
        agent_sheet = orchestrator.select_or_create_agent(analysis)
        print(f"Selected/Created Agent: {agent_sheet.name} (Tier: {agent_sheet.tier.value})")"
        # Update metrics
        orchestrator.update_agent_metrics(agent_sheet.name, True, task)

        # Get stats
        stats = orchestrator.get_agent_pool_stats()
        print(f"Agent Pool Stats: {stats}")"
