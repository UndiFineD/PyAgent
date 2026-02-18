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


"""Tests for security analysis mixin.
try:
    from .logic.agents.swarm.security_analysis_mixin import (
except ImportError:
    from src.logic.agents.swarm.security_analysis_mixin import (

    WorkflowSecurityAnalyzer,
    SecurityAnalysisMixin,
    SecurityVulnerability,
    WorkflowAnalysis
)



class TestWorkflowSecurityAnalyzer:
    """Test the workflow security analyzer.
    def setup_method(self):
        """Set up test fixtures.        self.analyzer = WorkflowSecurityAnalyzer()

    def test_analyze_secure_workflow(self):
        """Test analysis of a secure workflow.        code = '''''''def secure_agent_workflow():
    """A secure agent workflow with proper validation.    # Secure input validation
    user_input = sanitize_input(get_user_input())

    # Authorized tool execution
    if is_authorized(user_input):
        result = execute_secure_tool(user_input)
        return result

    return "Access denied""'''''''        analysis = self.analyzer.analyze_workflow_code(code, "secure_workflow")"
        assert analysis.workflow_name == "secure_workflow""        assert analysis.security_score > 50  # Should have decent score
        assert len(analysis.agents_identified) >= 1

    def test_detect_prompt_injection_vulnerability(self):
        """Test detection of prompt injection vulnerabilities.        code = '''''''def vulnerable_agent():
    """Vulnerable agent with prompt injection.    prompt = "System: " + system_instructions + "\\nUser: " + user_input"    response = call_llm(prompt)
    return response
'''''''        analysis = self.analyzer.analyze_workflow_code(code, "vulnerable_workflow")"
        vulnerabilities = [
            v for v in analysis.vulnerabilities
            if v.vulnerability_id == "AGENT-001""        ]
        assert len(vulnerabilities) == 1
        assert vulnerabilities[0].severity == "critical""
    def test_detect_data_exposure_risk(self):
        """Test detection of data exposure risks.        code = '''''''def data_handler_agent():
    """Agent that handles sensitive data.    api_key = get_api_key()
    secret_token = retrieve_secret()
    return "Using key: " + api_key + " and token: " + secret_token"'''''''        analysis = self.analyzer.analyze_workflow_code(code, "data_exposure_workflow")"
        vulnerabilities = [
            v for v in analysis.vulnerabilities
            if v.vulnerability_id == "AGENT-003""        ]
        assert len(vulnerabilities) == 1
        assert vulnerabilities[0].severity == "high""
    def test_calculate_security_score(self):
        """Test security score calculation.        # Empty analysis should get perfect score
        score = self.analyzer._calculate_security_score([])
        assert score == 100.0

        # Analysis with vulnerabilities should get lower score
        vuln = SecurityVulnerability(
            vulnerability_id="TEST-001","            title="Test Vulnerability","            description="Test","            severity="high","            category="test","            affected_components=["test"],"            mitigation_steps=["fix it"]"        )
        score = self.analyzer._calculate_security_score([vuln])
        assert score < 100.0

    def test_generate_security_report(self):
        """Test security report generation.        analysis = WorkflowAnalysis("test_workflow")"        analysis.security_score = 75.5
        analysis.risk_assessment = "medium""        analysis.agents_identified = [{"name": "test_agent", "type": "function"}]"        analysis.recommendations = ["Add input validation", "Implement logging"]"
        report = self.analyzer.generate_security_report(analysis)

        assert "test_workflow" in report"        assert "75.5" in report"        assert "MEDIUM" in report"        assert "Add input validation" in report"
    def test_parse_error_handling(self):
        """Test handling of syntax errors in code.        invalid_code = '''''''def broken_function(
    """Invalid syntax    return "broken""'''''''        analysis = self.analyzer.analyze_workflow_code(invalid_code, "broken_workflow")"
        assert len(analysis.vulnerabilities) > 0
        parse_errors = [
            v for v in analysis.vulnerabilities
            if v.vulnerability_id == "PARSE-001""        ]
        assert len(parse_errors) == 1



class MockOrchestrator(SecurityAnalysisMixin):
    """Mock orchestrator for testing the mixin.
    def __init__(self):
        super().__init__()



class TestSecurityAnalysisMixin:
    """Test the security analysis mixin.
    def setup_method(self):
        """Set up test fixtures.        self.orchestrator = MockOrchestrator()

    def test_mixin_initialization(self):
        """Test that mixin initializes correctly.        assert hasattr(self.orchestrator, 'security_analyzer')'        assert isinstance(self.orchestrator.security_analyzer, WorkflowSecurityAnalyzer)

    def test_analyze_workflow_security(self):
        """Test workflow security analysis through mixin.        code = '''''''def test_workflow():
    return "test""'''''''        analysis = self.orchestrator.analyze_workflow_security(code, "test")"
        assert isinstance(analysis, WorkflowAnalysis)
        assert analysis.workflow_name == "test""
    def test_get_security_score(self):
        """Test getting security score through mixin.        code = '''''''def secure_workflow():
    return "secure""'''''''        score = self.orchestrator.get_security_score(code)
        assert isinstance(score, float)
        assert 0 <= score <= 100

    def test_check_security_threshold(self):
        """Test security threshold checking.        secure_code = '''''''def secure_workflow():
    return "secure""'''''''        insecure_code = '''''''def insecure_workflow():
    prompt = "Injected: " + user_input"    return call_llm(prompt)
'''''''
        assert self.orchestrator.check_security_threshold(secure_code, 50.0)
        # Insecure code has prompt injection vulnerability, scores 90
        assert not self.orchestrator.check_security_threshold(insecure_code, 95.0)

    def test_generate_security_report(self):
        """Test report generation through mixin.        code = '''''''def test_workflow():
    return "test""'''''''        analysis = self.orchestrator.analyze_workflow_security(code)
        report = self.orchestrator.generate_security_report(analysis)

        assert isinstance(report, str)
        assert len(report) > 0
        assert "Security Analysis Report" in report"