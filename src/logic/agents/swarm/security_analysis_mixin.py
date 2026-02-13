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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Security Analysis Mixin - Workflow Security Analysis and Threat Modeling

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate WorkflowSecurityAnalyzer and call analyze(workflow_ast) or integrate as a mixin on agent orchestration classes to produce WorkflowAnalysis objects and vulnerability reports.
- Example: analyzer = WorkflowSecurityAnalyzer(); report = analyzer.analyze(parsed_workflow); print(report.recommendations)

WHAT IT DOES:
- Provides dataclasses (SecurityVulnerability, WorkflowAnalysis) to model findings and an analyzer class (WorkflowSecurityAnalyzer) that loads a built-in vulnerability database and performs static analysis / threat modeling of agent workflows.
- Identifies common AI-agent risks (prompt injection, tool-execution bypass, data exfiltration), scores risk, documents affected components, and emits mitigation recommendations and OWASP-style references.

WHAT IT SHOULD DO BETTER:
- Expose a public analyze(...) method with robust AST traversal hooks, rule registration, and plugin support so new vulnerability rules can be added without editing core code.
- Add runtime/behavioral analysis (dynamic instrumentation, canary token handling, telemetry) and richer reporting formats (SARIF, JSON Schema, CI-failing thresholds).
- Harden defaults: configurable severity mapping, allowlists/denylists for tools, provenance tracking for data flows, and automated fix suggestions or CI gate integration.

FILE CONTENT SUMMARY:
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Security analysis and threat modeling for PyAgent workflows."""

import ast
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


logger = logging.getLogger(__name__)


@dataclass
class SecurityVulnerability:
    """Represents a security vulnerability in an agent workflow."""

    vulnerability_id: str
    title: str
    description: str
    severity: str  # "critical", "high", "medium", "low", "info"
    category: str  # "authentication", "authorization", "data_exposure", etc.
    affected_components: List[str]
    mitigation_steps: List[str]
    owasp_reference: Optional[str] = None
    cve_reference: Optional[str] = None


@dataclass
class WorkflowAnalysis:
    """Analysis results for an agent workflow."""

    workflow_name: str
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    agents_identified: List[Dict[str, Any]] = field(default_factory=list)
    tools_identified: List[Dict[str, Any]] = field(default_factory=list)
    data_flows: List[Dict[str, Any]] = field(default_factory=list)
    vulnerabilities: List[SecurityVulnerability] = field(default_factory=list)
    security_score: float = 0.0
    risk_assessment: str = "unknown"
    recommendations: List[str] = field(default_factory=list)


class WorkflowSecurityAnalyzer:
    """
    Security analyzer for PyAgent workflows.

    Inspired by Agent-Wiz's threat modeling capabilities, this analyzer
    performs static analysis of agent workflows to identify security
    vulnerabilities and provide mitigation recommendations.
    """

    def __init__(self):
        self.vulnerability_database = self._load_vulnerability_database()

    def _load_vulnerability_database(self) -> Dict[str, SecurityVulnerability]:
        """Load the vulnerability database with known AI agent security issues."""
        return {
            "prompt_injection": SecurityVulnerability(
                vulnerability_id="AGENT-001",
                title="Prompt Injection Vulnerability",
                description=(
                    "Agent susceptible to prompt injection attacks where malicious "
                    "input can override system instructions"
                ),
                severity="critical",
                category="input_validation",
                affected_components=["agent_instruction_parsing"],
                mitigation_steps=[
                    "Implement prompt sanitization and validation",
                    "Use structured prompts with clear boundaries",
                    "Add input filtering and length limits",
                    "Implement canary tokens for injection detection"
                ],
                owasp_reference="OWASP LLM TOP 10 - A01:2024 Prompt Injection"
            ),
            "tool_execution_bypass": SecurityVulnerability(
                vulnerability_id="AGENT-002",
                title="Tool Execution Authorization Bypass",
                description="Agent can execute tools without proper authorization checks",
                severity="high",
                category="authorization",
                affected_components=["tool_execution"],
                mitigation_steps=[
                    "Implement tool authorization checks",
                    "Add tool execution policies",
                    "Validate tool parameters against allowlists",
                    "Log all tool executions with context"
                ],
                owasp_reference="OWASP LLM TOP 10 - A02:2024 Insecure Output Handling"
            ),
            "data_exfiltration": SecurityVulnerability(
                vulnerability_id="AGENT-003",
                title="Sensitive Data Exfiltration Risk",
                description="Agent workflows may expose sensitive data through tool outputs or agent communications",
                severity="high",
                category="data_exposure",
                affected_components=["data_handling", "agent_communication"],
                mitigation_steps=[
                    "Implement data classification and handling policies",
                    "Add data sanitization befo
"""

