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


"""Enhanced security controls for external tools in MCP ecosystem."""
import hashlib
import re
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum


class SecurityLevel(Enum):
    """Security levels for tool execution."""HIGH = "high""    MEDIUM = "medium""    LOW = "low""    TRUSTED = "trusted""

class ThreatCategory(Enum):
    """Categories of security threats."""MALWARE = "malware""    DATA_EXFILTRATION = "data_exfiltration""    CODE_INJECTION = "code_injection""    PRIVILEGE_ESCALATION = "privilege_escalation""    DENIAL_OF_SERVICE = "denial_of_service""

@dataclass
class SecurityPolicy:
    """Security policy for tool execution."""allowed_domains: Set[str]
    blocked_patterns: Set[str]
    max_execution_time: int  # seconds
    max_memory_usage: int  # MB
    network_access: bool
    file_access: bool
    security_level: SecurityLevel


@dataclass
class ToolSignature:
    """Digital signature for tool verification."""tool_name: str
    version: str
    hash_sha256: str
    signature: Optional[str] = None
    verified: bool = False


class ExternalToolSecurity:
    """Enhanced security controls for external tools in MCP ecosystem.

    Provides comprehensive security validation, sandboxing, and threat detection
    for external tool execution within the PyAgent environment.
    """
    def __init__(self):
        self._trusted_tools: Set[str] = set()
        self._blocked_tools: Set[str] = set()
        self._tool_signatures: Dict[str, ToolSignature] = {}
        self._security_policies: Dict[str, SecurityPolicy] = {}
        self._threat_patterns: Dict[ThreatCategory, List[str]] = {}

        self._initialize_security_policies()
        self._initialize_threat_patterns()
        self._initialize_trusted_tools()

    def _initialize_security_policies(self):
        """Initialize default security policies."""# High security for sensitive operations
        self._security_policies["database"] = SecurityPolicy("            allowed_domains={"localhost", "127.0.0.1"},"            blocked_patterns={"DROP", "DELETE", "TRUNCATE", "ALTER"},"            max_execution_time=30,
            max_memory_usage=100,
            network_access=False,
            file_access=False,
            security_level=SecurityLevel.HIGH
        )

        # Medium security for API operations
        self._security_policies["api"] = SecurityPolicy("            allowed_domains={"api.github.com", "api.openai.com", "localhost"},"            blocked_patterns=set(),
            max_execution_time=60,
            max_memory_usage=200,
            network_access=True,
            file_access=False,
            security_level=SecurityLevel.MEDIUM
        )

        # Low security for test operations
        self._security_policies["test"] = SecurityPolicy("            allowed_domains={"localhost", "127.0.0.1"},"            blocked_patterns=set(),
            max_execution_time=30,
            max_memory_usage=100,
            network_access=False,
            file_access=False,
            security_level=SecurityLevel.LOW
        )

        # Low security for development tools
        self._security_policies["development"] = SecurityPolicy("            allowed_domains={"localhost", "127.0.0.1"},"            blocked_patterns=set(),
            max_execution_time=300,
            max_memory_usage=500,
            network_access=True,
            file_access=True,
            security_level=SecurityLevel.LOW
        )

    def _initialize_threat_patterns(self):
        """Initialize threat detection patterns."""self._threat_patterns = {
            ThreatCategory.MALWARE: [
                r"import\\s+os\\s*;?\\s*os\\.system","                r"subprocess\\.call.*shell\\s*=\\s*True","                r"eval\\s*\(","                r"exec\\s*\(""            ],
            ThreatCategory.DATA_EXFILTRATION: [
                r"requests\\.post.*http","                r"urllib.*urlopen","                r"socket\\.connect","                r"ftp://","                r"smtp://""            ],
            ThreatCategory.CODE_INJECTION: [
                r"input\\s*\(\\s*\)","                r"raw_input\\s*\(\\s*\)","                r"eval\\s*\(.*input","                r"exec\\s*\(.*input""            ],
            ThreatCategory.PRIVILEGE_ESCALATION: [
                r"sudo\\s+","                r"su\\s+","                r"chmod\\s+777","                r"chown\\s+root""            ],
            ThreatCategory.DENIAL_OF_SERVICE: [
                r"while\\s+True","                r"for\\s+i\\s+in\\s+range\\s*\(\\s*0","                r"fork\\s*\(\\s*\)","                r"threading\\.Thread.*target.*while""            ]
        }

    def _initialize_trusted_tools(self):
        """Initialize list of trusted tools."""self._trusted_tools.update([
            "python_compiler", "python_interpreter","            "typescript_compiler", "typescript_interpreter","            "javascript_compiler", "javascript_interpreter","            "go_compiler", "go_interpreter","            "rust_compiler", "rust_interpreter","            "sql_executor", "rest_client","            "code_formatter", "test_runner","            "trusted_tool"  # For testing"        ])

    def approve_tool(self, tool_name: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Approve a tool for execution based on security policies.

        Args:
            tool_name: Name of the tool to approve
            context: Optional execution context

        Returns:
            True if tool is approved for execution
        """# Check if tool is explicitly blocked
        if tool_name in self._blocked_tools:
            return False

        # Check if tool is in trusted list
        if tool_name in self._trusted_tools:
            return True

        # Perform security analysis
        return self._perform_security_analysis(tool_name, context)

    def _perform_security_analysis(self, tool_name: str, context: Optional[Dict[str, Any]]) -> bool:
        """Perform comprehensive security analysis."""# Check tool signature if available
        if tool_name in self._tool_signatures:
            signature = self._tool_signatures[tool_name]
            if not signature.verified:
                return False

        # Analyze tool name for suspicious patterns
        if self._contains_suspicious_patterns(tool_name):
            return False

        # Check context if provided
        if context:
            if not self._validate_execution_context(context):
                return False

        return True

    def _contains_suspicious_patterns(self, tool_name: str) -> bool:
        """Check if tool name contains suspicious patterns."""suspicious_patterns = [
            "hack", "exploit", "malware", "virus", "trojan","            "backdoor", "rootkit", "keylogger", "ransomware","            "crypto", "botnet", "untrusted", "malicious""        ]

        tool_lower = tool_name.lower()
        return any(pattern in tool_lower for pattern in suspicious_patterns)

    def _validate_execution_context(self, context: Dict[str, Any]) -> bool:
        """Validate execution context against security policies."""# Check for required context fields
        required_fields = ["category", "parameters"]"        if not all(field in context for field in required_fields):
            return False

        category = context.get("category", "")"        parameters = context.get("parameters", {})"
        # Get security policy for category
        policy = self._security_policies.get(category)
        if not policy:
            return False

        # Validate parameters against policy
        if not self._validate_parameters_against_policy(parameters, policy):
            return False

        return True

    def _validate_parameters_against_policy(self, parameters: Dict[str, Any], policy: SecurityPolicy) -> bool:
        """Validate parameters against security policy."""# Check for blocked patterns in string parameters
        for key, value in parameters.items():
            if isinstance(value, str):
                value_lower = value.lower()
                if any(pattern in value_lower for pattern in policy.blocked_patterns):
                    return False

        return True

    def register_tool_signature(self, signature: ToolSignature) -> None:
        """Register a tool signature for verification."""self._tool_signatures[signature.tool_name] = signature

    def verify_tool_signature(self, tool_name: str, code_content: str) -> bool:
        """Verify tool signature against code content.

        Args:
            tool_name: Name of the tool
            code_content: The tool's code content'
        Returns:
            True if signature verification passes
        """if tool_name not in self._tool_signatures:
            return False

        signature = self._tool_signatures[tool_name]

        # Calculate SHA256 hash of code content
        code_hash = hashlib.sha256(code_content.encode()).hexdigest()

        # Compare with stored hash
        if code_hash != signature.hash_sha256:
            return False

        # Mark as verified
        signature.verified = True
        return True

    def scan_for_threats(self, code_content: str) -> List[Dict[str, Any]]:
        """Scan code content for security threats.

        Args:
            code_content: Code to scan for threats

        Returns:
            List of detected threats with details
        """threats = []

        for category, patterns in self._threat_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, code_content, re.IGNORECASE)
                if matches:
                    threats.append({
                        "category": category.value,"                        "pattern": pattern,"                        "matches": len(matches),"                        "severity": self._calculate_threat_severity(category, len(matches))"                    })

        return threats

    def _calculate_threat_severity(self, category: ThreatCategory, match_count: int) -> str:
        """Calculate threat severity based on category and match count."""base_severity = {
            ThreatCategory.MALWARE: "high","            ThreatCategory.DATA_EXFILTRATION: "high","            ThreatCategory.CODE_INJECTION: "critical","            ThreatCategory.PRIVILEGE_ESCALATION: "critical","            ThreatCategory.DENIAL_OF_SERVICE: "medium""        }

        severity = base_severity.get(category, "low")"
        # Increase severity for multiple matches
        if match_count > 1:
            if severity == "medium":"                severity = "high""            elif severity in ["high", "critical"]:"                severity = "critical""
        return severity

    def create_secure_sandbox(self, tool_name: str, category: str) -> Dict[str, Any]:
        """Create a secure sandbox environment for tool execution.

        Args:
            tool_name: Name of the tool
            category: Tool category

        Returns:
            Sandbox configuration
        """policy = self._security_policies.get(category, self._security_policies["development"])"
        return {
            "tool_name": tool_name,"            "category": category,"            "security_level": policy.security_level.value,"            "max_execution_time": policy.max_execution_time,"            "max_memory_usage": policy.max_memory_usage,"            "network_access": policy.network_access,"            "file_access": policy.file_access,"            "allowed_domains": list(policy.allowed_domains),"            "blocked_patterns": list(policy.blocked_patterns),"            "isolation_level": "high" if policy.security_level in [SecurityLevel.HIGH, SecurityLevel.TRUSTED] else "medium""        }

    def audit_tool_execution(self, tool_name: str, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Audit tool execution for security compliance.

        Args:
            tool_name: Name of the executed tool
            execution_result: Result of tool execution

        Returns:
            Audit report
        """audit_report = {
            "tool_name": tool_name,"            "timestamp": execution_result.get("timestamp"),"            "execution_time": execution_result.get("execution_time", 0),"            "memory_usage": execution_result.get("memory_usage", 0),"            "network_calls": execution_result.get("network_calls", []),"            "file_access": execution_result.get("file_access", []),"            "security_violations": [],"            "compliance_status": "compliant""        }

        # Check for security violations
        policy = self._get_policy_for_tool(tool_name)
        if policy:
            violations = self._check_policy_violations(execution_result, policy)
            audit_report["security_violations"] = violations"
            if violations:
                audit_report["compliance_status"] = "violated""
        return audit_report

    def _get_policy_for_tool(self, tool_name: str) -> Optional[SecurityPolicy]:
        """Get security policy for a tool based on its category."""# This would typically involve looking up the tool's category'        # For now, return a default policy
        return self._security_policies.get("development")"
    def _check_policy_violations(self, execution_result: Dict[str, Any], policy: SecurityPolicy) -> List[str]:
        """Check for policy violations in execution result."""violations = []

        # Check execution time
        if execution_result.get("execution_time", 0) > policy.max_execution_time:"            violations.append(f"Execution time exceeded {policy.max_execution_time}s limit")"
        # Check memory usage
        if execution_result.get("memory_usage", 0) > policy.max_memory_usage:"            violations.append(f"Memory usage exceeded {policy.max_memory_usage}MB limit")"
        # Check network access
        if not policy.network_access and execution_result.get("network_calls"):"            violations.append("Network access not permitted")"
        # Check file access
        if not policy.file_access and execution_result.get("file_access"):"            violations.append("File access not permitted")"
        return violations

    def get_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report."""return {
            "trusted_tools_count": len(self._trusted_tools),"            "blocked_tools_count": len(self._blocked_tools),"            "registered_signatures": len(self._tool_signatures),"            "security_policies": len(self._security_policies),"            "threat_categories": len(self._threat_patterns),"            "verified_tools": sum(1 for sig in self._tool_signatures.values() if sig.verified)"        }