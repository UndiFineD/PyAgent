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

# Active Directory Attack & Defense Core - AD Kill Chain Analysis
# Based on patterns from AD-Attack-Defense repository

import json
import logging
from typing import Dict, List, Optional, Any, cast
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class KillChainPhase(Enum):
    """Active Directory Kill Chain phases"""RECONNAISSANCE = "reconnaissance""    WEAPONIZATION = "weaponization""    DELIVERY = "delivery""    EXPLOITATION = "exploitation""    INSTALLATION = "installation""    COMMAND_AND_CONTROL = "command_and_control""    PRIVILEGE_ESCALATION = "privilege_escalation""    PERSISTENCE = "persistence""    CREDENTIAL_DUMPING = "credential_dumping""    LATERAL_MOVEMENT = "lateral_movement""    ACTIONS_ON_OBJECTIVES = "actions_on_objectives""

class AttackTechnique(Enum):
    """Common AD attack techniques"""KERBEROASTING = "kerberoasting""    ASREP_ROASTING = "asrep_roasting""    PASS_THE_HASH = "pass_the_hash""    PASS_THE_TICKET = "pass_the_ticket""    GOLDEN_TICKET = "golden_ticket""    SILVER_TICKET = "silver_ticket""    DCSYNC = "dcsync""    DC_SHADOW = "dc_shadow""    UNCONSTRAINED_DELEGATION = "unconstrained_delegation""    CONSTRAINED_DELEGATION = "constrained_delegation""    RESOURCE_BASED_CONSTRAINED_DELEGATION = "resource_based_constrained_delegation""    GPO_ABUSE = "gpo_abuse""    ACL_ABUSE = "acl_abuse""    TRUST_EXPLOITATION = "trust_exploitation""    LAPS_ABUSE = "laps_abuse""    SYSVOL_CREDENTIALS = "sysvol_credentials""    DNSADMIN_ESCALATION = "dnsadmin_escalation""

class DefenseControl(Enum):
    """Defense and detection controls"""MULTI_FACTOR_AUTH = "multi_factor_auth""    LEAST_PRIVILEGE = "least_privilege""    REGULAR_AUDITS = "regular_audits""    LOGGING_MONITORING = "logging_monitoring""    PATCH_MANAGEMENT = "patch_management""    NETWORK_SEGMENTATION = "network_segmentation""    ENDPOINT_PROTECTION = "endpoint_protection""    ANOMALY_DETECTION = "anomaly_detection""