import ast
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


logger = logging.getLogger(__name__)


@dataclass
class SecurityVulnerability:
    """Represents a security vulnerability in an agent workflow."""

    vulnerability_id: str
    title: str
    description: str
    severity: str  # "critical", "high", "medium", "low", "info"
    category: str  # "authentication", "authorization", "data_exposure", etc.
    affected_components: List[str]
    mitigation_steps: List[str]
    owasp_reference: Optional[str] = None
    cve_reference: Optional[str] = None


@dataclass
class WorkflowAnalysis:
    """Analysis results for an agent workflow."""

    workflow_name: str
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    agents_identified: List[Dict[str, Any]] = field(default_factory=list)
    tools_identified: List[Dict[str, Any]] = field(default_factory=list)
    data_flows: List[Dict[str, Any]] = field(default_factory=list)
    vulnerabilities: List[SecurityVulnerability] = field(default_factory=list)
    security_score: float = 0.0
    risk_assessment: str = "unknown"
    recommendations: List[str] = field(default_factory=list)


class WorkflowSecurityAnalyzer:
    """
    Security analyzer for PyAgent workflows.

    Inspired by Agent-Wiz's threat modeling capabilities, this analyzer
    performs static analysis of agent workflows to identify security
    vulnerabilities and provide mitigation recommendations.
    """

    def __init__(self):
        self.vulnerability_database = self._load_vulnerability_database()

    def _load_vulnerability_database(self) -> Dict[str, SecurityVulnerability]:
        """Load the vulnerability database with known AI agent security issues."""
        return {
            "prompt_injection": SecurityVulnerability(
                vulnerability_id="AGENT-001",
                title="Prompt Injection Vulnerability",
                description=(
                    "Agent susceptible to prompt injection attacks where malicious "
                    "input can override system instructions"
                ),
                severity="critical",
                category="input_validation",
                affected_components=["agent_instruction_parsing"],
                mitigation_steps=[
                    "Implement prompt sanitization and validation",
                    "Use structured prompts with clear boundaries",
                    "Add input filtering and length limits",
                    "Implement canary tokens for injection detection"
                ],
                owasp_reference="OWASP LLM TOP 10 - A01:2024 Prompt Injection"
            ),
            "tool_execution_bypass": SecurityVulnerability(
                vulnerability_id="AGENT-002",
                title="Tool Execution Authorization Bypass",
                description="Agent can execute tools without proper authorization checks",
                severity="high",
                category="authorization",
                affected_components=["tool_execution"],
                mitigation_steps=[
                    "Implement tool authorization checks",
                    "Add tool execution policies",
                    "Validate tool parameters against allowlists",
                    "Log all tool executions with context"
                ],
                owasp_reference="OWASP LLM TOP 10 - A02:2024 Insecure Output Handling"
            ),
            "data_exfiltration": SecurityVulnerability(
                vulnerability_id="AGENT-003",
                title="Sensitive Data Exfiltration Risk",
                description="Agent workflows may expose sensitive data through tool outputs or agent communications",
                severity="high",
                category="data_exposure",
                affected_components=["data_handling", "agent_communication"],
                mitigation_steps=[
                    "Implement data classification and handling policies",
                    "Add data sanitization before output",
                    "Use encrypted communication channels",
                    "Implement data loss prevention (DLP) controls"
                ],
                owasp_reference="OWASP LLM TOP 10 - A03:2024 Sensitive Information Disclosure"
            ),
            "infinite_loop": SecurityVulnerability(
                vulnerability_id="AGENT-004",
                title="Infinite Loop/Resource Exhaustion",
                description="Agent workflows lack proper termination conditions, risking resource exhaustion",
                severity="medium",
                category="denial_of_service",
                affected_components=["workflow_execution"],
                mitigation_steps=[
                    "Implement maximum iteration limits",
                    "Add timeout mechanisms",
                    "Include convergence checks",
                    "Monitor resource usage"
                ]
            ),
            "untrusted_tool_integration": SecurityVulnerability(
                vulnerability_id="AGENT-005",
                title="Untrusted Tool Integration",
                description="Agent integrates with external tools without proper validation",
                severity="medium",
                category="supply_chain",
                affected_components=["tool_integration"],
                mitigation_steps=[
                    "Validate tool sources and integrity",
                    "Implement tool sandboxing",
                    "Add tool output validation",
                    "Use trusted tool registries"
                ],
                owasp_reference="OWASP LLM TOP 10 - A05:2024 Supply Chain Vulnerabilities"
            )
        }

    def analyze_workflow_code(self, code: str, filename: str = "unknown") -> WorkflowAnalysis:
        """
        Analyze workflow code for security vulnerabilities.

        Args:
            code: Python code containing agent workflow definitions
            filename: Name of the file being analyzed

        Returns:
            WorkflowAnalysis with findings and recommendations
        """
        analysis = WorkflowAnalysis(workflow_name=filename)

        try:
            # Parse the AST
            tree = ast.parse(code)

            # Extract workflow components
            analyzer = WorkflowASTAnalyzer()
            analyzer.visit(tree)

            analysis.agents_identified = analyzer.agents
            analysis.tools_identified = analyzer.tools
            analysis.data_flows = analyzer.data_flows

            # Perform security analysis
            vulnerabilities = self._analyze_security_issues(analyzer)
            analysis.vulnerabilities = vulnerabilities

            # Calculate security score
            analysis.security_score = self._calculate_security_score(vulnerabilities)
            analysis.risk_assessment = self._assess_risk_level(analysis.security_score)

            # Generate recommendations
            analysis.recommendations = self._generate_recommendations(vulnerabilities, analyzer)

        except SyntaxError as e:
            logger.error(f"Syntax error in {filename}: {e}")
            analysis.vulnerabilities.append(SecurityVulnerability(
                vulnerability_id="PARSE-001",
                title="Code Parsing Error",
                description=f"Unable to parse workflow code: {e}",
                severity="high",
                category="code_quality",
                affected_components=["code_parsing"],
                mitigation_steps=["Fix syntax errors", "Validate code before deployment"]
            ))

        return analysis

    def _analyze_security_issues(self, analyzer: 'WorkflowASTAnalyzer') -> List[SecurityVulnerability]:
        """Analyze the parsed workflow for security issues."""
        vulnerabilities = []

        # Check for prompt injection vulnerabilities
        if self._has_prompt_injection_risk(analyzer):
            vulnerabilities.append(self.vulnerability_database["prompt_injection"])

        # Check for tool execution issues
        if self._has_tool_execution_risk(analyzer):
            vulnerabilities.append(self.vulnerability_database["tool_execution_bypass"])

        # Check for data exposure risks
        if self._has_data_exposure_risk(analyzer):
            vulnerabilities.append(self.vulnerability_database["data_exfiltration"])

        # Check for infinite loop risks
        if self._has_infinite_loop_risk(analyzer):
            vulnerabilities.append(self.vulnerability_database["infinite_loop"])

        # Check for untrusted tool integration
        if self._has_untrusted_tool_risk(analyzer):
            vulnerabilities.append(self.vulnerability_database["untrusted_tool_integration"])

        return vulnerabilities

    def _has_prompt_injection_risk(self, analyzer: 'WorkflowASTAnalyzer') -> bool:
        """Check if workflow has prompt injection vulnerabilities."""
        # Look for LLM calls which could be vulnerable to prompt injection
        llm_calls = [flow for flow in analyzer.data_flows if flow.get("type") == "llm_call"]
        return len(llm_calls) > 0

    def _has_tool_execution_risk(self, analyzer: 'WorkflowASTAnalyzer') -> bool:
        """Check if workflow has tool execution authorization issues."""
        # Check if external function calls are made
        external_calls = [
            flow for flow in analyzer.data_flows
            if flow.get("type") == "function_call"
            and flow.get("callee") not in [agent["name"] for agent in analyzer.agents]
        ]
        return len(external_calls) > 0

    def _has_data_exposure_risk(self, analyzer: 'WorkflowASTAnalyzer') -> bool:
        """Check if workflow has data exposure risks."""
        # Check for sensitive data handling patterns
        sensitive_keywords = ["password", "secret", "token", "key", "api_key", "data_handler"]
        for agent in analyzer.agents:
            # Check function names
            func_name = agent.get("name", "").lower()
            if any(keyword in func_name for keyword in sensitive_keywords):
                return True
        return False

    def _has_infinite_loop_risk(self, analyzer: 'WorkflowASTAnalyzer') -> bool:
        """Check if workflow has infinite loop risks."""
        # Look for loops without termination conditions
        has_loops = any(flow.get("type") == "loop" for flow in analyzer.data_flows)
        has_termination = any(flow.get("type") == "termination_check" for flow in analyzer.data_flows)
        return has_loops and not has_termination

    def _has_untrusted_tool_risk(self, analyzer: 'WorkflowASTAnalyzer') -> bool:
        """Check if workflow uses untrusted tools."""
        # Check for external tool imports or calls
        external_tools = [tool for tool in analyzer.tools if tool.get("source") == "external"]
        return len(external_tools) > 0

    def _calculate_security_score(self, vulnerabilities: List[SecurityVulnerability]) -> float:
        """Calculate overall security score (0-100, higher is better)."""
        if not vulnerabilities:
            return 100.0

        # Severity weights
        severity_weights = {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 2,
            "info": 1
        }

        total_penalty = sum(severity_weights.get(v.severity, 0) for v in vulnerabilities)
        score = max(0, 100 - total_penalty)
        return score

    def _assess_risk_level(self, score: float) -> str:
        """Assess overall risk level based on security score."""
        if score >= 80:
            return "low"
        elif score >= 60:
            return "medium"
        elif score >= 40:
            return "high"
        else:
            return "critical"

    def _generate_recommendations(
        self,
        vulnerabilities: List[SecurityVulnerability],
        analyzer: 'WorkflowASTAnalyzer'
    ) -> List[str]:
        """Generate security recommendations."""
        recommendations = []

        if vulnerabilities:
            recommendations.append("Implement comprehensive input validation and sanitization")
            recommendations.append("Add authentication and authorization checks for all agent actions")
            recommendations.append("Implement logging and monitoring for all agent activities")
            recommendations.append("Regular security audits and penetration testing of agent workflows")

        if len(analyzer.agents) > 5:
            recommendations.append("Consider breaking down large workflows into smaller, manageable components")

        if len(analyzer.tools) > 10:
            recommendations.append("Review tool usage and implement tool governance policies")

        return recommendations

    def generate_security_report(self, analysis: WorkflowAnalysis) -> str:
        """Generate a comprehensive security report."""
        report = f"""
# Security Analysis Report for {analysis.workflow_name}

**Analysis Date:** {analysis.analysis_timestamp}
**Security Score:** {analysis.security_score:.1f}/100
**Risk Level:** {analysis.risk_assessment.upper()}

## Workflow Overview

- **Agents Identified:** {len(analysis.agents_identified)}
- **Tools Identified:** {len(analysis.tools_identified)}
- **Data Flows:** {len(analysis.data_flows)}

## Security Vulnerabilities Found

"""

        if analysis.vulnerabilities:
            for vuln in analysis.vulnerabilities:
                report += f"""
### {vuln.vulnerability_id}: {vuln.title}

**Severity:** {vuln.severity.upper()}
**Category:** {vuln.category}
**Description:** {vuln.description}

**Affected Components:**
{chr(10).join(f"- {comp}" for comp in vuln.affected_components)}

**Mitigation Steps:**
{chr(10).join(f"- {step}" for step in vuln.mitigation_steps)}

"""
                if vuln.owasp_reference:
                    report += f"**OWASP Reference:** {vuln.owasp_reference}\n"
        else:
            report += "✅ No security vulnerabilities detected.\n"

        report += f"""
## Recommendations

{chr(10).join(f"- {rec}" for rec in analysis.recommendations)}

## Security Score Interpretation

- 80-100: Low Risk - Workflow is well-secured
- 60-79: Medium Risk - Some security improvements recommended
- 40-59: High Risk - Significant security issues require attention
- 0-39: Critical Risk - Immediate security remediation required

---
*Report generated by PyAgent Security Analyzer*
"""

        return report


