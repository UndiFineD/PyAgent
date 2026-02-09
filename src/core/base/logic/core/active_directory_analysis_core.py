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
Active Directory Analysis Core

This core provides comprehensive analysis capabilities for Active Directory environments,
including enumeration, privilege escalation detection, and security assessment.

Based on patterns from Active-Directory-Exploitation-Cheat-Sheet repository.
"""

import logging
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from enum import Enum


class PrivilegeLevel(Enum):
    """Active Directory privilege levels"""
    DOMAIN_USER = "domain_user"
    LOCAL_ADMIN = "local_admin"
    DOMAIN_ADMIN = "domain_admin"
    ENTERPRISE_ADMIN = "enterprise_admin"
    SYSTEM = "system"


class ADObjectType(Enum):
    """Active Directory object types"""
    USER = "user"
    COMPUTER = "computer"
    GROUP = "group"
    OU = "organizational_unit"
    GPO = "group_policy"
    DOMAIN = "domain"


@dataclass
class ADObject:
    """Represents an Active Directory object"""
    distinguished_name: str
    object_type: ADObjectType
    name: str
    properties: Dict[str, Any]
    privileges: Set[PrivilegeLevel]
    relationships: Dict[str, List[str]]  # relationship_type -> [target_dns]


@dataclass
class ADEnumerationResult:
    """Results from AD enumeration"""
    domain_controllers: List[ADObject]
    users: List[ADObject]
    computers: List[ADObject]
    groups: List[ADObject]
    ous: List[ADObject]
    gpos: List[ADObject]
    trusts: List[Dict[str, Any]]
    shares: List[Dict[str, Any]]


@dataclass
class ADVulnerability:
    """Represents a detected AD vulnerability"""
    vulnerability_type: str
    severity: str
    description: str
    affected_objects: List[str]
    exploit_path: List[str]
    mitigation: str


class ActiveDirectoryAnalysisCore:
    """
    Core for analyzing Active Directory environments and detecting security vulnerabilities.

    This core implements patterns from the Active-Directory-Exploitation-Cheat-Sheet
    for comprehensive AD security assessment.
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.ad_objects: Dict[str, ADObject] = {}
        self.vulnerabilities: List[ADVulnerability] = []
        self.enumeration_cache: Optional[ADEnumerationResult] = None

    async def enumerate_domain(self, domain_name: Optional[str] = None) -> ADEnumerationResult:
        """
        Perform comprehensive domain enumeration using PowerView-style techniques.

        Args:
            domain_name: Optional domain to enumerate (defaults to current domain)

        Returns:
            ADEnumerationResult with all enumerated objects
        """
        self.logger.info(f"Starting domain enumeration for domain: {domain_name or 'current'}")

        # Simulate domain enumeration (in real implementation, this would use LDAP/low-level-protocols)
        result = ADEnumerationResult(
            domain_controllers=[],
            users=[],
            computers=[],
            groups=[],
            ous=[],
            gpos=[],
            trusts=[],
            shares=[]
        )

        # Domain controllers
        dc_dns = [
            "CN=DC01,OU=Domain Controllers,DC=example,DC=com",
            "CN=DC02,OU=Domain Controllers,DC=example,DC=com"
        ]

        for dc_dn in dc_dns:
            dc = ADObject(
                distinguished_name=dc_dn,
                object_type=ADObjectType.COMPUTER,
                name=dc_dn.split(',')[0].replace('CN=', ''),
                properties={"operating_system": "Windows Server 2022", "is_dc": True},
                privileges={PrivilegeLevel.DOMAIN_ADMIN, PrivilegeLevel.ENTERPRISE_ADMIN},
                relationships={}
            )
            result.domain_controllers.append(dc)
            self.ad_objects[dc_dn] = dc

        # Domain users
        user_dns = [
            "CN=Administrator,CN=Users,DC=example,DC=com",
            "CN=jsmith,CN=Users,DC=example,DC=com",
            "CN=bjones,CN=Users,DC=example,DC=com"
        ]

        for user_dn in user_dns:
            user_name = user_dn.split(',')[0].replace('CN=', '')
            user = ADObject(
                distinguished_name=user_dn,
                object_type=ADObjectType.USER,
                name=user_name,
                properties={"enabled": True, "last_logon": "2024-01-15"},
                privileges={PrivilegeLevel.DOMAIN_USER} if user_name != "Administrator"
                         else {PrivilegeLevel.DOMAIN_ADMIN, PrivilegeLevel.ENTERPRISE_ADMIN},
                relationships={}
            )
            result.users.append(user)
            self.ad_objects[user_dn] = user

        # Domain groups
        group_dns = [
            "CN=Domain Admins,CN=Users,DC=example,DC=com",
            "CN=Enterprise Admins,CN=Users,DC=example,DC=com",
            "CN=Domain Users,CN=Users,DC=example,DC=com"
        ]

        for group_dn in group_dns:
            group_name = group_dn.split(',')[0].replace('CN=', '')
            group = ADObject(
                distinguished_name=group_dn,
                object_type=ADObjectType.GROUP,
                name=group_name,
                properties={"member_count": 5},
                privileges={PrivilegeLevel.DOMAIN_ADMIN} if "Admins" in group_name
                         else {PrivilegeLevel.DOMAIN_USER},
                relationships={"members": [user_dn for user_dn in user_dns if "Administrator" in user_dn]}
            )
            result.groups.append(group)
            self.ad_objects[group_dn] = group

        self.enumeration_cache = result
        return result

    async def analyze_privilege_escalation_paths(self) -> List[List[str]]:
        """
        Analyze privilege escalation paths in the AD environment.

        Returns:
            List of privilege escalation paths (each path is a list of object DNs)
        """
        if not self.enumeration_cache:
            await self.enumerate_domain()

        escalation_paths = []

        # Find users with admin privileges
        admin_users = [
            obj for obj in self.ad_objects.values()
            if PrivilegeLevel.DOMAIN_ADMIN in obj.privileges or
               PrivilegeLevel.ENTERPRISE_ADMIN in obj.privileges
        ]

        # Find computers with local admin access
        admin_computers = [
            obj for obj in self.ad_objects.values()
            if obj.object_type == ADObjectType.COMPUTER and
               PrivilegeLevel.LOCAL_ADMIN in obj.privileges
        ]

        # Build escalation paths
        for user in admin_users:
            for computer in admin_computers:
                path = [user.distinguished_name, computer.distinguished_name]
                escalation_paths.append(path)

        return escalation_paths

    async def detect_vulnerabilities(self) -> List[ADVulnerability]:
        """
        Detect common AD vulnerabilities and misconfigurations.

        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []

        if not self.enumeration_cache:
            await self.enumerate_domain()

        # Check for unconstrained delegation
        unconstrained_delegation = ADVulnerability(
            vulnerability_type="unconstrained_delegation",
            severity="high",
            description="Computers with unconstrained delegation allow privilege escalation",
            affected_objects=["CN=DC01,OU=Domain Controllers,DC=example,DC=com"],
            exploit_path=["User with delegation rights", "Delegated authentication", "Domain admin access"],
            mitigation="Remove unconstrained delegation or limit to trusted computers"
        )
        vulnerabilities.append(unconstrained_delegation)

        # Check for weak passwords (simulated)
        weak_password_users = [
            obj for obj in self.ad_objects.values()
            if obj.object_type == ADObjectType.USER and
               not obj.properties.get("password_policy", {}).get("complexity", True)
        ]

        if weak_password_users:
            weak_password_vuln = ADVulnerability(
                vulnerability_type="weak_passwords",
                severity="medium",
                description="Users with weak password policies detected",
                affected_objects=[obj.distinguished_name for obj in weak_password_users],
                exploit_path=["Password spraying", "Brute force attacks"],
                mitigation="Enforce strong password policies and regular password changes"
            )
            vulnerabilities.append(weak_password_vuln)

        # Check for Kerberoastable accounts
        kerberoastable_accounts = [
            obj for obj in self.ad_objects.values()
            if obj.object_type == ADObjectType.USER and
               obj.properties.get("service_principal_name", False)
        ]

        if kerberoastable_accounts:
            kerberoast_vuln = ADVulnerability(
                vulnerability_type="kerberoastable_accounts",
                severity="medium",
                description="Service accounts vulnerable to Kerberoasting attacks",
                affected_objects=[obj.distinguished_name for obj in kerberoastable_accounts],
                exploit_path=["Request service tickets", "Extract hashes", "Offline cracking"],
                mitigation="Use managed service accounts or strong service account passwords"
            )
            vulnerabilities.append(kerberoast_vuln)

        self.vulnerabilities = vulnerabilities
        return vulnerabilities

    async def analyze_group_memberships(self) -> Dict[str, List[str]]:
        """
        Analyze group memberships and identify privilege relationships.

        Returns:
            Dictionary mapping group DNs to member DNs
        """
        if not self.enumeration_cache:
            await self.enumerate_domain()

        group_memberships = {}

        for group in self.enumeration_cache.groups:
            members = group.relationships.get("members", [])
            group_memberships[group.distinguished_name] = members

        return group_memberships

    async def check_acl_abuses(self) -> List[ADVulnerability]:
        """
        Check for dangerous ACL configurations that could lead to privilege escalation.

        Returns:
            List of ACL-related vulnerabilities
        """
        acl_vulnerabilities = []

        # Check for dangerous ACEs (simulated)
        dangerous_aces = [
            {
                "object": "CN=Domain Admins,CN=Users,DC=example,DC=com",
                "principal": "CN=jsmith,CN=Users,DC=example,DC=com",
                "rights": ["GenericAll"],
                "description": "Regular user has full control over Domain Admins group"
            }
        ]

        for ace in dangerous_aces:
            acl_vuln = ADVulnerability(
                vulnerability_type="dangerous_acl",
                severity="critical",
                description=f"Dangerous ACL: {ace['description']}",
                affected_objects=[ace["object"]],
                exploit_path=[
                    f"User {ace['principal']} exploits {ace['rights']} rights",
                    "Modifies group membership",
                    "Gains elevated privileges"
                ],
                mitigation="Review and restrict dangerous ACEs, implement least privilege"
            )
            acl_vulnerabilities.append(acl_vuln)

        return acl_vulnerabilities

    async def generate_security_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive security report for the AD environment.

        Returns:
            Dictionary containing the full security assessment
        """
        if not self.enumeration_cache:
            await self.enumerate_domain()

        escalation_paths = await self.analyze_privilege_escalation_paths()
        vulnerabilities = await self.detect_vulnerabilities()
        acl_issues = await self.check_acl_abuses()
        group_analysis = await self.analyze_group_memberships()

        report = {
            "enumeration_summary": {
                "total_users": len(self.enumeration_cache.users),
                "total_computers": len(self.enumeration_cache.computers),
                "total_groups": len(self.enumeration_cache.groups),
                "domain_controllers": len(self.enumeration_cache.domain_controllers)
            },
            "privilege_escalation_paths": len(escalation_paths),
            "vulnerabilities_found": len(vulnerabilities) + len(acl_issues),
            "critical_findings": [
                vuln for vuln in vulnerabilities + acl_issues
                if vuln.severity in ["critical", "high"]
            ],
            "group_membership_analysis": group_analysis,
            "recommendations": [
                "Implement least privilege access",
                "Regular password policy enforcement",
                "Monitor for suspicious group membership changes",
                "Review ACL configurations",
                "Enable advanced auditing"
            ]
        }
        return report

    async def analyze_dormant_accounts(self) -> List[ADVulnerability]:
        """
        Analyze dormant accounts that haven't logged in recently.

        Based on AD_Miner patterns for identifying stale accounts.
        """
        dormant_vulns = []

        if not self.enumeration_cache:
            await self.enumerate_domain()

        # Find accounts with old last logon dates (simulated)
        dormant_accounts = [
            obj for obj in self.ad_objects.values()
            if obj.object_type == ADObjectType.USER and
               obj.properties.get("last_logon", "").startswith("2023")  # Older than 1 year
        ]

        if dormant_accounts:
            dormant_vuln = ADVulnerability(
                vulnerability_type="dormant_accounts",
                severity="low",
                description="Dormant user accounts detected - potential security risk",
                affected_objects=[obj.distinguished_name for obj in dormant_accounts],
                exploit_path=["Account takeover", "Privilege escalation through stale credentials"],
                mitigation="Disable or remove dormant accounts, implement account lifecycle management"
            )
            dormant_vulns.append(dormant_vuln)

        return dormant_vulns

    async def analyze_kerberoastable_accounts(self) -> List[ADVulnerability]:
        """
        Identify accounts vulnerable to Kerberoasting attacks.

        Based on AD_Miner patterns for SPN analysis.
        """
        kerberoast_vulns = []

        if not self.enumeration_cache:
            await self.enumerate_domain()

        # Find accounts with Service Principal Names (vulnerable to Kerberoasting)
        kerberoastable = [
            obj for obj in self.ad_objects.values()
            if obj.object_type == ADObjectType.USER and
               obj.properties.get("service_principal_name", False)
        ]

        if kerberoastable:
            kerberoast_vuln = ADVulnerability(
                vulnerability_type="kerberoastable_accounts",
                severity="medium",
                description="Accounts with SPNs detected - vulnerable to Kerberoasting",
                affected_objects=[obj.distinguished_name for obj in kerberoastable],
                exploit_path=["Request service tickets", "Extract TGS hashes", "Offline cracking"],
                mitigation="Use managed service accounts or strong service account passwords"
            )
            kerberoast_vulns.append(kerberoast_vuln)

        return kerberoast_vulns

    async def analyze_privileged_accounts(self) -> Dict[str, List[str]]:
        """
        Analyze accounts with privileged access patterns.

        Based on AD_Miner privilege analysis.
        """
        privileged_analysis = {
            "domain_admins": [],
            "enterprise_admins": [],
            "tier_zero_sessions": [],
            "machine_accounts_with_admin": []
        }

        if not self.enumeration_cache:
            await self.enumerate_domain()

        for obj in self.ad_objects.values():
            if PrivilegeLevel.DOMAIN_ADMIN in obj.privileges:
                privileged_analysis["domain_admins"].append(obj.distinguished_name)
            if PrivilegeLevel.ENTERPRISE_ADMIN in obj.privileges:
                privileged_analysis["enterprise_admins"].append(obj.distinguished_name)

        # Identify machine accounts with admin privileges
        for obj in self.ad_objects.values():
            if (obj.object_type == ADObjectType.COMPUTER and
                PrivilegeLevel.DOMAIN_ADMIN in obj.privileges):
                privileged_analysis["machine_accounts_with_admin"].append(obj.distinguished_name)

        return privileged_analysis

    async def analyze_control_paths(self) -> List[Dict[str, Any]]:
        """
        Analyze control paths in the AD environment.

        Based on AD_Miner path analysis for privilege escalation routes.
        """
        control_paths = []

        if not self.enumeration_cache:
            await self.enumerate_domain()

        # Analyze paths from regular users to domain admins
        escalation_paths = await self.analyze_privilege_escalation_paths()

        for i, path in enumerate(escalation_paths):
            control_paths.append({
                "path_id": f"path_{i}",
                "source": path[0],
                "target": path[-1],
                "hops": len(path) - 1,
                "path": path,
                "risk_level": "high" if len(path) <= 3 else "medium"
            })

        return control_paths

    async def detect_apt_c2_patterns(self) -> List[ADVulnerability]:
        """
        Detect APT Command & Control patterns from APT-Attack-Simulation repository.

        Analyzes AD objects for signs of APT C2 activity including:
        - OneDrive API abuse (APT28 Fancy Bear)
        - VS Code tunnel exploitation (Mustang Panda)
        - DLL injection patterns
        - Unusual service accounts
        - Encrypted communication channels

        Returns:
            List of detected APT C2 vulnerabilities
        """
        vulnerabilities = []

        # Check for OneDrive API abuse patterns (APT28)
        onedrive_indicators = await self._detect_onedrive_c2_abuse()
        vulnerabilities.extend(onedrive_indicators)

        # Check for VS Code tunnel abuse (Mustang Panda)
        vscode_indicators = await self._detect_vscode_tunnel_abuse()
        vulnerabilities.extend(vscode_indicators)

        # Check for DLL injection patterns
        dll_injection_indicators = await self._detect_dll_injection_patterns()
        vulnerabilities.extend(dll_injection_indicators)

        # Check for trojanized application patterns (Labyrinth Chollima)
        trojanized_app_indicators = await self._detect_trojanized_applications()
        vulnerabilities.extend(trojanized_app_indicators)

        # Check for unusual service account activity
        service_account_indicators = await self._detect_unusual_service_accounts()
        vulnerabilities.extend(service_account_indicators)

        return vulnerabilities

    async def _detect_onedrive_c2_abuse(self) -> List[ADVulnerability]:
        """Detect OneDrive API abuse patterns used by APT28."""
        vulnerabilities = []

        # Look for accounts with unusual OneDrive API access patterns
        for dn, obj in self.ad_objects.items():
            if obj.object_type == ADObjectType.USER:
                # Check for suspicious properties indicating OneDrive C2
                suspicious_props = []

                # Check for unusual API permissions or tokens
                if "onedrive_api_access" in obj.properties:
                    suspicious_props.append("OneDrive API access detected")

                # Check for CRC32 checksum patterns in properties
                if any("crc32" in str(prop).lower() for prop in obj.properties.values()):
                    suspicious_props.append("CRC32 checksum patterns detected")

                # Check for base64 encoded content
                if any(self._is_base64_like(str(prop)) for prop in obj.properties.values()):
                    suspicious_props.append("Base64 encoded content detected")

                if suspicious_props:
                    vulnerabilities.append(ADVulnerability(
                        vulnerability_type="APT28_OneDrive_C2",
                        severity="high",
                        description=f"Potential APT28 Fancy Bear OneDrive C2 activity detected: {', '.join(suspicious_props)}",
                        affected_objects=[dn],
                        exploit_path=["User enumeration", "OneDrive API abuse", "Command execution"],
                        mitigation="Monitor OneDrive API access, implement strict API rate limiting, audit unusual authentication patterns"
                    ))

        return vulnerabilities

    async def _detect_vscode_tunnel_abuse(self) -> List[ADVulnerability]:
        """Detect VS Code tunnel abuse patterns used by Mustang Panda."""
        vulnerabilities = []

        # Look for accounts with VS Code tunnel access
        for dn, obj in self.ad_objects.items():
            if obj.object_type == ADObjectType.USER:
                suspicious_props = []

                # Check for VS Code tunnel indicators
                if "vscode_tunnel_access" in obj.properties:
                    suspicious_props.append("VS Code tunnel access detected")

                # Check for GitHub OAuth tokens
                if "github_oauth_token" in obj.properties:
                    suspicious_props.append("GitHub OAuth token detected")

                # Check for reverse shell indicators
                if any("tunnel" in str(prop).lower() for prop in obj.properties.values()):
                    suspicious_props.append("Tunnel-related activity detected")

                if suspicious_props:
                    vulnerabilities.append(ADVulnerability(
                        vulnerability_type="MustangPanda_VSCode_C2",
                        severity="high",
                        description=f"Potential Mustang Panda VS Code tunnel abuse detected: {', '.join(suspicious_props)}",
                        affected_objects=[dn],
                        exploit_path=["VS Code installation", "GitHub OAuth", "Tunnel establishment", "Reverse shell"],
                        mitigation="Monitor VS Code installations, restrict GitHub OAuth, audit tunnel connections"
                    ))

        return vulnerabilities

    async def _detect_dll_injection_patterns(self) -> List[ADVulnerability]:
        """Detect DLL injection patterns used by various APT groups."""
        vulnerabilities = []

        # Look for computers with suspicious DLL loading patterns
        for dn, obj in self.ad_objects.items():
            if obj.object_type == ADObjectType.COMPUTER:
                suspicious_props = []

                # Check for unusual DLL loading
                if "suspicious_dll_loads" in obj.properties:
                    suspicious_props.append("Suspicious DLL loading detected")

                # Check for VirtualAlloc patterns (memory allocation for shellcode)
                if "virtualalloc_usage" in obj.properties:
                    suspicious_props.append("VirtualAlloc memory allocation detected")

                # Check for process injection indicators
                if any("injection" in str(prop).lower() for prop in obj.properties.values()):
                    suspicious_props.append("Process injection indicators detected")

                if suspicious_props:
                    vulnerabilities.append(ADVulnerability(
                        vulnerability_type="APT_DLL_Injection",
                        severity="high",
                        description=f"DLL injection patterns detected: {', '.join(suspicious_props)}",
                        affected_objects=[dn],
                        exploit_path=["Malicious DLL deployment", "Process injection", "Memory execution"],
                        mitigation="Implement DLL allowlisting, monitor process injection, enable AMSI protection"
                    ))

        return vulnerabilities

    async def _detect_trojanized_applications(self) -> List[ADVulnerability]:
        """Detect trojanized application patterns used by Labyrinth Chollima."""
        vulnerabilities = []

        # Look for computers with trojanized applications
        for dn, obj in self.ad_objects.items():
            if obj.object_type == ADObjectType.COMPUTER:
                suspicious_props = []

                # Check for modified legitimate applications
                if "modified_sumatrapdf" in obj.properties:
                    suspicious_props.append("Modified SumatraPDF detected")

                # Check for trojanized PDF readers
                if "trojanized_pdf_reader" in obj.properties:
                    suspicious_props.append("Trojanized PDF reader detected")

                # Check for shellter injection patterns
                if "shellter_injection" in obj.properties:
                    suspicious_props.append("Shellter DLL injection detected")

                if suspicious_props:
                    vulnerabilities.append(ADVulnerability(
                        vulnerability_type="LabyrinthChollima_Trojanized_App",
                        severity="critical",
                        description=f"Trojanized application patterns detected: {', '.join(suspicious_props)}",
                        affected_objects=[dn],
                        exploit_path=["Legitimate application download", "DLL injection", "Trojanized execution"],
                        mitigation="Verify application integrity, use application allowlisting, monitor file modifications"
                    ))

        return vulnerabilities

    async def _detect_unusual_service_accounts(self) -> List[ADVulnerability]:
        """Detect unusual service account activity patterns."""
        vulnerabilities = []

        # Look for service accounts with suspicious activity
        for dn, obj in self.ad_objects.items():
            if obj.object_type == ADObjectType.USER:
                # Check if it's a service account
                if any("service" in str(prop).lower() for prop in obj.properties.values()):
                    suspicious_props = []

                    # Check for unusual login patterns
                    if "unusual_login_times" in obj.properties:
                        suspicious_props.append("Unusual login times detected")

                    # Check for lateral movement indicators
                    if "lateral_movement" in obj.properties:
                        suspicious_props.append("Lateral movement detected")

                    # Check for data exfiltration patterns
                    if "data_exfiltration" in obj.properties:
                        suspicious_props.append("Data exfiltration patterns detected")

                    if suspicious_props:
                        vulnerabilities.append(ADVulnerability(
                            vulnerability_type="APT_Service_Account_Abuse",
                            severity="medium",
                            description=f"Unusual service account activity: {', '.join(suspicious_props)}",
                            affected_objects=[dn],
                            exploit_path=["Service account compromise", "Privilege escalation", "Lateral movement"],
                            mitigation="Monitor service account usage, implement strict access controls, regular credential rotation"
                        ))

        return vulnerabilities

    def _is_base64_like(self, text: str) -> bool:
        """Check if text appears to be base64 encoded."""
        import base64
        import binascii

        # Remove whitespace and check length
        text = text.strip()
        if len(text) % 4 != 0:
            return False

        try:
            # Try to decode as base64
            decoded = base64.b64decode(text)
            # Check if decoded content looks like binary/executable
            return len(decoded) > 10 and any(c < 32 or c > 126 for c in decoded[:20])
        except (binascii.Error, ValueError):
            return False

    async def generate_ad_miner_style_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive AD security report in AD_Miner style.

        Includes risk ratings, key indicators, and mitigation recommendations.
        """
        if not self.enumeration_cache:
            await self.enumerate_domain()

        # Gather all analysis data
        dormant_accounts = await self.analyze_dormant_accounts()
        kerberoastable = await self.analyze_kerberoastable_accounts()
        privileged_analysis = await self.analyze_privileged_accounts()
        control_paths = await self.analyze_control_paths()
        vulnerabilities = await self.detect_vulnerabilities()
        acl_issues = await self.check_acl_abuses()
        apt_c2_vulnerabilities = await self.detect_apt_c2_patterns()

        # Calculate risk scores
        risk_score = 0
        risk_factors = []

        if len(dormant_accounts) > 0:
            risk_score += 2
            risk_factors.append("dormant_accounts")

        if len(kerberoastable) > 0:
            risk_score += 3
            risk_factors.append("kerberoastable_accounts")

        if len(privileged_analysis["machine_accounts_with_admin"]) > 0:
            risk_score += 4
            risk_factors.append("machine_accounts_with_admin")

        if len(control_paths) > 0:
            risk_score += 3
            risk_factors.append("short_control_paths")

        if len(apt_c2_vulnerabilities) > 0:
            risk_score += 5  # APT activity is highly concerning
            risk_factors.append("apt_c2_activity")

        # Determine overall risk level
        if risk_score >= 8:
            overall_risk = "critical"
        elif risk_score >= 5:
            overall_risk = "high"
        elif risk_score >= 3:
            overall_risk = "medium"
        else:
            overall_risk = "low"

        report = {
            "ad_miner_analysis": {
                "enumeration_summary": {
                    "total_users": len(self.enumeration_cache.users),
                    "total_computers": len(self.enumeration_cache.computers),
                    "total_groups": len(self.enumeration_cache.groups),
                    "domain_controllers": len(self.enumeration_cache.domain_controllers)
                },
                "privileged_accounts": privileged_analysis,
                "vulnerability_findings": {
                    "dormant_accounts": len(dormant_accounts),
                    "kerberoastable_accounts": len(kerberoastable),
                    "apt_c2_vulnerabilities": len(apt_c2_vulnerabilities),
                    "total_vulnerabilities": len(vulnerabilities) + len(acl_issues) + len(dormant_accounts) + len(kerberoastable) + len(apt_c2_vulnerabilities)
                },
                "control_paths": {
                    "total_paths": len(control_paths),
                    "high_risk_paths": len([p for p in control_paths if p["risk_level"] == "high"])
                },
                "risk_assessment": {
                    "overall_risk": overall_risk,
                    "risk_score": risk_score,
                    "risk_factors": risk_factors
                },
                "recommendations": [
                    "Review and disable dormant accounts",
                    "Implement managed service accounts for SPN-enabled accounts",
                    "Audit machine accounts with administrative privileges",
                    "Review control paths and implement least privilege",
                    "Enable advanced auditing and monitoring",
                    "Regular password policy enforcement",
                    "Implement account lifecycle management",
                    "Monitor for APT C2 indicators (OneDrive API abuse, VS Code tunnels)",
                    "Implement DLL allowlisting and injection prevention",
                    "Verify integrity of legitimate applications",
                    "Monitor service account usage patterns",
                    "Implement comprehensive endpoint detection and response (EDR)"
                ]
            }
        }

        return report