@dataclass
class AttackVector:
    """Represents an attack vector in AD"""technique: AttackTechnique
    phase: KillChainPhase
    prerequisites: List[str] = field(default_factory=list)
    impact: str = """    detection_difficulty: str = "medium""    mitigation_complexity: str = "medium""    affected_components: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)


@dataclass
class DefenseAssessment:
    """Assessment of defensive controls"""control: DefenseControl
    implemented: bool = False
    effectiveness: str = "unknown"  # high, medium, low, unknown"    coverage: str = "partial"  # full, partial, minimal, none"    last_assessed: Optional[datetime] = None
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class KillChainAnalysis:
    """Analysis of AD kill chain progression"""analysis_id: str
    domain: str
    start_time: datetime
    phases_completed: List[KillChainPhase] = field(default_factory=list)
    techniques_used: List[AttackTechnique] = field(default_factory=list)
    defenses_bypassed: List[DefenseControl] = field(default_factory=list)
    risk_score: float = 0.0
    time_to_compromise: Optional[float] = None  # minutes
    attack_path: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SecurityPosture:
    """Overall AD security posture assessment"""assessment_id: str
    domain: str
    assessment_date: datetime
    overall_score: float  # 0-100, higher is better
    attack_vectors: List[AttackVector] = field(default_factory=list)
    defense_assessments: List[DefenseAssessment] = field(default_factory=list)
    kill_chain_analyses: List[KillChainAnalysis] = field(default_factory=list)
    critical_gaps: List[str] = field(default_factory=list)
    priority_actions: List[str] = field(default_factory=list)


class ActiveDirectoryAttackDefenseCore:
    """Active Directory Attack & Defense Core for comprehensive AD security analysis.

    Provides kill chain analysis, attack simulation, defense assessment,
    and security posture evaluation based on AD-Attack-Defense methodologies.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.attack_vectors: Dict[AttackTechnique, AttackVector] = {}
        self.defense_assessments: Dict[DefenseControl, DefenseAssessment] = {}
        self.kill_chain_analyses: List[KillChainAnalysis] = []
        self.security_postures: Dict[str, SecurityPosture] = {}

    async def initialize(self) -> bool:
        """Initialize the AD attack & defense core"""try:
            await self.load_attack_vectors()
            await self.initialize_defense_assessments()
            self.logger.info("Active Directory Attack & Defense Core initialized successfully")"            return True
        except Exception:  # noqa: BLE001
            self.logger.exception("Failed to initialize Active Directory Attack & Defense Core")"            return False

    async def load_attack_vectors(self) -> None:
        """Load comprehensive attack vectors database"""self.attack_vectors = {
            AttackTechnique.KERBEROASTING: AttackVector(
                technique=AttackTechnique.KERBEROASTING,
                phase=KillChainPhase.RECONNAISSANCE,
                prerequisites=["Domain user account", "Service accounts with SPNs"],"                impact="Credential harvesting for offline cracking","                detection_difficulty="low","                mitigation_complexity="medium","                affected_components=["Kerberos", "Service Accounts"],"                indicators=[
                    "TGS-REQ requests for service accounts","                    "Unusual account enumeration patterns","                    "Offline password cracking attempts""                ],
                mitigations=[
                    "Use strong, complex service account passwords","                    "Implement Group Managed Service Accounts (gMSA)","                    "Monitor for unusual Kerberos ticket requests""                ]
            ),

            AttackTechnique.ASREP_ROASTING: AttackVector(
                technique=AttackTechnique.ASREP_ROASTING,
                phase=KillChainPhase.RECONNAISSANCE,
                prerequisites=["Accounts with DONT_REQ_PREAUTH flag"],"                impact="Credential harvesting without pre-authentication","                detection_difficulty="low","                mitigation_complexity="low","                affected_components=["Kerberos", "Account Settings"],"                indicators=[
                    "AS-REQ requests without pre-authentication","                    "Accounts with DONT_REQ_PREAUTH set""                ],
                mitigations=[
                    "Remove DONT_REQ_PREAUTH from accounts","                    "Use strong passwords for vulnerable accounts","                    "Monitor Kerberos pre-authentication failures""                ]
            ),

            AttackTechnique.UNCONSTRAINED_DELEGATION: AttackVector(
                technique=AttackTechnique.UNCONSTRAINED_DELEGATION,
                phase=KillChainPhase.PRIVILEGE_ESCALATION,
                prerequisites=["Unconstrained delegation configured on computers"],"                impact="Complete domain compromise via ticket forwarding","                detection_difficulty="medium","                mitigation_complexity="medium","                affected_components=["Kerberos", "Computer Objects"],"                indicators=[
                    "TRUSTED_FOR_DELEGATION flag on computer accounts","                    "TGT forwarding to unauthorized services""                ],
                mitigations=[
                    "Use constrained delegation instead","                    "Limit delegation to trusted services only","                    "Monitor for unusual delegation patterns""                ]
            ),

            AttackTechnique.CONSTRAINED_DELEGATION: AttackVector(
                technique=AttackTechnique.CONSTRAINED_DELEGATION,
                phase=KillChainPhase.PRIVILEGE_ESCALATION,
                prerequisites=["Constrained delegation configured", "Service account compromise"],"                impact="Service ticket impersonation","                detection_difficulty="high","                mitigation_complexity="medium","                affected_components=["Kerberos", "Service Accounts"],"                indicators=[
                    "S4U2self/S4U2proxy usage","                    "Service tickets for unauthorized services""                ],
                mitigations=[
                    "Use resource-based constrained delegation","                    "Limit service ticket scope","                    "Monitor S4U extensions usage""                ]
            ),

            AttackTechnique.GPO_ABUSE: AttackVector(
                technique=AttackTechnique.GPO_ABUSE,
                phase=KillChainPhase.PERSISTENCE,
                prerequisites=["GPO edit permissions", "Domain user account"],"                impact="Persistent code execution via group policy","                detection_difficulty="medium","                mitigation_complexity="low","                affected_components=["Group Policy", "SYSVOL"],"                indicators=[
                    "Unauthorized GPO modifications","                    "New scheduled tasks in GPOs","                    "Modified login scripts""                ],
                mitigations=[
                    "Restrict GPO creation/modification permissions","                    "Audit GPO changes","                    "Use GPO delegation carefully""                ]
            ),

            AttackTechnique.ACL_ABUSE: AttackVector(
                technique=AttackTechnique.ACL_ABUSE,
                phase=KillChainPhase.PRIVILEGE_ESCALATION,
                prerequisites=["Excessive permissions on AD objects"],"                impact="Privilege escalation via access rights","                detection_difficulty="high","                mitigation_complexity="high","                affected_components=["Access Control Lists", "AD Objects"],"                indicators=[
                    "GenericAll/GenericWrite permissions on sensitive objects","                    "DCSync rights on non-admin accounts""                ],
                mitigations=[
                    "Implement least privilege principle","                    "Regular ACL audits","                    "Use tiered administration model""                ]
            ),

            AttackTechnique.DCSYNC: AttackVector(
                technique=AttackTechnique.DCSYNC,
                phase=KillChainPhase.CREDENTIAL_DUMPING,
                prerequisites=["Replicating Directory Changes permissions"],"                impact="Complete domain credential extraction","                detection_difficulty="medium","                mitigation_complexity="medium","                affected_components=["Directory Replication", "Domain Controllers"],"                indicators=[
                    "DS-Replication-Get-Changes requests","                    "Unusual replication traffic""                ],
                mitigations=[
                    "Limit replication permissions","                    "Monitor for unusual replication requests","                    "Use Protected Users group""                ]
            ),

            AttackTechnique.GOLDEN_TICKET: AttackVector(
                technique=AttackTechnique.GOLDEN_TICKET,
                phase=KillChainPhase.LATERAL_MOVEMENT,
                prerequisites=["KRBTGT hash compromise"],"                impact="Persistent domain-wide access","                detection_difficulty="high","                mitigation_complexity="medium","                affected_components=["Kerberos", "Domain Controllers"],"                indicators=[
                    "Tickets with unrealistic lifetimes","                    "TGT requests without recent AS requests""                ],
                mitigations=[
                    "Regular KRBTGT password changes","                    "Monitor for anomalous ticket patterns","                    "Implement PAC validation""                ]
            ),

            AttackTechnique.TRUST_EXPLOITATION: AttackVector(
                technique=AttackTechnique.TRUST_EXPLOITATION,
                phase=KillChainPhase.PRIVILEGE_ESCALATION,
                prerequisites=["Domain/forest trust relationships"],"                impact="Cross-domain/forest compromise","                detection_difficulty="medium","                mitigation_complexity="high","                affected_components=["Domain Trusts", "Forest Trusts"],"                indicators=[
                    "SID history usage","                    "Cross-domain ticket requests""                ],
                mitigations=[
                    "Selective authentication on trusts","                    "SID filtering","                    "Regular trust audits""                ]
            ),

            AttackTechnique.LAPS_ABUSE: AttackVector(
                technique=AttackTechnique.LAPS_ABUSE,
                phase=KillChainPhase.CREDENTIAL_DUMPING,
                prerequisites=["LAPS read permissions on computer objects"],"                impact="Local admin password retrieval","                detection_difficulty="low","                mitigation_complexity="low","                affected_components=["LAPS", "Computer Objects"],"                indicators=[
                    "LDAP queries for ms-Mcs-AdmPwd attribute","                    "Access to LAPS passwords""                ],
                mitigations=[
                    "Restrict LAPS password read permissions","                    "Audit LAPS password access","                    "Use just-in-time access for local admin""                ]
            )
        }

        self.logger.info(f"Loaded {len(self.attack_vectors)} attack vectors")"
    async def initialize_defense_assessments(self) -> None:
        """Initialize defense control assessments"""for control in DefenseControl:
            self.defense_assessments[control] = DefenseAssessment(
                control=control,
                implemented=False,
                effectiveness="unknown","                coverage="none""            )

        self.logger.info("Initialized defense control assessments")"
    async def assess_security_posture(
        self,
        domain: str,
        ad_configuration: Optional[Dict[str, Any]] = None
    ) -> SecurityPosture:
        """Perform comprehensive security posture assessment

        Args:
            domain: Domain to assess
            ad_configuration: AD configuration data

        Returns:
            Security posture assessment
        """
        # Analyze attack vectors
        attack_vectors = await self.analyze_attack_vectors(ad_configuration or {})

        # Assess defenses
        defense_assessments = await self.assess_defenses(ad_configuration or {})

        # Perform kill chain analysis
        kill_chain_analyses = await self.analyze_kill_chains(attack_vectors)

        # Calculate overall score
        overall_score = await self.calculate_overall_score(attack_vectors, defense_assessments)

        # Identify critical gaps
        critical_gaps = await self.identify_critical_gaps(attack_vectors, defense_assessments)

        # Generate priority actions
        priority_actions = await self.generate_priority_actions(critical_gaps, defense_assessments)

        posture = SecurityPosture(
            assessment_id=f"posture_{datetime.now().strftime('%Y%m%d_%H%M%S')}","'            domain=domain,
            assessment_date=datetime.now(),
            overall_score=overall_score,
            attack_vectors=attack_vectors,
            defense_assessments=list(defense_assessments.values()),
            kill_chain_analyses=kill_chain_analyses,
            critical_gaps=critical_gaps,
            priority_actions=priority_actions
        )

        self.security_postures[domain] = posture

        self.logger.info(f"Completed security posture assessment for {domain}: score {overall_score:.1f}")"        return posture

    async def analyze_attack_vectors(self, ad_config: Dict[str, Any]) -> List[AttackVector]:
        """Analyze applicable attack vectors based on AD configuration"""applicable_vectors = []

        # Mock analysis based on configuration
        # In real implementation, this would analyze actual AD data

        # Check for unconstrained delegation
        if ad_config.get("unconstrained_delegation_enabled", True):"            applicable_vectors.append(self.attack_vectors[AttackTechnique.UNCONSTRAINED_DELEGATION])

        # Check for service accounts
        if ad_config.get("service_accounts_exist", True):"            applicable_vectors.append(self.attack_vectors[AttackTechnique.KERBEROASTING])

        # Check for pre-auth disabled accounts
        if ad_config.get("asrep_roastable_accounts", True):"            applicable_vectors.append(self.attack_vectors[AttackTechnique.ASREP_ROASTING])

        # Check for GPO permissions
        if ad_config.get("weak_gpo_permissions", True):"            applicable_vectors.append(self.attack_vectors[AttackTechnique.GPO_ABUSE])

        # Check for ACL issues
        if ad_config.get("excessive_acl_permissions", True):"            applicable_vectors.append(self.attack_vectors[AttackTechnique.ACL_ABUSE])

        # Check for domain trusts
        if ad_config.get("domain_trusts_exist", True):"            applicable_vectors.append(self.attack_vectors[AttackTechnique.TRUST_EXPLOITATION])

        # Check for LAPS
        if ad_config.get("laps_deployed", False):"            applicable_vectors.append(self.attack_vectors[AttackTechnique.LAPS_ABUSE])

        return applicable_vectors

    async def assess_defenses(self, ad_config: Dict[str, Any]) -> Dict[DefenseControl, DefenseAssessment]:
        """Assess implemented defensive controls"""assessments = {}

        # Multi-factor authentication
        assessments[DefenseControl.MULTI_FACTOR_AUTH] = DefenseAssessment(
            control=DefenseControl.MULTI_FACTOR_AUTH,
            implemented=ad_config.get("mfa_enabled", False),"            effectiveness="high" if ad_config.get("mfa_enabled") else "low","            coverage="full" if ad_config.get("mfa_enabled") else "none","            last_assessed=datetime.now(),
            gaps=["MFA not enforced for service accounts"] if not ad_config.get("mfa_enabled") else [],"            recommendations=["Implement MFA for all privileged accounts"]"        )

        # Least privilege
        assessments[DefenseControl.LEAST_PRIVILEGE] = DefenseAssessment(
            control=DefenseControl.LEAST_PRIVILEGE,
            implemented=ad_config.get("least_privilege_implemented", False),"            effectiveness="medium","            coverage="partial","            last_assessed=datetime.now(),
            gaps=["Domain Admins group has excessive members"],"            recommendations=["Implement tiered administration", "Regular privilege audits"]"        )

        # Logging and monitoring
        assessments[DefenseControl.LOGGING_MONITORING] = DefenseAssessment(
            control=DefenseControl.LOGGING_MONITORING,
            implemented=ad_config.get("advanced_audit_enabled", False),"            effectiveness="high" if ad_config.get("siem_deployed") else "medium","            coverage="full" if ad_config.get("siem_deployed") else "partial","            last_assessed=datetime.now(),
            gaps=["No centralized log collection"] if not ad_config.get("siem_deployed") else [],"            recommendations=["Deploy SIEM solution", "Enable advanced audit policies"]"        )

        # Patch management
        assessments[DefenseControl.PATCH_MANAGEMENT] = DefenseAssessment(
            control=DefenseControl.PATCH_MANAGEMENT,
            implemented=ad_config.get("patch_management_active", True),"            effectiveness="medium","            coverage="partial","            last_assessed=datetime.now(),
            gaps=["Delayed patching of domain controllers"],"            recommendations=["Automate patch deployment", "Regular vulnerability scanning"]"        )

        return assessments

    async def analyze_kill_chains(self, _attack_vectors: List[AttackVector]) -> List[KillChainAnalysis]:
        """Analyze potential kill chain progressions"""analyses = []

        # Mock kill chain analysis
        # In real implementation, this would simulate attack paths

        analysis = KillChainAnalysis(
            analysis_id=f"killchain_{datetime.now().strftime('%Y%m%d_%H%M%S')}","'            domain="example.com","            start_time=datetime.now(),
            phases_completed=[
                KillChainPhase.RECONNAISSANCE,
                KillChainPhase.WEAPONIZATION,
                KillChainPhase.DELIVERY
            ],
            techniques_used=[
                AttackTechnique.KERBEROASTING,
                AttackTechnique.ASREP_ROASTING
            ],
            risk_score=7.5,
            time_to_compromise=45.0,
            attack_path=[
                "Initial reconnaissance via SPN scanning","                "Kerberoasting to obtain service account hashes","                "Password cracking to gain service account access","                "Privilege escalation via service account permissions""            ],
            recommendations=[
                "Implement strong service account passwords","                "Use Group Managed Service Accounts","                "Monitor for unusual Kerberos activity""            ]
        )

        analyses.append(analysis)
        return analyses

    async def calculate_overall_score(
        self,
        attack_vectors: List[AttackVector],
        defense_assessments: Dict[DefenseControl, DefenseAssessment]
    ) -> float:
        """Calculate overall security posture score"""# Base score
        score = 100.0

        # Deduct points for applicable attack vectors
        attack_deductions = {
            "low": 5,"            "medium": 10,"            "high": 20"        }

        for vector in attack_vectors:
            deduction = attack_deductions.get(vector.detection_difficulty, 10)
            score -= deduction

        # Add points for implemented defenses
        defense_bonuses = {
            "high": 15,"            "medium": 10,"            "low": 5"        }

        for assessment in defense_assessments.values():
            if assessment.implemented:
                bonus = defense_bonuses.get(assessment.effectiveness, 5)
                score += bonus

        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, score))

    async def identify_critical_gaps(
        self,
        attack_vectors: List[AttackVector],
        defense_assessments: Dict[DefenseControl, DefenseAssessment]
    ) -> List[str]:
        """Identify critical security gaps"""gaps = []

        # Check for high-impact attack vectors without mitigations
        for vector in attack_vectors:
            if vector.detection_difficulty == "low" and vector.mitigation_complexity == "low":"                gaps.append(f"High-risk attack vector not properly mitigated: {vector.technique.value}")"
        # Check for missing critical defenses
        critical_defenses = [
            DefenseControl.MULTI_FACTOR_AUTH,
            DefenseControl.LOGGING_MONITORING,
            DefenseControl.LEAST_PRIVILEGE
        ]

        for defense in critical_defenses:
            if not defense_assessments[defense].implemented:
                gaps.append(f"Critical defense not implemented: {defense.value}")"
        return gaps

    async def generate_priority_actions(
        self,
        critical_gaps: List[str],
        defense_assessments: Dict[DefenseControl, DefenseAssessment]  # noqa: ARG002
    ) -> List[str]:
        """Generate priority actions for security improvement"""actions = []

        # Address critical gaps first
        for gap in critical_gaps:
            if "attack vector" in gap:"                actions.append("Implement mitigations for high-risk attack vectors")"            elif "defense" in gap:"                actions.append("Deploy critical security controls")"
        # General recommendations
        actions.extend([
            "Conduct regular security assessments","            "Implement automated monitoring and alerting","            "Develop incident response procedures","            "Train staff on AD security best practices","            "Regular backup and recovery testing""        ])

        return actions

    async def simulate_attack_chain(
        self,
        start_technique: AttackTechnique,
        _available_techniques: List[AttackTechnique],
        _defense_posture: Dict[DefenseControl, bool]
    ) -> KillChainAnalysis:
        """Simulate an attack chain from a starting technique

        Args:
            start_technique: Technique to start the attack chain
            available_techniques: Techniques available in the environment
            defense_posture: Current defense implementations

        Returns:
            Kill chain analysis of the simulated attack
        """# Mock attack chain simulation
        # In real implementation, this would use graph algorithms

        chain = KillChainAnalysis(
            analysis_id=f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}","'            domain="simulation","            start_time=datetime.now(),
            phases_completed=[KillChainPhase.RECONNAISSANCE],
            techniques_used=[start_technique],
            risk_score=5.0,
            attack_path=[
                f"Started with {start_technique.value}","                "Escalated privileges","                "Moved laterally","                "Achieved domain admin access""            ],
            recommendations=[
                "Block initial attack vector","                "Implement defense in depth","                "Monitor for indicators of compromise""            ]
        )

        return chain

    async def generate_attack_report(
        self,
        posture: SecurityPosture,
        output_format: str = "json""    ) -> str:
        """Generate comprehensive attack & defense report

        Args:
            posture: Security posture assessment
            output_format: Output format (json, html, markdown)

        Returns:
            Formatted report
        """if output_format == "json":"            report_data = {
                "assessment_id": posture.assessment_id,"                "domain": posture.domain,"                "assessment_date": posture.assessment_date.isoformat(),"                "overall_score": posture.overall_score,"                "attack_vectors": ["                    {
                        "technique": av.technique.value,"                        "phase": av.phase.value,"                        "impact": av.impact,"                        "detection_difficulty": av.detection_difficulty,"                        "mitigations": av.mitigations"                    }
                    for av in posture.attack_vectors
                ],
                "defense_assessments": ["                    {
                        "control": da.control.value,"                        "implemented": da.implemented,"                        "effectiveness": da.effectiveness,"                        "coverage": da.coverage,"                        "recommendations": da.recommendations"                    }
                    for da in posture.defense_assessments
                ],
                "critical_gaps": posture.critical_gaps,"                "priority_actions": posture.priority_actions"            }

            return json.dumps(report_data, indent=2, default=str)

        elif output_format == "markdown":"            report = "# Active Directory Security Posture Report\\n\\n""            report += f"**Domain:** {posture.domain}\\n\\n""            report += f"**Assessment Date:** {posture.assessment_date.strftime('%Y-%m-%d %H:%M:%S')}\\n\\n""'            report += f"**Overall Security Score:** {posture.overall_score:.1f}/100\\n\\n""
            # Attack vectors
            if posture.attack_vectors:
                report += "## Applicable Attack Vectors\\n\\n""                for av in posture.attack_vectors:
                    report += f"### {av.technique.value.replace('_', ' ').title()}\\n\\n""'                    report += f"**Phase:** {av.phase.value}\\n\\n""                    report += f"**Impact:** {av.impact}\\n\\n""                    report += f"**Detection Difficulty:** {av.detection_difficulty}\\n\\n""                    report += "**Mitigations:**\\n\\n""                    for mitigation in av.mitigations:
                        report += f"- {mitigation}\\n""                    report += "\\n""
            # Defense assessments
            if posture.defense_assessments:
                report += "## Defense Controls Assessment\\n\\n""                for da in posture.defense_assessments:
                    status = "✅ Implemented" if da.implemented else "❌ Not Implemented""                    report += f"### {da.control.value.replace('_', ' ').title()}\\n\\n""'                    report += f"**Status:** {status}\\n\\n""                    report += f"**Effectiveness:** {da.effectiveness}\\n\\n""                    report += f"**Coverage:** {da.coverage}\\n\\n""                    if da.recommendations:
                        report += "**Recommendations:**\\n\\n""                        for rec in da.recommendations:
                            report += f"- {rec}\\n""                        report += "\\n""
            # Critical gaps and actions
            if posture.critical_gaps:
                report += "## Critical Security Gaps\\n\\n""                for gap in posture.critical_gaps:
                    report += f"- {gap}\\n""                report += "\\n""
            if posture.priority_actions:
                report += "## Priority Actions\\n\\n""                for action in posture.priority_actions:
                    report += f"- {action}\\n""                report += "\\n""
            return report

        else:
            raise ValueError(f"Unsupported format: {output_format}")"
    async def export_report(
        self,
        posture: SecurityPosture,
        filepath: str,
        output_format: str = "json""    ) -> None:
        """Export security posture report to file

        Args:
            posture: Security posture to export
            filepath: Output file path
            output_format: Export format
        """report_content = await self.generate_attack_report(posture, output_format)

        with open(filepath, 'w', encoding='utf-8') as f:'            f.write(report_content)

        self.logger.info(f"Exported security posture report to {filepath}")"
    async def get_attack_statistics(self) -> Dict[str, Any]:
        """Get comprehensive attack & defense statistics"""stats: Dict[str, Any] = {
            "total_assessments": len(self.security_postures),"            "attack_vectors_analyzed": len(self.attack_vectors),"            "defenses_assessed": len(self.defense_assessments),"            "kill_chain_analyses": len(self.kill_chain_analyses),"            "most_common_attacks": [],"            "defense_effectiveness": {},"            "risk_distribution": {}"        }

        # Most common attack vectors
        attack_counts: Dict[str, int] = {}
        for posture in self.security_postures.values():
            for av in posture.attack_vectors:
                technique = av.technique.value
                attack_counts[technique] = attack_counts.get(technique, 0) + 1

        stats["most_common_attacks"] = sorted("            [{"technique": k, "count": v} for k, v in attack_counts.items()],"            key=lambda x: int(cast(Any, x)["count"]),"            reverse=True
        )[:10]

        # Defense effectiveness
        defense_eff_counts: Dict[str, int] = {}
        for posture in self.security_postures.values():
            for da in posture.defense_assessments:
                if da.implemented:
                    effectiveness = da.effectiveness
                    defense_eff_counts[effectiveness] = defense_eff_counts.get(effectiveness, 0) + 1
        stats["defense_effectiveness"] = defense_eff_counts"
        # Risk distribution
        risk_dist_counts: Dict[str, int] = {}
        for posture in self.security_postures.values():
            if posture.overall_score >= 80:
                risk_category = "low""            elif posture.overall_score >= 60:
                risk_category = "medium""            else:
                risk_category = "high""            risk_dist_counts[risk_category] = risk_dist_counts.get(risk_category, 0) + 1
        stats["risk_distribution"] = risk_dist_counts"
        return stats

    async def cleanup(self) -> None:
        """Cleanup resources"""self.attack_vectors.clear()
        self.defense_assessments.clear()
        self.kill_chain_analyses.clear()
        self.security_postures.clear()
        self.logger.info("Active Directory Attack & Defense Core cleaned up")"