class WorkflowASTAnalyzer(ast.NodeVisitor):
    """
    AST analyzer for extracting workflow components from Python code.

    Based on Agent-Wiz's AST parsing approach for workflow extraction.
    """

    def __init__(self):
        self.agents = []
        self.tools = []
        self.data_flows = []
        self.current_function = None
        self.imports = set()

    def visit_Import(self, node):
        """Track imports for external tool detection."""
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node):
        """Track from imports."""
        module = node.module or ""
        for alias in node.names:
            self.imports.add(f"{module}.{alias.name}")

    def visit_ClassDef(self, node):
        """Extract agent classes."""
        # Look for agent-related classes
        if any(keyword in node.name.lower() for keyword in ["agent", "orchestrator", "coordinator"]):
            agent_info = {
                "name": node.name,
                "type": "class",
                "methods": [method.name for method in node.body if isinstance(method, ast.FunctionDef)],
                "bases": [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases]
            }
            self.agents.append(agent_info)

    def visit_FunctionDef(self, node):
        """Extract agent functions and tools."""
        self.current_function = node.name

        # Check if this looks like an agent function
        if any(keyword in node.name.lower() for keyword in ["agent", "workflow", "orchestrate"]):
            agent_info = {
                "name": node.name,
                "type": "function",
                "args": [arg.arg for arg in node.args.args],
                "docstring": self._get_docstring(node)
            }
            self.agents.append(agent_info)

        # Check for tool definitions
        if any(keyword in node.name.lower() for keyword in ["tool", "function", "call"]):
            tool_info = {
                "name": node.name,
                "type": "function",
                "source": "internal" if not self._is_external_tool(node) else "external"
            }
            self.tools.append(tool_info)

        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        """Extract function calls and data flows."""
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # Handle method calls like obj.method()
            func_name = node.func.attr

        if func_name:
            # Track all function calls as potential tool usage
            self.data_flows.append({
                "type": "function_call",
                "caller": self.current_function,
                "callee": func_name,
                "args": len(node.args) if node.args else 0
            })

            # Check if this looks like an LLM call (potential prompt injection)
            llm_keywords = ["llm", "gpt", "claude", "openai", "anthropic"]
            if any(llm_keyword in func_name.lower() for llm_keyword in llm_keywords):
                self.data_flows[-1]["type"] = "llm_call"

        self.generic_visit(node)

    def _get_docstring(self, node) -> Optional[str]:
        """Extract docstring from a function or class."""
        if node.body and isinstance(node.body[0], ast.Expr):
            expr = node.body[0]
            if isinstance(expr.value, ast.Constant) and isinstance(expr.value.value, str):
                return expr.value.value
            # Fallback for older Python versions
            elif hasattr(expr.value, 's'):
                return expr.value.s
        return None

    def _is_external_tool(self, node) -> bool:
        """Check if a tool function uses external libraries."""
        # Simple heuristic: check if function body references imported modules
        external_modules = {"requests", "urllib", "subprocess", "os", "sys"}

        for child in ast.walk(node):
            if isinstance(child, ast.Name) and child.id in external_modules:
                return True
            if isinstance(child, ast.Attribute) and isinstance(child.value, ast.Name):
                if child.value.id in self.imports:
                    return True

        return False


