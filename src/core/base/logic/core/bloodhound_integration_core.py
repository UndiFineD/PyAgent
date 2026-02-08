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

# BloodHound Integration Core - Graph-based Active Directory Security Analysis
# Based on patterns from AD_Miner repository

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ADObjectType(Enum):
    """Active Directory object types"""
    USER = "User"
    COMPUTER = "Computer"
    GROUP = "Group"
    DOMAIN = "Domain"
    OU = "OU"
    GPO = "GPO"


class SecurityControl(Enum):
    """Security controls that can be assessed"""
    DORMANT_ACCOUNTS = "dormant_accounts"
    GHOST_COMPUTERS = "ghost_computers"
    PASSWORD_NEVER_EXPIRES = "password_never_expires"
    OLD_PASSWORDS = "old_passwords"
    CLEARTEXT_PASSWORDS = "cleartext_passwords"
    KERBEROASTABLE = "kerberoastable"
    ASREP_ROASTABLE = "asrep_roastable"
    SID_HISTORY = "sid_history"
    LAPS_STATUS = "laps_status"
    UNCONSTRAINED_DELEGATION = "unconstrained_delegation"
    CONSTRAINED_DELEGATION = "constrained_delegation"
    DCSYNC_RIGHTS = "dcsync_rights"
    ADMIN_COUNT = "admin_count"
    RDP_ACCESS = "rdp_access"
    DOMAIN_ADMINS = "domain_admins"
    ENTERPRISE_ADMINS = "enterprise_admins"


@dataclass
class ADObject:
    """Represents an Active Directory object"""
    name: str
    object_type: ADObjectType
    distinguished_name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    risk_indicators: List[str] = field(default_factory=list)
    risk_score: float = 0.0


@dataclass
class SecurityFinding:
    """Represents a security finding"""
    control: SecurityControl
    title: str
    description: str
    risk_level: RiskLevel
    affected_objects: List[str]
    evidence: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ControlPath:
    """Represents a control path in the AD graph"""
    source: str
    target: str
    path: List[str]
    privileges: List[str] = field(default_factory=list)
    risk_score: float = 0.0


@dataclass
class AuditReport:
    """Comprehensive audit report"""
    report_id: str
    domain: str
    generated_at: datetime
    total_objects: int
    findings: List[SecurityFinding]
    control_paths: List[ControlPath]
    risk_summary: Dict[str, int] = field(default_factory=dict)
    evolution_data: Optional[Dict[str, Any]] = None
    statistics: Dict[str, Any] = field(default_factory=dict)


