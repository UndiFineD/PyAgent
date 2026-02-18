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

# Active Directory Threat Hunting Core - AD Security Analysis and Monitoring
# Based on patterns from Active_Directory_Advanced_Threat_Hunting repository

import asyncio
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

from src.core.base.common.base_core import BaseCore



class ThreatLevel(Enum):
    """Threat severity levels"""LOW = "low""    MEDIUM = "medium""    HIGH = "high""    CRITICAL = "critical""


class ADObjectType(Enum):
    """Active Directory object types"""USER = "user""    COMPUTER = "computer""    GROUP = "group""    OU = "organizational_unit""    GPO = "group_policy_object""    SERVICE_ACCOUNT = "service_account""

@dataclass
class ADObject:
    """Represents an Active Directory object"""distinguished_name: str
    object_class: ADObjectType
    sam_account_name: Optional[str] = None
    user_principal_name: Optional[str] = None
    member_of: List[str] = field(default_factory=list)
    permissions: Dict[str, Any] = field(default_factory=dict)
    last_logon: Optional[datetime] = None
    password_last_set: Optional[datetime] = None
    account_status: str = "active""    risk_indicators: List[str] = field(default_factory=list)


@dataclass
class ThreatFinding:
    """Represents a threat hunting finding"""id: str
    title: str
    description: str
    threat_level: ThreatLevel
    affected_objects: List[str]
    mitre_technique: Optional[str] = None
    evidence: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class HuntingResult:
    """Results from a threat hunting operation"""scan_id: str
    scan_type: str
    findings: List[ThreatFinding]
    scanned_objects: int
    execution_time: float
    risk_score: float
    summary: Dict[str, Any] = field(default_factory=dict)



