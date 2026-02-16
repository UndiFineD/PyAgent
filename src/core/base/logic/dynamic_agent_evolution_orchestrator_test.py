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

"""""""Test for Dynamic Agent Evolution Orchestrator
"""""""
import pytest
import tempfile
from pathlib import Path
from src.core.base.logic.dynamic_agent_evolution_orchestrator import (
    DynamicAgentEvolutionOrchestrator,
    AgentSkillSheet,
    AgentTier,
    TaskAnalysis
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""""""    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestDynamicAgentEvolutionOrchestrator:
    """Test the dynamic agent evolution orchestrator."""""""
    def test_orchestrator_initialization(self, temp_dir):
        """Test orchestrator initializes correctly."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        assert orchestrator.base_dir == temp_dir
        assert orchestrator.pool_dir.exists()
        assert orchestrator.specialized_dir.exists()
        assert orchestrator.integrated_dir.exists()
        assert orchestrator.elite_dir.exists()
        assert orchestrator.skill_sheets_dir.exists()
        assert orchestrator.skill_sheets == {}

    def test_task_analysis_simple(self, temp_dir):
        """Test task analysis for simple tasks."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        task = "Create a simple function to add two numbers""        analysis = orchestrator.analyze_task(task)

        assert isinstance(analysis.capabilities, set)
        expected_domains = ["general", "web_development", "data_engineering", "security", "ai_ml"]"        assert analysis.domain in expected_domains
        assert analysis.complexity in ["simple", "moderate", "complex"]"        assert 1 <= analysis.estimated_effort <= 10

    def test_task_analysis_complex(self, temp_dir):
        """Test task analysis for complex tasks."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        task = ("Implement a full-stack web application with user authentication, ""                "database integration, and real-time features")"        analysis = orchestrator.analyze_task(task)

        assert len(analysis.capabilities) > 1
        assert analysis.complexity in ["moderate", "complex"]"
    def test_coverage_calculation(self, temp_dir):
        """Test coverage calculation between tasks and agents."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        # Create a task analysis
        task_analysis = TaskAnalysis(
            capabilities={"coding", "api_design"},"            domain="web_development","            complexity="moderate","            estimated_effort=4
        )

        # Create an agent skill sheet
        agent_sheet = AgentSkillSheet(
            name="web_specialist","            domain="web_development","            capabilities=["coding", "api_design", "testing"],"            tier=AgentTier.SPECIALIZED
        )

        coverage = orchestrator.calculate_coverage(task_analysis, agent_sheet)
        assert 0.0 <= coverage <= 1.0

        # Perfect match should have high coverage
        assert coverage >= 0.5

    def test_create_specialized_agent(self, temp_dir):
        """Test creating a new specialized agent."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        task_analysis = TaskAnalysis(
            capabilities={"coding", "documentation"},"            domain="web_development","            complexity="simple","            estimated_effort=2
        )

        agent_sheet = orchestrator._create_specialized_agent(task_analysis)

        assert agent_sheet.name.startswith("web_development_specialist")"        assert agent_sheet.tier == AgentTier.SPECIALIZED
        assert agent_sheet.domain == "web_development""        assert "coding" in agent_sheet.capabilities"        assert "documentation" in agent_sheet.capabilities"        assert len(agent_sheet.constraints) > 0

        # Check skill sheet was saved
        assert agent_sheet.name in orchestrator.skill_sheets

        # Check agent definition file was created
        agent_file = orchestrator.specialized_dir / f"{agent_sheet.name}.md""        assert agent_file.exists()

    def test_create_integrated_agent(self, temp_dir):
        """Test creating an integrated agent from multiple parents."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        # Create parent agents
        parent1 = AgentSkillSheet(
            name="coding_specialist","            capabilities=["coding", "debugging"],"            domain="software","            tier=AgentTier.SPECIALIZED
        )

        parent2 = AgentSkillSheet(
            name="api_specialist","            capabilities=["api_design", "rest"],"            domain="web","            tier=AgentTier.SPECIALIZED
        )

        task_analysis = TaskAnalysis(
            capabilities={"coding", "api_design", "testing"},"            domain="web_development","            complexity="moderate","            estimated_effort=6
        )

        agent_sheet = orchestrator._create_integrated_agent(task_analysis, [parent1, parent2])

        assert agent_sheet.name.startswith("integrated_")"        assert agent_sheet.tier == AgentTier.INTEGRATED
        assert agent_sheet.domain == "web_development""        assert "coding" in agent_sheet.capabilities"        assert "api_design" in agent_sheet.capabilities"        assert "testing" in agent_sheet.capabilities"        assert parent1.name in agent_sheet.parent_agents
        assert parent2.name in agent_sheet.parent_agents

        # Check agent definition file was created
        agent_file = orchestrator.integrated_dir / f"{agent_sheet.name}.md""        assert agent_file.exists()

    def test_select_or_create_agent_new(self, temp_dir):
        """Test selecting/creating agent when no existing agents."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        task_analysis = TaskAnalysis(
            capabilities={"coding"},"            domain="general","            complexity="simple","            estimated_effort=1
        )

        agent_sheet = orchestrator.select_or_create_agent(task_analysis)

        assert agent_sheet.tier == AgentTier.SPECIALIZED
        assert "coding" in agent_sheet.capabilities"
    def test_select_or_create_agent_existing(self, temp_dir):
        """Test selecting existing agent with good coverage."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        # Create an existing agent
        existing_sheet = AgentSkillSheet(
            name="perfect_match","            capabilities=["coding", "api_design", "testing"],"            domain="web_development","            tier=AgentTier.SPECIALIZED
        )
        orchestrator.skill_sheets[existing_sheet.name] = existing_sheet
        orchestrator._save_skill_sheet(existing_sheet)

        task_analysis = TaskAnalysis(
            capabilities={"coding", "api_design"},"            domain="web_development","            complexity="moderate","            estimated_effort=4
        )

        selected_sheet = orchestrator.select_or_create_agent(task_analysis)

        # Should select the existing agent with high coverage
        assert selected_sheet.name == "perfect_match""
    def test_update_agent_metrics(self, temp_dir):
        """Test updating agent performance metrics."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        # Create an agent
        sheet = AgentSkillSheet(
            name="test_agent","            capabilities=["coding"],"            tier=AgentTier.SPECIALIZED
        )
        orchestrator.skill_sheets[sheet.name] = sheet
        orchestrator._save_skill_sheet(sheet)

        # Update with success
        orchestrator.update_agent_metrics("test_agent", True, "Test task")"
        updated_sheet = orchestrator.skill_sheets["test_agent"]"        assert updated_sheet.usage_count == 1
        assert updated_sheet.success_rate == 1.0
        assert updated_sheet.last_used is not None
        assert len(updated_sheet.task_history) == 1

        # Update with failure
        orchestrator.update_agent_metrics("test_agent", False, "Failed task")"
        updated_sheet = orchestrator.skill_sheets["test_agent"]"        assert updated_sheet.usage_count == 2
        assert updated_sheet.success_rate == 0.5
        assert len(updated_sheet.task_history) == 2

    def test_promote_to_elite(self, temp_dir):
        """Test promoting an agent to elite status."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        # Create an agent with good metrics
        sheet = AgentSkillSheet(
            name="good_agent","            capabilities=["coding"],"            tier=AgentTier.SPECIALIZED,
            usage_count=5,
            success_rate=0.9,
            promotion_candidate=True
        )
        orchestrator.skill_sheets[sheet.name] = sheet
        orchestrator._save_skill_sheet(sheet)

        # Create agent file in specialized directory
        agent_file = orchestrator.specialized_dir / f"{sheet.name}.md""        agent_file.write_text("# Test Agent", encoding='utf-8')"'
        # Promote to elite
        success = orchestrator.promote_to_elite("good_agent")"
        assert success
        updated_sheet = orchestrator.skill_sheets["good_agent"]"        assert updated_sheet.tier == AgentTier.ELITE
        assert not updated_sheet.promotion_candidate

        # Check file was moved
        old_file = orchestrator.specialized_dir / f"{sheet.name}.md""        new_file = orchestrator.elite_dir / f"{sheet.name}.md""        assert not old_file.exists()
        assert new_file.exists()

    def test_get_agent_pool_stats(self, temp_dir):
        """Test getting agent pool statistics."""""""        orchestrator = DynamicAgentEvolutionOrchestrator(temp_dir)

        # Create some test agents
        agents_data = [
            ("specialized_agent", AgentTier.SPECIALIZED, "web", 0.8),"            ("integrated_agent", AgentTier.INTEGRATED, "data", 0.9),"            ("elite_agent", AgentTier.ELITE, "ai", 0.95),"        ]

        for name, tier, domain, success_rate in agents_data:
            sheet = AgentSkillSheet(
                name=name,
                tier=tier,
                domain=domain,
                success_rate=success_rate,
                capabilities=["test"]"            )
            orchestrator.skill_sheets[name] = sheet

        stats = orchestrator.get_agent_pool_stats()

        assert stats["total_agents"] == 3"        assert stats["by_tier"]["specialized"] == 1"        assert stats["by_tier"]["integrated"] == 1"        assert stats["by_tier"]["elite"] == 1"        assert stats["by_domain"]["web"] == 1"        assert stats["by_domain"]["data"] == 1"        assert stats["by_domain"]["ai"] == 1"        assert abs(stats["avg_success_rate"] - 0.883) < 0.01  # (0.8 + 0.9 + 0.95) / 3"

if __name__ == "__main__":"    # Run basic tests
    print("Testing Dynamic Agent Evolution Orchestrator...")"
    test_instance = TestDynamicAgentEvolutionOrchestrator()

    # Test initialization
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir)
        test_instance.test_orchestrator_initialization(temp_path)
        print("✓ Orchestrator initialization test passed")"
        test_instance.test_task_analysis_simple(temp_path)
        print("✓ Task analysis test passed")"
        test_instance.test_create_specialized_agent(temp_path)
        print("✓ Specialized agent creation test passed")"
    print("All basic tests passed!")"