class BloodHoundIntegrationCore:
    """
    BloodHound Integration Core for graph-based Active Directory security analysis.

    Provides comprehensive AD security assessment using graph database patterns,
    risk analysis, and security control evaluation based on AD_Miner methodologies.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ad_objects: Dict[str, ADObject] = {}
        self.findings: List[SecurityFinding] = []
        self.control_paths: List[ControlPath] = []
        self.audit_history: List[AuditReport] = []
        self.baseline_config: Dict[str, Any] = {}
        self.cypher_queries: Dict[str, str] = {}

    async def initialize(self) -> bool:
        """Initialize the BloodHound integration core"""
        try:
            # Initialize baseline security configurations
            await self.load_baseline_config()
            await self.load_cypher_queries()
            self.logger.info("BloodHound Integration Core initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize BloodHound Integration Core: {e}")
            return False

    async def load_baseline_config(self) -> None:
        """Load baseline security configurations"""
        self.baseline_config = {
            "password_renewal_days": 90,
            "dormant_account_threshold_days": 90,
            "old_password_threshold_days": 180,
            "krbtgt_password_max_age_days": 365,
            "min_domain_admins": 2,
            "max_domain_admins": 10,
            "tier_0_groups": [
                "Domain Admins",
                "Enterprise Admins",
                "Schema Admins",
                "Administrators"
            ],
            "high_privilege_groups": [
                "Domain Admins",
                "Enterprise Admins",
                "Schema Admins",
                "Administrators",
                "Account Operators",
                "Backup Operators",
                "Print Operators",
                "Server Operators"
            ]
        }

        self.logger.info("Loaded baseline security configurations")

    async def load_cypher_queries(self) -> None:
        """Load Cypher queries for AD analysis"""
        self.cypher_queries = {
            "dormant_accounts": """
                MATCH (u:User)
                WHERE u.lastlogon < $threshold_date AND u.enabled = true
                RETURN u.name, u.distinguishedname, u.lastlogon
            """,
            "password_never_expires": """
                MATCH (u:User)
                WHERE u.passwordneverexpires = true AND u.enabled = true
                RETURN u.name, u.distinguishedname
            """,
            "kerberoastable_accounts": """
                MATCH (u:User)
                WHERE u.hasspn = true AND u.enabled = true
                RETURN u.name, u.distinguishedname, u.serviceprincipalnames
            """,
            "asrep_roastable_accounts": """
                MATCH (u:User)
                WHERE u.dontreqpreauth = true AND u.enabled = true
                RETURN u.name, u.distinguishedname
            """,
            "unconstrained_delegation": """
                MATCH (c:Computer)
                WHERE c.unconstraineddelegation = true
                RETURN c.name, c.distinguishedname
            """,
            "domain_admins": """
                MATCH (u:User)-[:MemberOf*1..]->(g:Group)
                WHERE g.name = 'DOMAIN ADMINS@DOMAIN.COM'
                RETURN u.name, u.distinguishedname
            """,
            "control_paths_to_da": """
                MATCH p=shortestPath((u:User)-[:MemberOf|HasSession|AdminTo|AllExtendedRights|GenericAll|GenericWrite|WriteDACL|WriteOwner*1..]->(da:Group))
                WHERE da.name = 'DOMAIN ADMINS@DOMAIN.COM'
                RETURN p
            """
        }

        self.logger.info(f"Loaded {len(self.cypher_queries)} Cypher queries")

    async def load_ad_data(self, neo4j_connection: Dict[str, Any], use_cache: bool = True) -> bool:
        """
        Load Active Directory data from Neo4j/BloodHound

        Args:
            neo4j_connection: Neo4j connection parameters
            use_cache: Whether to use cached data

        Returns:
            True if successful, False otherwise
        """
        try:
            # Mock Neo4j connection and data loading
            # In real implementation, this would connect to actual Neo4j database
            await self._mock_load_ad_objects()
            self.logger.info(f"Loaded {len(self.ad_objects)} AD objects")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load AD data: {e}")
            return False

    async def _mock_load_ad_objects(self) -> None:
        """Load mock AD objects for demonstration"""
        # Mock users
        users = [
            ADObject(
                name="Administrator",
                object_type=ADObjectType.USER,
                distinguished_name="CN=Administrator,CN=Users,DC=domain,DC=com",
                properties={
                    "enabled": True,
                    "lastlogon": datetime.now() - timedelta(days=1),
                    "passwordlastset": datetime.now() - timedelta(days=30),
                    "passwordneverexpires": False,
                    "hasspn": False,
                    "dontreqpreauth": False
                },
                relationships={
                    "MemberOf": ["Domain Admins", "Administrators"]
                }
            ),
            ADObject(
                name="jsmith",
                object_type=ADObjectType.USER,
                distinguished_name="CN=John Smith,CN=Users,DC=domain,DC=com",
                properties={
                    "enabled": True,
                    "lastlogon": datetime.now() - timedelta(days=120),  # Dormant
                    "passwordlastset": datetime.now() - timedelta(days=200),  # Old password
                    "passwordneverexpires": True,  # Never expires
                    "hasspn": True,  # Kerberoastable
                    "dontreqpreauth": False
                },
                relationships={
                    "MemberOf": ["Domain Users"]
                }
            ),
            ADObject(
                name="svc-sql",
                object_type=ADObjectType.USER,
                distinguished_name="CN=svc-sql,CN=Users,DC=domain,DC=com",
                properties={
                    "enabled": True,
                    "lastlogon": datetime.now() - timedelta(days=1),
                    "passwordlastset": datetime.now() - timedelta(days=400),
                    "passwordneverexpires": False,
                    "hasspn": True,
                    "dontreqpreauth": False
                },
                relationships={
                    "MemberOf": ["Service Accounts"]
                }
            )
        ]

        # Mock computers
        computers = [
            ADObject(
                name="DC01",
                object_type=ADObjectType.COMPUTER,
                distinguished_name="CN=DC01,OU=Domain Controllers,DC=domain,DC=com",
                properties={
                    "operatingsystem": "Windows Server 2022",
                    "unconstraineddelegation": False
                }
            ),
            ADObject(
                name="WORKSTATION01",
                object_type=ADObjectType.COMPUTER,
                distinguished_name="CN=WORKSTATION01,CN=Computers,DC=domain,DC=com",
                properties={
                    "operatingsystem": "Windows 10",
                    "unconstraineddelegation": True  # Vulnerable
                }
            )
        ]

        # Mock groups
        groups = [
            ADObject(
                name="Domain Admins",
                object_type=ADObjectType.GROUP,
                distinguished_name="CN=Domain Admins,CN=Users,DC=domain,DC=com",
                properties={
                    "admincount": 1
                },
                relationships={
                    "Member": ["Administrator"]
                }
            )
        ]

        # Store all objects
        for obj in users + computers + groups:
            self.ad_objects[obj.distinguished_name] = obj

    async def perform_security_audit(
        self,
        controls: Optional[List[SecurityControl]] = None,
        domain: str = "domain.com"
    ) -> AuditReport:
        """
        Perform comprehensive security audit

        Args:
            controls: Specific controls to check, None for all
            domain: Domain to audit

        Returns:
            Comprehensive audit report
        """
        start_time = datetime.now()
        findings = []

        # Select controls to run
        controls_to_run = controls or list(SecurityControl)

        # Run each control
        for control in controls_to_run:
            control_findings = await self._run_security_control(control)
            findings.extend(control_findings)

        # Analyze control paths
        control_paths = await self._analyze_control_paths()

        # Calculate risk summary
        risk_summary = {}
        for finding in findings:
            risk_level = finding.risk_level.value
            risk_summary[risk_level] = risk_summary.get(risk_level, 0) + 1

        # Generate statistics
        statistics = {
            "total_objects": len(self.ad_objects),
            "total_findings": len(findings),
            "total_control_paths": len(control_paths),
            "audit_duration": (datetime.now() - start_time).total_seconds(),
            "objects_by_type": {}
        }

        # Count objects by type
        for obj in self.ad_objects.values():
            obj_type = obj.object_type.value
            statistics["objects_by_type"][obj_type] = statistics["objects_by_type"].get(obj_type, 0) + 1

        # Create report
        report = AuditReport(
            report_id=f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            domain=domain,
            generated_at=datetime.now(),
            total_objects=len(self.ad_objects),
            findings=findings,
            control_paths=control_paths,
            risk_summary=risk_summary,
            statistics=statistics
        )

        self.audit_history.append(report)
        self.findings.extend(findings)
        self.control_paths.extend(control_paths)

        self.logger.info(f"Completed security audit: {len(findings)} findings, {len(control_paths)} control paths")
        return report

    async def _run_security_control(self, control: SecurityControl) -> List[SecurityFinding]:
        """Run a specific security control"""
        findings = []

        if control == SecurityControl.DORMANT_ACCOUNTS:
            findings.extend(await self._check_dormant_accounts())
        elif control == SecurityControl.PASSWORD_NEVER_EXPIRES:
            findings.extend(await self._check_password_never_expires())
        elif control == SecurityControl.KERBEROASTABLE:
            findings.extend(await self._check_kerberoastable_accounts())
        elif control == SecurityControl.ASREP_ROASTABLE:
            findings.extend(await self._check_asrep_roastable_accounts())
        elif control == SecurityControl.UNCONSTRAINED_DELEGATION:
            findings.extend(await self._check_unconstrained_delegation())
        elif control == SecurityControl.DOMAIN_ADMINS:
            findings.extend(await self._check_domain_admins())
        elif control == SecurityControl.OLD_PASSWORDS:
            findings.extend(await self._check_old_passwords())
        # Add more controls as needed

        return findings

    async def _check_dormant_accounts(self) -> List[SecurityFinding]:
        """Check for dormant/inactive accounts"""
        findings = []
        threshold_days = self.baseline_config["dormant_account_threshold_days"]
        threshold_date = datetime.now() - timedelta(days=threshold_days)

        for obj in self.ad_objects.values():
            if obj.object_type == ADObjectType.USER:
                last_logon = obj.properties.get("lastlogon")
                if last_logon and isinstance(last_logon, datetime) and last_logon < threshold_date:
                    days_dormant = (datetime.now() - last_logon).days

                    findings.append(SecurityFinding(
                        control=SecurityControl.DORMANT_ACCOUNTS,
                        title="Dormant Account Detected",
                        description=f"Account {obj.name} has not logged in for {days_dormant} days",
                        risk_level=RiskLevel.MEDIUM,
                        affected_objects=[obj.distinguished_name],
                        evidence={
                            "last_logon": last_logon.isoformat(),
                            "days_dormant": days_dormant,
                            "threshold_days": threshold_days
                        },
                        recommendations=[
                            "Review account necessity",
                            "Disable or remove dormant accounts",
                            "Implement automated account lifecycle management"
                        ]
                    ))

        return findings

    async def _check_password_never_expires(self) -> List[SecurityFinding]:
        """Check for accounts with passwords that never expire"""
        findings = []

        for obj in self.ad_objects.values():
            if (obj.object_type == ADObjectType.USER and
                obj.properties.get("passwordneverexpires", False)):

                findings.append(SecurityFinding(
                    control=SecurityControl.PASSWORD_NEVER_EXPIRES,
                    title="Password Never Expires",
                    description=f"Account {obj.name} has a password that never expires",
                    risk_level=RiskLevel.HIGH,
                    affected_objects=[obj.distinguished_name],
                    evidence={
                        "password_never_expires": True,
                        "account_enabled": obj.properties.get("enabled", True)
                    },
                    recommendations=[
                        "Configure password expiration policy",
                        "Implement regular password rotation",
                        "Review service account password policies"
                    ]
                ))

        return findings

    async def _check_kerberoastable_accounts(self) -> List[SecurityFinding]:
        """Check for Kerberoastable accounts (accounts with SPNs)"""
        findings = []

        for obj in self.ad_objects.values():
            if (obj.object_type == ADObjectType.USER and
                obj.properties.get("hasspn", False)):

                spns = obj.properties.get("serviceprincipalnames", [])

                findings.append(SecurityFinding(
                    control=SecurityControl.KERBEROASTABLE,
                    title="Kerberoastable Account",
                    description=f"Account {obj.name} has service principal names and is vulnerable to Kerberoasting",
                    risk_level=RiskLevel.HIGH,
                    affected_objects=[obj.distinguished_name],
                    evidence={
                        "service_principal_names": spns,
                        "has_spn": True
                    },
                    recommendations=[
                        "Use strong service account passwords",
                        "Consider using Group Managed Service Accounts (gMSA)",
                        "Limit service account privileges"
                    ]
                ))

        return findings

    async def _check_asrep_roastable_accounts(self) -> List[SecurityFinding]:
        """Check for AS-REP roastable accounts (don't require pre-auth)"""
        findings = []

        for obj in self.ad_objects.values():
            if (obj.object_type == ADObjectType.USER and
                obj.properties.get("dontreqpreauth", False)):

                findings.append(SecurityFinding(
                    control=SecurityControl.ASREP_ROASTABLE,
                    title="AS-REP Roastable Account",
                    description=f"Account {obj.name} doesn't require pre-authentication and is vulnerable to AS-REP roasting",
                    risk_level=RiskLevel.HIGH,
                    affected_objects=[obj.distinguished_name],
                    evidence={
                        "dont_require_preauth": True,
                        "account_enabled": obj.properties.get("enabled", True)
                    },
                    recommendations=[
                        "Enable pre-authentication requirement",
                        "Use strong passwords for vulnerable accounts",
                        "Monitor for AS-REP roasting attempts"
                    ]
                ))

        return findings

    async def _check_unconstrained_delegation(self) -> List[SecurityFinding]:
        """Check for computers with unconstrained delegation"""
        findings = []

        for obj in self.ad_objects.values():
            if (obj.object_type == ADObjectType.COMPUTER and
                obj.properties.get("unconstraineddelegation", False)):

                findings.append(SecurityFinding(
                    control=SecurityControl.UNCONSTRAINED_DELEGATION,
                    title="Unconstrained Delegation Enabled",
                    description=f"Computer {obj.name} has unconstrained delegation enabled",
                    risk_level=RiskLevel.CRITICAL,
                    affected_objects=[obj.distinguished_name],
                    evidence={
                        "unconstrained_delegation": True,
                        "operating_system": obj.properties.get("operatingsystem")
                    },
                    recommendations=[
                        "Disable unconstrained delegation",
                        "Use constrained delegation instead",
                        "Limit delegation to trusted services only"
                    ]
                ))

        return findings

    async def _check_domain_admins(self) -> List[SecurityFinding]:
        """Check domain admin group membership"""
        findings = []
        domain_admins = []

        # Find domain admins group
        da_group = None
        for obj in self.ad_objects.values():
            if (obj.object_type == ADObjectType.GROUP and
                "Domain Admins" in obj.name):
                da_group = obj
                domain_admins = obj.relationships.get("Member", [])
                break

        if da_group:
            admin_count = len(domain_admins)
            min_admins = self.baseline_config["min_domain_admins"]
            max_admins = self.baseline_config["max_domain_admins"]

            if admin_count < min_admins:
                findings.append(SecurityFinding(
                    control=SecurityControl.DOMAIN_ADMINS,
                    title="Insufficient Domain Administrators",
                    description=f"Only {admin_count} domain administrators found (minimum recommended: {min_admins})",
                    risk_level=RiskLevel.MEDIUM,
                    affected_objects=[da_group.distinguished_name],
                    evidence={
                        "admin_count": admin_count,
                        "min_recommended": min_admins,
                        "domain_admins": domain_admins
                    },
                    recommendations=[
                        "Ensure adequate number of domain administrators",
                        "Implement emergency admin accounts",
                        "Use privileged access management"
                    ]
                ))
            elif admin_count > max_admins:
                findings.append(SecurityFinding(
                    control=SecurityControl.DOMAIN_ADMINS,
                    title="Excessive Domain Administrators",
                    description=f"{admin_count} domain administrators found (maximum recommended: {max_admins})",
                    risk_level=RiskLevel.MEDIUM,
                    affected_objects=[da_group.distinguished_name],
                    evidence={
                        "admin_count": admin_count,
                        "max_recommended": max_admins,
                        "domain_admins": domain_admins
                    },
                    recommendations=[
                        "Review domain admin memberships",
                        "Implement just-in-time access",
                        "Use role-based access control"
                    ]
                ))

        return findings

    async def _check_old_passwords(self) -> List[SecurityFinding]:
        """Check for accounts with old passwords"""
        findings = []
        threshold_days = self.baseline_config["old_password_threshold_days"]
        threshold_date = datetime.now() - timedelta(days=threshold_days)

        for obj in self.ad_objects.values():
            if obj.object_type == ADObjectType.USER:
                pwd_last_set = obj.properties.get("passwordlastset")
                if pwd_last_set and isinstance(pwd_last_set, datetime) and pwd_last_set < threshold_date:
                    days_old = (datetime.now() - pwd_last_set).days

                    findings.append(SecurityFinding(
                        control=SecurityControl.OLD_PASSWORDS,
                        title="Old Password Detected",
                        description=f"Account {obj.name} has a password that is {days_old} days old",
                        risk_level=RiskLevel.MEDIUM,
                        affected_objects=[obj.distinguished_name],
                        evidence={
                            "password_last_set": pwd_last_set.isoformat(),
                            "days_old": days_old,
                            "threshold_days": threshold_days
                        },
                        recommendations=[
                            "Enforce password rotation policies",
                            "Implement password aging requirements",
                            "Use multi-factor authentication"
                        ]
                    ))

        return findings

    async def _analyze_control_paths(self) -> List[ControlPath]:
        """Analyze control paths in the AD graph"""
        control_paths = []

        # Mock control path analysis
        # In real implementation, this would use graph algorithms

        # Example: Path from user to domain admin
        user_obj = None
        da_group = None

        for obj in self.ad_objects.values():
            if obj.object_type == ADObjectType.USER and obj.name == "jsmith":
                user_obj = obj
            elif obj.object_type == ADObjectType.GROUP and "Domain Admins" in obj.name:
                da_group = obj

        if user_obj and da_group:
            # Mock path: user -> some group -> domain admins
            control_paths.append(ControlPath(
                source=user_obj.distinguished_name,
                target=da_group.distinguished_name,
                path=[
                    user_obj.distinguished_name,
                    "CN=Some Group,CN=Users,DC=domain,DC=com",
                    da_group.distinguished_name
                ],
                privileges=["MemberOf"],
                risk_score=7.5
            ))

        return control_paths

    async def generate_audit_report(
        self,
        report: AuditReport,
        format: str = "json",
        include_evolution: bool = False
    ) -> str:
        """
        Generate audit report in specified format

        Args:
            report: Audit report to format
            format: Output format (json, html)
            include_evolution: Include evolution data

        Returns:
            Formatted report
        """
        if format == "json":
            report_data = {
                "report_id": report.report_id,
                "domain": report.domain,
                "generated_at": report.generated_at.isoformat(),
                "total_objects": report.total_objects,
                "findings": [
                    {
                        "control": f.control.value,
                        "title": f.title,
                        "description": f.description,
                        "risk_level": f.risk_level.value,
                        "affected_objects": f.affected_objects,
                        "evidence": f.evidence,
                        "recommendations": f.recommendations,
                        "timestamp": f.timestamp.isoformat()
                    }
                    for f in report.findings
                ],
                "control_paths": [
                    {
                        "source": cp.source,
                        "target": cp.target,
                        "path": cp.path,
                        "privileges": cp.privileges,
                        "risk_score": cp.risk_score
                    }
                    for cp in report.control_paths
                ],
                "risk_summary": report.risk_summary,
                "statistics": report.statistics
            }

            if include_evolution and report.evolution_data:
                report_data["evolution_data"] = report.evolution_data

            return json.dumps(report_data, indent=2, default=str)

        elif format == "html":
            # Generate basic HTML report
            html = f"""
            <html>
            <head><title>AD Security Audit Report - {report.domain}</title></head>
            <body>
                <h1>Active Directory Security Audit Report</h1>
                <p><strong>Domain:</strong> {report.domain}</p>
                <p><strong>Generated:</strong> {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Total Objects:</strong> {report.total_objects}</p>

                <h2>Risk Summary</h2>
                <ul>
            """

            for risk_level, count in report.risk_summary.items():
                html += f"<li><strong>{risk_level.upper()}:</strong> {count} findings</li>"

            html += """
                </ul>

                <h2>Critical Findings</h2>
                <ul>
            """

            critical_findings = [f for f in report.findings if f.risk_level == RiskLevel.CRITICAL]
            for finding in critical_findings[:10]:  # Limit to first 10
                html += f"""
                <li>
                    <strong>{finding.title}</strong><br>
                    {finding.description}<br>
                    <em>Affected: {', '.join(finding.affected_objects)}</em>
                </li>
                """

            html += """
                </ul>
            </body>
            </html>
            """

            return html

        else:
            raise ValueError(f"Unsupported format: {format}")

    async def export_report(
        self,
        report: AuditReport,
        filepath: str,
        format: str = "json"
    ) -> None:
        """
        Export audit report to file

        Args:
            report: Report to export
            filepath: Output file path
            format: Export format
        """
        report_content = await self.generate_audit_report(report, format)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)

        self.logger.info(f"Exported audit report to {filepath}")

    async def get_audit_statistics(self) -> Dict[str, Any]:
        """Get comprehensive audit statistics"""
        stats = {
            "total_audits": len(self.audit_history),
            "total_findings": len(self.findings),
            "total_control_paths": len(self.control_paths),
            "findings_by_control": {},
            "findings_by_risk": {},
            "audit_trends": [],
            "most_common_issues": []
        }

        # Findings by control
        for finding in self.findings:
            control = finding.control.value
            stats["findings_by_control"][control] = stats["findings_by_control"].get(control, 0) + 1

        # Findings by risk level
        for finding in self.findings:
            risk = finding.risk_level.value
            stats["findings_by_risk"][risk] = stats["findings_by_risk"].get(risk, 0) + 1

        # Audit trends
        for audit in self.audit_history[-10:]:  # Last 10 audits
            stats["audit_trends"].append({
                "date": audit.generated_at.isoformat(),
                "findings": len(audit.findings),
                "high_risk": len([f for f in audit.findings if f.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
            })

        # Most common issues
        issue_counts = {}
        for finding in self.findings:
            issue = finding.title
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

        stats["most_common_issues"] = sorted(
            [{"issue": k, "count": v} for k, v in issue_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]  # Top 10

        return stats

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.ad_objects.clear()
        self.findings.clear()
        self.control_paths.clear()
        self.audit_history.clear()
        self.logger.info("BloodHound Integration Core cleaned up")