class ActiveDirectoryThreatHuntingCore(BaseCore):
    """Active Directory Threat Hunting Core for comprehensive AD security analysis.

    Provides capabilities for Active Directory enumeration, threat detection,
    permission analysis, and security monitoring based on advanced threat hunting patterns.
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.ad_objects: Dict[str, ADObject] = {}
        self.threat_findings: List[ThreatFinding] = []
        self.hunting_history: List[HuntingResult] = []
        self.risk_indicators: Dict[str, List[str]] = {}
        self.baseline_data: Dict[str, Any] = {}

    async def initialize(self) -> bool:
        """Initialize the Active Directory threat hunting core"""
try:
            # Initialize threat detection rules and baselines
            await self.load_threat_detection_rules()
            await self.initialize_baselines()
            self.logger.info("Active Directory Threat Hunting Core initialized successfully")"            return True
        except Exception:  # noqa: BLE001
            self.logger.exception("Failed to initialize Active Directory Threat Hunting Core")"            return False

    async def load_threat_detection_rules(self) -> None:
        """Load threat detection rules and indicators"""self.risk_indicators = {
            "privileged_accounts": ["                "Domain Admins","                "Enterprise Admins","                "Schema Admins","                "Administrators""            ],
            "suspicious_permissions": ["                "GenericAll","                "GenericWrite","                "WriteDACL","                "WriteOwner","                "Replicating Directory Changes""            ],
            "service_accounts": ["                "ServicePrincipalNames","                "PasswordNeverExpires","                "TrustedForDelegation""            ],
            "stale_accounts": ["                "LastLogon > 90 days","                "PasswordLastSet > 180 days""            ],
            "weak_security": ["                "PreAuthNotRequired","                "DontRequirePreAuth","                "PasswordNotRequired""            ]
        }

        self.logger.info(f"Loaded threat detection rules with {len(self.risk_indicators)} categories")"
    async def initialize_baselines(self) -> None:
        """Initialize baseline security configurations"""self.baseline_data = {
            "max_group_membership": 50,"            "max_privileged_accounts": 10,"            "password_expiry_days": 90,"            "account_lockout_threshold": 5,"            "stale_account_threshold_days": 90,"            "service_account_indicators": ["svc-", "service-", "-svc", "-service"]"        }

        self.logger.info("Initialized baseline security configurations")"
    async def enumerate_ad_objects(
        self,
        _domain_controller: Optional[str] = None,
        _search_base: Optional[str] = None,
        object_types: Optional[List[ADObjectType]] = None
    ) -> List[ADObject]:
        """Enumerate Active Directory objects

        Args:
            domain_controller: Domain controller to query
            search_base: Search base DN
            object_types: Types of objects to enumerate

        Returns:
            List of enumerated AD objects
        """
# Mock AD enumeration - in real implementation, this would use LDAP queries
        enumerated_objects = []

        # Generate mock AD objects for demonstration
        default_types = [ADObjectType.USER, ADObjectType.COMPUTER, ADObjectType.GROUP]
        mock_objects = await self._generate_mock_ad_objects(object_types or default_types)

        for obj_data in mock_objects:
            ad_object = ADObject(
                distinguished_name=obj_data["dn"],"                object_class=obj_data["type"],"                sam_account_name=obj_data.get("sam_account_name"),"                user_principal_name=obj_data.get("upn"),"                member_of=obj_data.get("member_of", []),"                permissions=obj_data.get("permissions", {}),"                last_logon=obj_data.get("last_logon"),"                password_last_set=obj_data.get("password_last_set"),"                account_status=obj_data.get("status", "active")"            )

            self.ad_objects[ad_object.distinguished_name] = ad_object
            enumerated_objects.append(ad_object)

        self.logger.info(f"Enumerated {len(enumerated_objects)} AD objects")"        return enumerated_objects

    async def _generate_mock_ad_objects(self, object_types: List[ADObjectType]) -> List[Dict[str, Any]]:
        """Generate mock AD objects for demonstration"""objects = []

        if ADObjectType.USER in object_types:
            # Mock users
            users = [
                {
                    "dn": "CN=Administrator,CN=Users,DC=domain,DC=com","                    "type": ADObjectType.USER,"                    "sam_account_name": "Administrator","                    "upn": "admin@domain.com","                    "member_of": ["Domain Admins", "Administrators"],"                    "permissions": {"GenericAll": True},"                    "last_logon": datetime.now() - timedelta(days=1),"                    "password_last_set": datetime.now() - timedelta(days=30),"                    "status": "active""                },
                {
                    "dn": "CN=John Doe,CN=Users,DC=domain,DC=com","                    "type": ADObjectType.USER,"                    "sam_account_name": "jdoe","                    "upn": "jdoe@domain.com","                    "member_of": ["Domain Users"],"                    "permissions": {},"                    "last_logon": datetime.now() - timedelta(days=5),"                    "password_last_set": datetime.now() - timedelta(days=60),"                    "status": "active""                },
                {
                    "dn": "CN=svc-sql,CN=Users,DC=domain,DC=com","                    "type": ADObjectType.USER,"                    "sam_account_name": "svc-sql","                    "upn": "svc-sql@domain.com","                    "member_of": ["Service Accounts"],"                    "permissions": {"ServicePrincipalNames": ["MSSQLSvc/server.domain.com"]},"                    "last_logon": datetime.now() - timedelta(days=1),"                    "password_last_set": datetime.now() - timedelta(days=365),"                    "status": "active""                }
            ]
            objects.extend(users)

        if ADObjectType.COMPUTER in object_types:
            # Mock computers
            computers = [
                {
                    "dn": "CN=WORKSTATION01,CN=Computers,DC=domain,DC=com","                    "type": ADObjectType.COMPUTER,"                    "sam_account_name": "WORKSTATION01$","                    "last_logon": datetime.now() - timedelta(days=2),"                    "status": "active""                }
            ]
            objects.extend(computers)

        if ADObjectType.GROUP in object_types:
            # Mock groups
            groups = [
                {
                    "dn": "CN=Domain Admins,CN=Users,DC=domain,DC=com","                    "type": ADObjectType.GROUP,"                    "sam_account_name": "Domain Admins","                    "member_of": ["Administrators"],"                    "permissions": {"GenericAll": True}"                }
            ]
            objects.extend(groups)

        return objects

    async def perform_threat_hunt(
        self,
        hunt_type: str,
        target_objects: Optional[List[str]] = None,  # noqa: ARG002
        custom_rules: Optional[Dict[str, Any]] = None  # noqa: ARG002
    ) -> HuntingResult:
        """Perform a threat hunting operation

        Args:
            hunt_type: Type of hunt (privileged_accounts, stale_accounts, etc.)
            target_objects: Specific objects to hunt in
            custom_rules: Custom hunting rules

        Returns:
            Hunting results
        """start_time = asyncio.get_event_loop().time()

        findings = []
        scanned_objects = 0

        # Select hunting method
        if hunt_type == "privileged_accounts":"            findings.extend(await self._hunt_privileged_accounts())
        elif hunt_type == "stale_accounts":"            findings.extend(await self._hunt_stale_accounts())
        elif hunt_type == "service_accounts":"            findings.extend(await self._hunt_service_accounts())
        elif hunt_type == "suspicious_permissions":"            findings.extend(await self._hunt_suspicious_permissions())
        elif hunt_type == "weak_security":"            findings.extend(await self._hunt_weak_security())
        else:
            findings.extend(await self._perform_general_hunt())

        scanned_objects = len(self.ad_objects)

        # Calculate risk score
        risk_score = await self._calculate_risk_score(findings)

        # Create result
        result = HuntingResult(
            scan_id=f"hunt_{datetime.now().strftime('%Y%m%d_%H%M%S')}","'            scan_type=hunt_type,
            findings=findings,
            scanned_objects=scanned_objects,
            execution_time=asyncio.get_event_loop().time() - start_time,
            risk_score=risk_score,
            summary={
                "total_findings": len(findings),"                "high_risk_findings": len(["                    f for f in findings if f.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
                ]),
                "affected_objects": len(set(obj for f in findings for obj in f.affected_objects))"            }
        )

        self.hunting_history.append(result)
        self.threat_findings.extend(findings)

        self.logger.info(f"Completed threat hunt '{hunt_type}': {len(findings)} findings, risk score: {risk_score:.2f}")"'        return result

    async def _hunt_privileged_accounts(self) -> List[ThreatFinding]:
        """Hunt for privileged accounts and excessive permissions"""findings = []

        privileged_groups = self.risk_indicators["privileged_accounts"]"
        for obj in self.ad_objects.values():
            if obj.object_class == ADObjectType.USER:
                # Check group memberships
                privileged_memberships = [group for group in obj.member_of if group in privileged_groups]

                if privileged_memberships:
                    threat_level = ThreatLevel.HIGH if "Domain Admins" in privileged_memberships else ThreatLevel.MEDIUM"
                    findings.append(ThreatFinding(
                        id=f"priv_acc_{obj.sam_account_name}","                        title="Privileged Account Detected","                        description=(
                            f"User {obj.sam_account_name} has membership in privileged ""                            f"groups: {', '.join(privileged_memberships)}""'                        ),
                        threat_level=threat_level,
                        affected_objects=[obj.distinguished_name],
                        mitre_technique="T1078.002",  # Valid Accounts: Domain Accounts"                        evidence={
                            "privileged_groups": privileged_memberships,"                            "last_logon": obj.last_logon.isoformat() if obj.last_logon else None"                        },
                        recommendations=[
                            "Review necessity of privileged access","                            "Implement just-in-time access","                            "Enable multi-factor authentication""                        ]
                    ))

        return findings

    async def _hunt_stale_accounts(self) -> List[ThreatFinding]:
        """Hunt for stale and inactive accounts"""findings = []
        threshold_days = self.baseline_data["stale_account_threshold_days"]"
        for obj in self.ad_objects.values():
            if obj.object_class in [ADObjectType.USER, ADObjectType.COMPUTER]:
                days_since_logon = (datetime.now() - (obj.last_logon or datetime.min)).days

                if days_since_logon > threshold_days:
                    findings.append(ThreatFinding(
                        id=f"stale_acc_{obj.sam_account_name}","                        title="Stale Account Detected","                        description=(
                            f"Account {obj.sam_account_name} hasn't logged in for ""'                            f"{days_since_logon} days""                        ),
                        threat_level=ThreatLevel.MEDIUM,
                        affected_objects=[obj.distinguished_name],
                        mitre_technique="T1078.003",  # Valid Accounts: Local Accounts"                        evidence={
                            "days_since_logon": days_since_logon,"                            "last_logon": obj.last_logon.isoformat() if obj.last_logon else None"                        },
                        recommendations=[
                            "Disable or remove stale accounts","                            "Review account lifecycle management","                            "Implement automated account cleanup""                        ]
                    ))

        return findings

    async def _hunt_service_accounts(self) -> List[ThreatFinding]:
        """Hunt for service accounts and their security posture"""findings = []

        for obj in self.ad_objects.values():
            if obj.object_class == ADObjectType.USER:
                # Check for service account indicators
                is_service_account = (
                    obj.sam_account_name and
                    any(
                        indicator in obj.sam_account_name.lower()
                        for indicator in self.baseline_data["service_account_indicators"]"                    )
                ) or (obj.user_principal_name and "svc-" in obj.user_principal_name.lower())"
                if is_service_account:
                    # Check for security issues
                    issues = []

                    # Check password age
                    if obj.password_last_set:
                        password_age_days = (datetime.now() - obj.password_last_set).days
                        if password_age_days > 365:
                            issues.append(f"Password not changed for {password_age_days} days")"
                    # Check for SPNs
                    if "ServicePrincipalNames" in obj.permissions:"                        spns = obj.permissions["ServicePrincipalNames"]"                        if not spns:
                            issues.append("Service account has no SPNs configured")"
                    # Check delegation
                    if (obj.permissions or {}).get("TrustedForDelegation"):"                        issues.append("Account is trusted for delegation")"
                    if issues:
                        findings.append(ThreatFinding(
                            id=f"svc_acc_{obj.sam_account_name}","                            title="Service Account Security Issue","                            description=(
                                f"Service account {obj.sam_account_name} has security ""                                f"concerns: {', '.join(issues)}""'                            ),
                            threat_level=ThreatLevel.MEDIUM,
                            affected_objects=[obj.distinguished_name],
                            mitre_technique="T1078.003",  # Valid Accounts: Local Accounts"                            evidence={
                                "issues": issues,"                                "password_age_days": ("                                    (datetime.now() - obj.password_last_set).days
                                    if obj.password_last_set else None
                                ),
                                "has_spn": bool((obj.permissions or {}).get("ServicePrincipalNames"))"                            },
                            recommendations=[
                                "Regularly rotate service account passwords","                                "Limit service account permissions","                                "Monitor service account usage""                            ]
                        ))

        return findings

    async def _hunt_suspicious_permissions(self) -> List[ThreatFinding]:
        """Hunt for suspicious permissions and access rights"""findings = []
        suspicious_perms = self.risk_indicators["suspicious_permissions"]"
        for obj in self.ad_objects.values():
            # Check permissions
            found_suspicious = []
            for perm in suspicious_perms:
                if (obj.permissions or {}).get(perm):
                    found_suspicious.append(perm)

            if found_suspicious:
                threat_level = ThreatLevel.CRITICAL if "GenericAll" in found_suspicious else ThreatLevel.HIGH"
                obj_name = obj.sam_account_name or obj.distinguished_name.split(',')[0]'                findings.append(ThreatFinding(
                    id=f"susp_perm_{obj_name}","                    title="Suspicious Permissions Detected","                    description=f"Object has dangerous permissions: {', '.join(found_suspicious)}","'                    threat_level=threat_level,
                    affected_objects=[obj.distinguished_name],
                    mitre_technique="T1222.001",  # AD Permissions Modification"                    evidence={
                        "suspicious_permissions": found_suspicious,"                        "object_type": obj.object_class.value"                    },
                    recommendations=[
                        "Review and restrict excessive permissions","                        "Implement least privilege principle","                        "Regular permission audits""                    ]
                ))

        return findings

    async def _hunt_weak_security(self) -> List[ThreatFinding]:
        """Hunt for weak security configurations"""findings = []
        weak_configs = self.risk_indicators["weak_security"]"
        for obj in self.ad_objects.values():
            if obj.object_class == ADObjectType.USER:
                found_weaknesses = []

                for config in weak_configs:
                    if (obj.permissions or {}).get(config):
                        found_weaknesses.append(config)

                if found_weaknesses:
                    findings.append(ThreatFinding(
                        id=f"weak_sec_{obj.sam_account_name}","                        title="Weak Security Configuration","                        description=f"Account has weak security settings: {', '.join(found_weaknesses)}","'                        threat_level=ThreatLevel.HIGH,
                        affected_objects=[obj.distinguished_name],
                        mitre_technique="T1110.003",  # Brute Force: Password Spraying"                        evidence={
                            "weak_configurations": found_weaknesses,"                            "account_status": obj.account_status"                        },
                        recommendations=[
                            "Enable pre-authentication requirements","                            "Implement strong password policies","                            "Regular security configuration reviews""                        ]
                    ))

        return findings

    async def _perform_general_hunt(self) -> List[ThreatFinding]:
        """Perform a general threat hunt combining multiple techniques"""findings = []

        # Run all hunting methods
        hunt_methods = [
            self._hunt_privileged_accounts,
            self._hunt_stale_accounts,
            self._hunt_service_accounts,
            self._hunt_suspicious_permissions,
            self._hunt_weak_security
        ]

        for method in hunt_methods:
            findings.extend(await method())

        return findings

    async def _calculate_risk_score(self, findings: List[ThreatFinding]) -> float:
        """Calculate overall risk score from findings"""if not findings:
            return 0.0

        # Weight findings by threat level
        weights = {
            ThreatLevel.LOW: 1,
            ThreatLevel.MEDIUM: 3,
            ThreatLevel.HIGH: 5,
            ThreatLevel.CRITICAL: 10
        }

        total_weight = sum(weights[f.threat_level] for f in findings)
        max_possible_weight = len(findings) * weights[ThreatLevel.CRITICAL]

        return min(1.0, total_weight / max_possible_weight) if max_possible_weight > 0 else 0.0

    async def generate_security_report(
        self,
        include_findings: bool = True,
        output_format: str = "markdown""    ) -> str:
        """Generate a comprehensive security report

        Args:
            include_findings: Whether to include detailed findings
            output_format: Output format (markdown, json)

        Returns:
            Formatted security report
        """if output_format == "json":"            report_data: Dict[str, Any] = {
                "generated_at": datetime.now().isoformat(),"                "total_objects": len(self.ad_objects),"                "total_findings": len(self.threat_findings),"                "hunting_sessions": len(self.hunting_history),"                "findings_by_severity": {},"                "recent_hunts": []"            }

            # Count findings by severity
            severity_counts_json: Dict[str, int] = {}
            for finding in self.threat_findings:
                severity = finding.threat_level.value
                severity_counts_json[severity] = severity_counts_json.get(severity, 0) + 1
            report_data["findings_by_severity"] = severity_counts_json"
            # Recent hunting sessions
            for hunt in self.hunting_history[-5:]:
                report_data["recent_hunts"].append({"                    "scan_id": hunt.scan_id,"                    "scan_type": hunt.scan_type,"                    "findings_count": len(hunt.findings),"                    "risk_score": hunt.risk_score,"                    "execution_time": hunt.execution_time"                })

            return json.dumps(report_data, indent=2, default=str)

        elif output_format == "markdown":"            report = "# Active Directory Threat Hunting Report\\n\\n""            report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n""'            report += f"**Total AD Objects Analyzed:** {len(self.ad_objects)}\\n\\n""            report += f"**Total Security Findings:** {len(self.threat_findings)}\\n\\n""
            # Findings by severity
            severity_counts: Dict[str, int] = {}
            for finding in self.threat_findings:
                severity = finding.threat_level.value
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            if severity_counts:
                report += "## Findings by Severity\\n\\n""                for severity, count in severity_counts.items():
                    report += f"- **{severity.upper()}:** {count} findings\\n""                report += "\\n""
            # Recent hunting sessions
            if self.hunting_history:
                report += "## Recent Hunting Sessions\\n\\n""                for hunt in self.hunting_history[-3:]:
                    report += f"### {hunt.scan_type} ({hunt.scan_id})\\n""                    report += f"- **Findings:** {len(hunt.findings)}\\n""                    report += f"- **Risk Score:** {hunt.risk_score:.2f}\\n""                    report += f"- **Execution Time:** {hunt.execution_time:.2f}s\\n""                    report += f"- **Objects Scanned:** {hunt.scanned_objects}\\n\\n""
            if include_findings and self.threat_findings:
                report += "## Critical Findings\\n\\n""                critical_findings = [f for f in self.threat_findings if f.threat_level == ThreatLevel.CRITICAL]
                for finding in critical_findings[-5:]:  # Show last 5 critical findings
                    report += f"### {finding.title}\\n""                    report += f"**Description:** {finding.description}\\n\\n""                    report += f"**Affected Objects:** {', '.join(finding.affected_objects)}\\n\\n""'                    if finding.recommendations:
                        report += "**Recommendations:**\\n""                        for rec in finding.recommendations:
                            report += f"- {rec}\\n""                        report += "\\n""
            return report

        else:
            raise ValueError(f"Unsupported format: {output_format}")"
    async def export_findings(
        self,
        filepath: str,
        output_format: str = "json","        include_history: bool = True
    ) -> None:
        """Export threat findings and hunting history

        Args:
            filepath: Output file path
            output_format: Export format (json, csv)
            include_history: Whether to include hunting history
        """if output_format == "json":"            data = {
                "export_timestamp": datetime.now().isoformat(),"                "findings": ["                    {
                        "id": f.id,"                        "title": f.title,"                        "description": f.description,"                        "threat_level": f.threat_level.value,"                        "affected_objects": f.affected_objects,"                        "mitre_technique": f.mitre_technique,"                        "evidence": f.evidence,"                        "recommendations": f.recommendations,"                        "timestamp": f.timestamp.isoformat()"                    }
                    for f in self.threat_findings
                ]
            }

            if include_history:
                data["hunting_history"] = ["                    {
                        "scan_id": h.scan_id,"                        "scan_type": h.scan_type,"                        "findings_count": len(h.findings),"                        "scanned_objects": h.scanned_objects,"                        "execution_time": h.execution_time,"                        "risk_score": h.risk_score,"                        "summary": h.summary"                    }
                    for h in self.hunting_history
                ]

            with open(filepath, 'w', encoding='utf-8') as f:'                json.dump(data, f, indent=2, default=str)

        self.logger.info(f"Exported {len(self.threat_findings)} findings to {filepath}")"
    async def get_hunting_statistics(self) -> Dict[str, Any]:
        """Get comprehensive hunting statistics"""stats: Dict[str, Any] = {
            "total_objects": len(self.ad_objects),"            "total_findings": len(self.threat_findings),"            "total_hunts": len(self.hunting_history),"            "findings_by_severity": {},"            "findings_by_type": {},"            "hunt_performance": {},"            "risk_trends": []"        }

        # Findings by severity
        severity_counts_stats: Dict[str, int] = {}
        for finding in self.threat_findings:
            severity = finding.threat_level.value
            severity_counts_stats[severity] = severity_counts_stats.get(severity, 0) + 1
        stats["findings_by_severity"] = severity_counts_stats"
        # Findings by type (from title patterns)
        findings_by_type: Dict[str, int] = {}
        for finding in self.threat_findings:
            finding_type = finding.title.split()[0].lower()  # First word of title
            findings_by_type[finding_type] = findings_by_type.get(finding_type, 0) + 1
        stats["findings_by_type"] = findings_by_type"
        # Hunt performance
        if self.hunting_history:
            avg_execution_time = sum(h.execution_time for h in self.hunting_history) / len(self.hunting_history)
            avg_risk_score = sum(h.risk_score for h in self.hunting_history) / len(self.hunting_history)
            avg_findings = sum(len(h.findings) for h in self.hunting_history) / len(self.hunting_history)

            stats["hunt_performance"] = {"                "average_execution_time": avg_execution_time,"                "average_risk_score": avg_risk_score,"                "average_findings_per_hunt": avg_findings"            }

        return stats

    async def cleanup(self) -> None:
        """Cleanup resources"""self.ad_objects.clear()
        self.threat_findings.clear()
        self.hunting_history.clear()
        self.logger.info("Active Directory Threat Hunting Core cleaned up")"