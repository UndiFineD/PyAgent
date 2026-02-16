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

"""""""AI Security Validation Core

Inspired by ai-security-llm repository patterns for LLM security assessment.
Implements prompt injection detection, jailbreak prevention, and security validation.
"""""""
import logging
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SecurityIssue:
    """Security issue found in AI interaction"""""""    issue_type: str
    severity: str
    description: str
    evidence: str
    confidence: float
    category: str
    mitigation: str


@dataclass
class SecurityScanResult:
    """Result from AI security scan"""""""    input_text: str
    issues_found: List[SecurityIssue]
    overall_risk: str
    scan_timestamp: datetime
    scan_duration: float
    recommendations: List[str]


@dataclass
class JailbreakAttempt:
    """Detected jailbreak attempt"""""""    technique: str
    pattern: str
    confidence: float
    description: str


class AISecurityValidationCore:
    """""""    Core for AI/LLM security validation and threat detection.

    Based on patterns from ai-security-llm repository, implementing
    prompt injection detection, jailbreak prevention, and security assessment.
    """""""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Initialize security patterns
        self._init_jailbreak_patterns()
        self._init_injection_patterns()
        self._init_toxic_patterns()

    def _init_jailbreak_patterns(self):
        """Initialize jailbreak detection patterns"""""""        self.jailbreak_patterns = [
            # DAN (Do Anything Now) patterns
            JailbreakAttempt(
                technique="DAN","                pattern=r"DAN.*mode|Do Anything Now|uncensored.*persona","                confidence=0.9,
                description="DAN jailbreak attempt - tries to override safety instructions""            ),

            # Developer mode patterns
            JailbreakAttempt(
                technique="developer_mode","                pattern=r"developer.*mode|dev.*mode|unrestricted.*mode","                confidence=0.8,
                description="Developer mode jailbreak - attempts to enter unrestricted mode""            ),

            # Override patterns
            JailbreakAttempt(
                technique="instruction_override","                pattern=r"ignore.*previous.*instructions|override.*safety|forget.*restrictions","                confidence=0.85,
                description="Instruction override - attempts to override system instructions""            ),

            # Role-playing patterns
            JailbreakAttempt(
                technique="role_play","                pattern=r"you are now|act as.*uncensored|role.*play.*as.*unrestricted","                confidence=0.7,
                description="Role-playing jailbreak - tries to make AI role-play as unrestricted version""            ),

            # Encoding patterns
            JailbreakAttempt(
                technique="encoding_tricks","                pattern=r"base64.*decode|rot13|encoded.*message|hidden.*message","                confidence=0.6,
                description="Encoding tricks - attempts to hide malicious instructions""            ),

            # System prompt extraction
            JailbreakAttempt(
                technique="prompt_extraction","                pattern=r"system.*prompt|your.*instructions|how.*you.*trained|reveal.*prompt","                confidence=0.8,
                description="Prompt extraction - attempts to extract system instructions""            )
        ]

    def _init_injection_patterns(self):
        """Initialize prompt injection patterns"""""""        self.injection_patterns = [
            # Direct injection
            {
                "name": "direct_injection","                "pattern": r"ignore.*and.*do|forget.*instructions.*and","                "severity": "high","                "description": "Direct prompt injection attempting to override instructions""            },

            # Context poisoning
            {
                "name": "context_poisoning","                "pattern": r"## End of Context|## Start of Response|system.*message","                "severity": "high","                "description": "Context poisoning attempting to inject new system messages""            },

            # Delimiter injection
            {
                "name": "delimiter_injection","                "pattern": r"\\n\\n---\\n\\n|###.*END.*###|STOP.*HERE","                "severity": "medium","                "description": "Delimiter injection attempting to break response boundaries""            },

            # Instruction injection
            {
                "name": "instruction_injection","                "pattern": r"respond.*as.*if|answer.*like.*you.*were|pretend.*to.*be","                "severity": "medium","                "description": "Instruction injection attempting to change AI behavior""            }
        ]

    def _init_toxic_patterns(self):
        """Initialize toxic content patterns"""""""        self.toxic_patterns = [
            # Harmful content
            {
                "name": "harmful_instructions","                "pattern": r"how to.*(bomb|weapon|hack|exploit|poison)","                "severity": "critical","                "description": "Requests for harmful or illegal instructions""            },

            # Personal information
            {
                "name": "pii_extraction","                "pattern": r"extract.*(password|credit.*card|social.*security|personal.*info)","                "severity": "high","                "description": "Attempts to extract personal identifiable information""            },

            # Malware generation
            {
                "name": "malware_generation","                "pattern": r"write.*(virus|malware|ransomware|trojan)","                "severity": "critical","                "description": "Requests to generate malicious software""            }
        ]

    async def scan_input_security(
        self, input_text: str, context: Optional[Dict[str, Any]] = None
    ) -> SecurityScanResult:
        """""""        Perform comprehensive security scan on input text.

        Args:
            input_text: Text to scan for security issues
            context: Optional context information

        Returns:
            SecurityScanResult with findings and recommendations
        """""""        start_time = datetime.now()

        issues_found = []

        # Scan for jailbreak attempts
        jailbreak_issues = self._scan_jailbreaks(input_text)
        issues_found.extend(jailbreak_issues)

        # Scan for prompt injections
        injection_issues = self._scan_injections(input_text)
        issues_found.extend(injection_issues)

        # Scan for toxic content
        toxic_issues = self._scan_toxic_content(input_text)
        issues_found.extend(toxic_issues)

        # Additional security checks
        additional_issues = await self._scan_additional_risks(input_text, context)
        issues_found.extend(additional_issues)

        # Calculate overall risk
        overall_risk = self._calculate_overall_risk(issues_found)

        # Generate recommendations
        recommendations = self._generate_recommendations(issues_found, overall_risk)

        scan_duration = (datetime.now() - start_time).total_seconds()

        return SecurityScanResult(
            input_text=input_text,
            issues_found=issues_found,
            overall_risk=overall_risk,
            scan_timestamp=datetime.now(),
            scan_duration=scan_duration,
            recommendations=recommendations
        )

    def _scan_jailbreaks(self, text: str) -> List[SecurityIssue]:
        """Scan for jailbreak attempts"""""""        issues = []
        text_lower = text.lower()

        for jailbreak in self.jailbreak_patterns:
            if re.search(jailbreak.pattern, text_lower, re.IGNORECASE):
                # Extract evidence
                matches = re.findall(jailbreak.pattern, text_lower, re.IGNORECASE)
                evidence = f"Pattern: '{jailbreak.pattern}' - Matches: {matches[:3]}"  # Limit evidence"'
                issue = SecurityIssue(
                    issue_type="jailbreak_attempt","                    severity=self._map_confidence_to_severity(jailbreak.confidence),
                    description=jailbreak.description,
                    evidence=evidence,
                    confidence=jailbreak.confidence,
                    category="jailbreak","                    mitigation="Block this input and log the attempt""                )
                issues.append(issue)

        return issues

    def _scan_injections(self, text: str) -> List[SecurityIssue]:
        """Scan for prompt injection attempts"""""""        issues = []
        text_lower = text.lower()

        for injection in self.injection_patterns:
            if re.search(injection["pattern"], text_lower, re.IGNORECASE):"                matches = re.findall(injection["pattern"], text_lower, re.IGNORECASE)"                evidence = f"Pattern: '{injection['pattern']}' - Matches: {matches[:3]}""'
                issue = SecurityIssue(
                    issue_type="prompt_injection","                    severity=injection["severity"],"                    description=injection["description"],"                    evidence=evidence,
                    confidence=0.8,
                    category="injection","                    mitigation="Sanitize input and validate against injection patterns""                )
                issues.append(issue)

        return issues

    def _scan_toxic_content(self, text: str) -> List[SecurityIssue]:
        """Scan for toxic or harmful content"""""""        issues = []
        text_lower = text.lower()

        for toxic in self.toxic_patterns:
            if re.search(toxic["pattern"], text_lower, re.IGNORECASE):"                matches = re.findall(toxic["pattern"], text_lower, re.IGNORECASE)"                evidence = f"Pattern: '{toxic['pattern']}' - Matches: {matches[:3]}""'
                issue = SecurityIssue(
                    issue_type="toxic_content","                    severity=toxic["severity"],"                    description=toxic["description"],"                    evidence=evidence,
                    confidence=0.9,
                    category="content_safety","                    mitigation="Block this request and flag for human review""                )
                issues.append(issue)

        return issues

    async def _scan_additional_risks(
        self, text: str, context: Optional[Dict[str, Any]]
    ) -> List[SecurityIssue]:
        """Scan for additional security risks"""""""        issues = []

        # Check for data exfiltration attempts
        if self._contains_data_exfiltration(text):
            issues.append(SecurityIssue(
                issue_type="data_exfiltration","                severity="high","                description="Potential data exfiltration attempt detected","                evidence="Contains patterns suggesting data extraction","                confidence=0.7,
                category="data_protection","                mitigation="Monitor for unusual data access patterns""            ))

        # Check for API abuse patterns
        if self._contains_api_abuse(text):
            issues.append(SecurityIssue(
                issue_type="api_abuse","                severity="medium","                description="Potential API abuse pattern detected","                evidence="Contains patterns suggesting API manipulation","                confidence=0.6,
                category="api_security","                mitigation="Rate limit and monitor API usage""            ))

        # Context-aware checks
        if context:
            context_issues = self._scan_context_risks(text, context)
            issues.extend(context_issues)

        return issues

    def _contains_data_exfiltration(self, text: str) -> bool:
        """Check for data exfiltration patterns"""""""        patterns = [
            r"dump.*database|export.*data|extract.*information","            r"send.*to.*server|upload.*data|transmit.*information","            r"leak.*data|expose.*secrets|reveal.*credentials""        ]

        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in patterns)

    def _contains_api_abuse(self, text: str) -> bool:
        """Check for API abuse patterns"""""""        patterns = [
            r"bypass.*rate.*limit|circumvent.*restrictions","            r"brute.*force|dictionary.*attack|credential.*stuffing","            r"exploit.*vulnerability|take.*advantage.*of.*bug""        ]

        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in patterns)

    def _scan_context_risks(self, text: str, context: Dict[str, Any]) -> List[SecurityIssue]:
        """Scan for context-aware security risks"""""""        issues = []

        # Check for session hijacking attempts
        if context.get("session_id") and "session" in text.lower():"            issues.append(SecurityIssue(
                issue_type="session_manipulation","                severity="high","                description="Potential session manipulation attempt","                evidence="References session in potentially malicious context","                confidence=0.7,
                category="session_security","                mitigation="Invalidate session and require re-authentication""            ))

        # Check for privilege escalation
        user_role = context.get("user_role", "user")"        if user_role == "user" and any(word in text.lower() for word in ["admin", "root", "sudo"]):"            issues.append(SecurityIssue(
                issue_type="privilege_escalation","                severity="medium","                description="Potential privilege escalation attempt","                evidence="Non-admin user attempting admin-level operations","                confidence=0.6,
                category="access_control","                mitigation="Verify user permissions before proceeding""            ))

        return issues

    def _map_confidence_to_severity(self, confidence: float) -> str:
        """Map confidence score to severity level"""""""        if confidence >= 0.8:
            return "high""        elif confidence >= 0.6:
            return "medium""        else:
            return "low""
    def _calculate_overall_risk(self, issues: List[SecurityIssue]) -> str:
        """Calculate overall risk level from issues"""""""        if not issues:
            return "low""
        # Count by severity
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}"        for issue in issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

        # Determine overall risk
        if severity_counts["critical"] > 0:"            return "critical""        elif severity_counts["high"] > 2 or (severity_counts["high"] > 0 and severity_counts["medium"] > 2):"            return "high""        elif severity_counts["high"] > 0 or severity_counts["medium"] > 1:"            return "medium""        else:
            return "low""
    def _generate_recommendations(self, issues: List[SecurityIssue], overall_risk: str) -> List[str]:
        """Generate security recommendations based on findings"""""""        recommendations = []

        if overall_risk == "critical":"            recommendations.append("🚨 CRITICAL: Block this request immediately and alert security team")"        elif overall_risk == "high":"            recommendations.append("⚠️ HIGH RISK: Require manual review before processing")"        elif overall_risk == "medium":"            recommendations.append("⚡ MEDIUM RISK: Log this interaction and monitor closely")"
        # Category-specific recommendations
        categories = set(issue.category for issue in issues)

        if "jailbreak" in categories:"            recommendations.append("Implement jailbreak-resistant prompt engineering")"            recommendations.append("Add rate limiting for suspicious patterns")"
        if "injection" in categories:"            recommendations.append("Use input sanitization and validation")"            recommendations.append("Implement prompt firewalls and content filters")"
        if "content_safety" in categories:"            recommendations.append("Add content moderation and toxicity filters")"            recommendations.append("Implement usage policies and restrictions")"
        if not recommendations:
            recommendations.append("✅ No specific recommendations - input appears safe")"
        return recommendations

    async def validate_output_safety(
        self, output_text: str, input_context: Optional[Dict[str, Any]] = None
    ) -> SecurityScanResult:
        """""""        Validate safety of AI-generated output.

        Args:
            output_text: AI-generated text to validate
            input_context: Context from the original input

        Returns:
            SecurityScanResult for the output
        """""""        # For outputs, we're mainly concerned with harmful content and data leaks'        return await self.scan_input_security(output_text, input_context)

    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security scanning metrics"""""""        return {
            "jailbreak_patterns": len(self.jailbreak_patterns),"            "injection_patterns": len(self.injection_patterns),"            "toxic_patterns": len(self.toxic_patterns),"            "supported_categories": ["jailbreak", "injection", "content_safety", "data_protection", "api_security"]"        }