class SecurityAnalysisMixin:
    """
    Mixin to add security analysis capabilities to PyAgent orchestrators.

    This mixin provides methods to analyze workflows for security vulnerabilities
    and generate security reports, inspired by Agent-Wiz's threat modeling.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.security_analyzer = WorkflowSecurityAnalyzer()

    def analyze_workflow_security(self, workflow_code: str, workflow_name: str = "unknown") -> WorkflowAnalysis:
        """
        Analyze a workflow for security vulnerabilities.

        Args:
            workflow_code: Python code defining the workflow
            workflow_name: Name of the workflow for reporting

        Returns:
            Security analysis results
        """
        return self.security_analyzer.analyze_workflow_code(workflow_code, workflow_name)

    def generate_security_report(self, analysis: WorkflowAnalysis) -> str:
        """
        Generate a comprehensive security report.

        Args:
            analysis: Security analysis results

        Returns:
            Formatted security report
        """
        return self.security_analyzer.generate_security_report(analysis)

    def get_security_score(self, workflow_code: str) -> float:
        """
        Get a security score for workflow code.

        Args:
            workflow_code: Python code to analyze

        Returns:
            Security score (0-100, higher is better)
        """
        analysis = self.analyze_workflow_security(workflow_code)
        return analysis.security_score

    def check_security_threshold(self, workflow_code: str, threshold: float = 70.0) -> bool:
        """
        Check if workflow meets security threshold.

        Args:
            workflow_code: Python code to analyze
            threshold: Minimum security score required

        Returns:
            True if security score meets threshold
        """
        score = self.get_security_score(workflow_code)
        return score >= threshold
