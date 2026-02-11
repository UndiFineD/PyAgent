#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test for MAESTRO Security Analyzer
"""

import pytest
import tempfile
from pathlib import Path
from src.core.base.logic.maestro_security_analyzer import (
    MAESTROSecurityAnalyzer,
    AgentNode
)
from src.core.base.logic.dynamic_agent_evolution_orchestrator import AgentTier


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestMAESTROSecurityAnalyzer:
    """Test the MAESTRO security analyzer."""

    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly."""
        analyzer = MAESTROSecurityAnalyzer()

        assert analyzer.base_dir == Path(".")
        assert isinstance(analyzer.threat_database, dict)
        assert "agent_ecosystem" in analyzer.threat_database
        assert "security_compliance" in analyzer.threat_database

    def test_agent_node_creation(self):
        """Test creating agent nodes."""
        agent = AgentNode(
            name="test_agent",
            tier=AgentTier.SPECIALIZED,
            capabilities=["coding", "testing"],
            tools=["pytest", "black"],
            lineage=["base_agent"],
            success_rate=0.9,
            usage_count=10
        )

        assert agent.name == "test_agent"
        assert agent.tier == AgentTier.SPECIALIZED
        assert "coding" in agent.capabilities
        assert "pytest" in agent.tools
        assert "base_agent" in agent.lineage
        assert agent.success_rate == 0.9
        assert agent.usage_count == 10

    def test_system_overview_analysis(self):
        """Test system overview analysis."""
        analyzer = MAESTROSecurityAnalyzer()

        agents = [
            AgentNode("agent1", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.8, 5),
            AgentNode("agent2", AgentTier.INTEGRATED, ["cap1", "cap2"], [], ["agent1"], 0.9, 10),
            AgentNode("agent3", AgentTier.ELITE, ["cap2", "cap3"], [], ["agent2"], 0.95, 20)
        ]

        overview = analyzer._analyze_system_overview(agents)

        assert overview["total_agents"] == 3
        assert overview["agent_distribution"]["specialized"] == 1
        assert overview["agent_distribution"]["integrated"] == 1
        assert overview["agent_distribution"]["elite"] == 1
        assert overview["capability_coverage"]["total_unique_capabilities"] == 3
        assert overview["system_maturity"] == "Established"

    def test_capability_coverage_analysis(self):
        """Test capability coverage analysis."""
        analyzer = MAESTROSecurityAnalyzer()

        agents = [
            AgentNode("agent1", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.8, 5),
            AgentNode("agent2", AgentTier.SPECIALIZED, ["cap1", "cap2"], [], [], 0.9, 10)
        ]

        coverage = analyzer._analyze_capability_coverage(agents)

        assert coverage["total_unique_capabilities"] == 2
        assert "cap1" in coverage["capabilities"]
        assert "cap2" in coverage["capabilities"]
        assert coverage["single_points_of_failure"] == ["cap2"]  # Only agent2 has cap2
        assert coverage["redundancy_level"] == "Low"

    def test_relationship_analysis(self):
        """Test inter-agent relationship analysis."""
        analyzer = MAESTROSecurityAnalyzer()

        agents = [
            AgentNode("parent", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.8, 5),
            AgentNode("child1", AgentTier.INTEGRATED, ["cap2"], [], ["parent"], 0.9, 10),
            AgentNode("child2", AgentTier.INTEGRATED, ["cap3"], [], ["parent"], 0.85, 8),
            AgentNode("child3", AgentTier.INTEGRATED, ["cap4"], [], ["parent"], 0.88, 12)
        ]

        relationships = analyzer._analyze_relationships(agents)

        assert len(relationships["lineage_chains"]) == 3
        assert len(relationships["cascading_failure_risks"]) == 1  # parent has 3 dependents
        assert relationships["cascading_failure_risks"][0]["high_dependency_agent"] == "parent"
        assert relationships["cascading_failure_risks"][0]["dependent_count"] == 3

    def test_system_maturity_assessment(self):
        """Test system maturity assessment."""
        analyzer = MAESTROSecurityAnalyzer()

        # Early development
        early_agents = [AgentNode("agent1", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.5, 1)]
        assert analyzer._assess_system_maturity(early_agents) == "Early Development"

        # Mature system
        mature_agents = [
            AgentNode("agent1", AgentTier.ELITE, ["cap1"], [], [], 0.95, 20),
            AgentNode("agent2", AgentTier.ELITE, ["cap2"], [], [], 0.92, 15),
            AgentNode("agent3", AgentTier.ELITE, ["cap3"], [], [], 0.96, 25)
        ]
        assert analyzer._assess_system_maturity(mature_agents) == "Mature"

    def test_layer_analysis(self):
        """Test MAESTRO layer analysis."""
        analyzer = MAESTROSecurityAnalyzer()

        agents = [AgentNode("test_agent", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.8, 5)]

        layer_assessment = analyzer._analyze_layer("agent_ecosystem", "Agent Ecosystem", agents)

        assert "layer_description" in layer_assessment
        assert "relevant_threats" in layer_assessment
        assert "risk_assessment" in layer_assessment
        assert "agent_relevance" in layer_assessment
        assert len(layer_assessment["relevant_threats"]) > 0

    def test_threat_assessment(self):
        """Test individual threat assessment."""
        analyzer = MAESTROSecurityAnalyzer()

        threat_data = {
            "threat": "Test Threat",
            "description": "A test security threat",
            "impact": "High",
            "likelihood": "Medium",
            "mitigations": ["Mitigation 1", "Mitigation 2"]
        }

        agents = [AgentNode("agent1", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.8, 5)]

        assessment = analyzer._assess_threat(threat_data, agents)

        assert assessment["threat"] == "Test Threat"
        assert assessment["description"] == "A test security threat"
        assert assessment["base_impact"] == "High"
        assert "adjusted_likelihood" in assessment
        assert "risk_level" in assessment
        assert len(assessment["mitigation_suggestions"]) == 2

    def test_risk_level_calculation(self):
        """Test risk level calculation from impact and likelihood."""
        analyzer = MAESTROSecurityAnalyzer()

        # Critical combinations
        assert analyzer._calculate_risk_level("Critical", "High") == "Critical"
        assert analyzer._calculate_risk_level("High", "High") == "Critical"

        # High risk combinations
        assert analyzer._calculate_risk_level("Critical", "Low") == "High"
        assert analyzer._calculate_risk_level("High", "Medium") == "High"

        # Medium risk combinations
        assert analyzer._calculate_risk_level("High", "Low") == "Medium"
        assert analyzer._calculate_risk_level("Medium", "High") == "High"

        # Low risk combinations
        assert analyzer._calculate_risk_level("Low", "Low") == "Low"
        assert analyzer._calculate_risk_level("Medium", "Low") == "Low"

    def test_overall_risk_calculation(self):
        """Test overall system risk calculation."""
        analyzer = MAESTROSecurityAnalyzer()

        layer_assessments = {
            "Layer 1": {"risk_assessment": "Low"},
            "Layer 2": {"risk_assessment": "Medium"},
            "Layer 3": {"risk_assessment": "High"},
            "Layer 4": {"risk_assessment": "Critical"}
        }

        overall_risk = analyzer._calculate_overall_risk(layer_assessments)

        assert overall_risk["overall_risk_level"] == "Critical"
        assert overall_risk["critical_layers_count"] == 1
        assert overall_risk["high_risk_layers_count"] == 1
        assert overall_risk["total_layers_assessed"] == 4

    def test_recommendations_generation(self):
        """Test security recommendations generation."""
        analyzer = MAESTROSecurityAnalyzer()

        # Create agents with single points of failure
        agents = [
            AgentNode("agent1", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.8, 5),
            AgentNode("agent2", AgentTier.SPECIALIZED, ["cap2"], [], [], 0.9, 10)  # cap2 is single point
        ]

        layer_assessments = {
            "Agent Ecosystem": {"risk_assessment": "High"},
            "Security and Compliance": {"risk_assessment": "Medium"}
        }

        recommendations = analyzer._generate_recommendations(layer_assessments, agents)

        assert len(recommendations) > 0
        assert any("single points of failure" in rec for rec in recommendations)
        assert any("Agent Ecosystem" in rec for rec in recommendations)

    def test_full_system_analysis(self):
        """Test complete multi-agent system analysis."""
        analyzer = MAESTROSecurityAnalyzer()

        agents = [
            AgentNode("web_agent", AgentTier.SPECIALIZED, ["web_scraping"], ["requests"], [], 0.85, 15),
            AgentNode("data_agent", AgentTier.INTEGRATED, ["data_processing", "web_scraping"], ["pandas"], ["web_agent"], 0.92, 8),
            AgentNode("security_agent", AgentTier.ELITE, ["security_analysis", "data_processing"], ["scanner"], ["data_agent"], 0.96, 25)
        ]

        report = analyzer.analyze_multi_agent_system(agents)

        # Verify report structure
        assert "maestro_framework" in report
        assert "system_overview" in report
        assert "layer_assessments" in report
        assert "overall_risk_assessment" in report
        assert "recommendations" in report

        # Verify system overview
        overview = report["system_overview"]
        assert overview["total_agents"] == 3
        assert overview["system_maturity"] == "Mature"

        # Verify layer assessments
        assert len(report["layer_assessments"]) == 7  # All MAESTRO layers

        # Verify overall risk
        risk = report["overall_risk_assessment"]
        assert "overall_risk_level" in risk
        assert "critical_layers_count" in risk
        assert "high_risk_layers_count" in risk

        # Verify recommendations
        assert isinstance(report["recommendations"], list)
        assert len(report["recommendations"]) > 0

    def test_report_export(self, temp_dir):
        """Test report export functionality."""
        analyzer = MAESTROSecurityAnalyzer()

        agents = [AgentNode("test_agent", AgentTier.SPECIALIZED, ["cap1"], [], [], 0.8, 5)]
        report = analyzer.analyze_multi_agent_system(agents)

        # Test JSON export
        json_path = temp_dir / "test_report.json"
        analyzer.export_report(report, json_path)
        assert json_path.exists()

        # Test markdown export
        md_path = temp_dir / "test_report.md"
        analyzer.generate_markdown_report(report, md_path)
        assert md_path.exists()

        # Verify markdown content
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "# MAESTRO Security Analysis Report" in content
            assert "## System Overview" in content
            assert "## Layer Assessments" in content
            assert "## Overall Risk Assessment" in content
            assert "## Security Recommendations" in content


if __name__ == "__main__":
    # Run basic tests
    print("Testing MAESTRO Security Analyzer...")

    test_instance = TestMAESTROSecurityAnalyzer()

    # Test initialization
    test_instance.test_analyzer_initialization()
    print("✓ Analyzer initialization test passed")

    # Test agent node creation
    test_instance.test_agent_node_creation()
    print("✓ Agent node creation test passed")

    # Test system analysis
    test_instance.test_full_system_analysis()
    print("✓ Full system analysis test passed")

    print("All basic tests passed!")
