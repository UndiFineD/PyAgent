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

from typing import List, Dict, Any


class ADIntelligence:
    """Intelligence engine for Active Directory enumeration and exploitation."""

    @staticmethod
    def get_certificate_abuse_scenarios() -> Dict[str, Any]:
        """Scenarios for Active Directory Certificate Services (ADCS) abuse (ESC1-ESC13)."""
        return {
            "ESC1": {
                "name": "Enrollee Supplies Subject Alternative Name",
                "description": "Template allows enrollees to request a certificate for any user (SAN abuse).",
                "conditions": "msPKI-Certificate-Name-Flag: CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT",
            },
            "ESC2": {
                "name": "Any Purpose EKU",
                "description": "Template defines 'Any Purpose' EKU or no EKU, allowing it to be used for any purpose.",
                "conditions": "pKIExtendedKeyUsage: 2.5.29.37.0",
            },
            "ESC3": {
                "name": "Certificate Request Agent EKU",
                "description": "Enrollment agent certificate can be used to request certificates on behalf of others.",
                "conditions": "pKIExtendedKeyUsage: 1.3.6.1.4.1.311.20.2.1",
            },
            "ESC4": {
                "name": "Vulnerable Template ACL",
                "description": "Template permits write access to an attacker-controlled principal.",
                "conditions": "ACL: Write/FullControl",
            },
        }

    @staticmethod
    def get_replication_rights_guids() -> Dict[str, str]:
        """GUIDs for Active Directory Replication Rights (DCSync)."""
        return {
            "DS-Replication-Get-Changes": "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2",
            "DS-Replication-Get-Changes-All": "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2",
            "DS-Replication-Get-Changes-In-Filtered-Set": "89e95b76-444d-4c62-991a-7fac0dd57a0c",
        }

    @staticmethod
    def get_weak_permission_abuse_types() -> Dict[str, str]:
        """A registry of weak AD permissions and their abuse vectors."""
        return {
            "GenericAll": "Full control over the object. Can change password, add to group, etc.",
            "GenericWrite": "Can update any non-protected attribute (e.g., servicePrincipalName, scriptPath).",
            "WriteDacl": "Can modify the security descriptor, effectively granting themselves GenericAll.",
            "WriteOwner": "Can take ownership of the object, then modify the DACL.",
            "AllExtendedRights": "Permission to perform any extended right (e.g., ForceChangePassword).",
            "AddMember": "Permission to add objects to a group.",
        }

    @staticmethod
    def generate_certex_command(action: str, target: str, template: str, cert_path: str = "") -> str:
        """Generates Certipy-style commands for ADCS abuse."""
        if action == "find":
            return f"certipy find -u {target} -p 'password' -dc-ip {target} -vulnerable"
        elif action == "req":
            return f"certipy req -u {target} -p 'password' -ca {target}-CA -template {template} -upn administrator"
        elif action == "auth":
            return f"certipy auth -pfx {cert_path} -dc-ip {target}"
        return ""

    @staticmethod
    def get_sensitive_spns() -> List[str]:
        """Common sensitive SPNs for Kerberoasting discovery."""
        return ["MSSQLSvc/*", "TERMSRV/*", "HTTP/*", "STS/*", "Exchange/*", "LDAP/*"]

    @staticmethod
    def get_laps_attributes() -> List[str]:
        """Returns attributes used by legacy and modern LAPS."""
        return [
            "ms-Mcs-AdmPwd",  # Legacy LAPS
            "ms-Mcs-AdmPwdExpirationTime",
            "msLAPS-Password",  # Modern Windows LAPS
            "msLAPS-PasswordExpirationTime",
        ]

    @staticmethod
    def get_sccm_vulnerability_indicators() -> Dict[str, Any]:
        """Indicators for SCCM (MECM) misconfigurations (Ported from GOAD/SharpSCCM)."""
        return {
            "NAA_Credentials": {
                "description": "Network Access Account credentials stored in WMI.",
                "query": (
                    "Get-WmiObject -Namespace root\\ccm\\policy\\machine\\actualconfig -Class CCM_NetworkAccessAccount"
                ),
            },
            "PXE_Password": {
                "description": "PXE boot passwords often found in SCCM configuration files or registry.",
                "location": "HKLM\\Software\\Microsoft\\SMS\\Providers\\CommaSeparatedPXEPassword",
            },
            "Client_Push_Account": {
                "description": "Accounts used for client push installation often have local admin rights.",
                "remediation": "Check for privileged accounts used in 'Client Push Installation Properties'.",
            },
        }

    @staticmethod
    def get_gpo_abuse_indicators() -> List[Dict[str, str]]:
        """Common GPO misconfigurations for persistence and privilege escalation."""
        return [
            {
                "name": "Scheduled Task GPO",
                "file": "ScheduledTasks.xml",
                "description": "Stored credentials in GPO scheduled tasks (cpassword).",
            },
            {
                "name": "Restricted Groups GPO",
                "file": "GptTmpl.inf",
                "description": "GPO enforcing local group membership (e.g. adding domain users to local admins).",
            },
            {
                "name": "Registry GPO",
                "file": "Registry.xml",
                "description": "GPO pushing insecure registry settings (e.g. disabling UAC or Defender).",
            },
        ]

    @staticmethod
    def get_bitlocker_recovery_attributes() -> List[str]:
        """Attributes for extracting BitLocker recovery keys (msFVE-RecoveryInformation)."""
        return [
            "msFVE-RecoveryPassword",  # Cleartext recovery key
            "msFVE-RecoveryGuid",
            "msFVE-VolumeGuid",
            "msFVE-KeyPackage",
        ]

    @staticmethod
    def get_bitlocker_ldap_query() -> str:
        """LDAP filter for discovering BitLocker recovery objects."""
        return "(objectClass=msFVE-RecoveryInformation)"

    @staticmethod
    def get_pathfinding_queries() -> Dict[str, str]:
        """Cypher queries for structured AD pathfinding analysis."""
        return {
            "shortest_path_to_domain_admin": (
                "MATCH (n:User), (m:Group {name: 'DOMAIN ADMINS'}), p=shortestPath((n)-[*..15]->(m)) RETURN p"
            ),
            "shortest_path_to_da_by_id": (
                "MATCH (n:User), (m:Group), p=shortestPath((n)-[*..15]->(m)) WHERE m.objectid ENDS WITH '-512' RETURN p"
            ),
            "high_value_targets_chokepoints": "MATCH (n:Group) WHERE n.highvalue = true RETURN n.name, n.objectid",
            "unconstrained_delegation": "MATCH (c:Computer {unconstraineddelegation: true}) RETURN c.name",
            "kerberoastable_users": "MATCH (u:User {hasspn: true}) RETURN u.name, u.serviceprincipalnames",
            "asreproastable_users": "MATCH (u:User {dontreqpreauth: true}) RETURN u.name",
            "pw_in_description": "MATCH (n) WHERE n.description =~ '.*((?i)pass|pw|:).*' RETURN n.name, n.description",
        }

    @staticmethod
    def get_drs_replication_primitives() -> Dict[str, Any]:
        """OIDs and codes for DRS (Directory Replication Service) protocol hunting."""
        return {
            "DRS_GET_NC_CHANGES": 0x3,
            "DRS_REPL_OBJ": 0x1,
            "hidden_objects_via_drs": "Using DRSGetNCChanges to retrieve objects bypassed by standard LDAP filters",
            "sid_history_hunting": "Identifying persistence via orphaned or high-privileged SIDHistory values",
            "gpo_link_regex": r"://(.*?;\d)",  # Used to extract GPOs from gPLink attribute
        }

    @staticmethod
    def get_account_property_sets() -> Dict[str, List[str]]:
        """Property sets for AD object enumeration (Ported from FarsightAD)."""
        minimal = ["Name", "ObjectGUID", "DistinguishedName", "ObjectClass"]
        account_min = minimal + ["Enabled", "SamAccountName", "objectSid", "Description", "whenCreated", "pwdLastSet"]
        return {
            "minimal": minimal,
            "account_extended": account_min + ["userAccountControl", "UserPrincipalName", "ServicePrincipalName"],
            "all": account_min
            + ["userCertificate", "mS-DS-CreatorSID", "primaryGroupID", "SIDHistory", "msDS-AllowedToDelegateTo"],
        }

    @staticmethod
    def get_adws_enumeration_info() -> Dict[str, Any]:
        """Returns info on Active Directory Web Services (Port 9389)."""
        return {
            "port": 9389,
            "service": "ADWS",
            "description": "Used by AD PowerShell module. Often easier to query than LDAP.",
        }

    @staticmethod
    def get_ad_privilege_enumeration_queries() -> Dict[str, str]:
        """A collection of high-value LDAP filters for Active Directory discovery."""
        return {
            "all_users": "(objectCategory=user)",
            "all_groups": "(objectCategory=group)",
            "all_computers": "(objectClass=Computer)",
            "privileged_accounts": "(&(objectCategory=person)(objectClass=user)(adminCount=1))",
            "kerberoastable_users": (
                "(&(&(servicePrincipalName=*)(UserAccountControl:1.2.840.113556.1.4.803:=512))"
                "(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))"
            ),
            "unconstrained_delegation_users": (
                "(&(&(objectCategory=person)(objectClass=user))(userAccountControl:1.2.840.113556.1.4.803:=524288))"
            ),
            "unconstrained_delegation_computers": (
                "(&(objectCategory=computer)(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))"
            ),
            "constrained_delegation": "(&(objectCategory=computer)(msDS-AllowedToDelegateTo=*))",
            "gpos": "(objectClass=groupPolicyContainer)",
            "laps_passwords": "(ms-Mcs-AdmPwd=*)",
            "asreproastable_users": "(userAccountControl:1.2.840.113556.1.4.803:=4194304)",
            "shadow_credentials": "(&(objectClass=user)(msDS-KeyCredentialLink=*))",
            "dns_admins": "(memberOf=CN=DnsAdmins,CN=Users,DC=...)",
        }

    @staticmethod
    def get_critical_event_ids() -> Dict[str, str]:
        """Mappings of MITRE ATT&CK techniques to Windows Event IDs for AD threat hunting."""
        return {
            "4769": "T1558.003 - Kerberoasting (Service Ticket Requested)",
            "4768": "T1558.004 - ASREPRoasting (TGT Requested)",
            "4776": "T1110 - Brute Force (Credential Validation)",
            "4662": "T1003.006 - DCSync (Replication Operation)",
            "5136": "T1134.005 - SID History Injection (Object Modified)",
            "1102": "T1070.001 - Clearing Event Logs",
            "4720": "T1136.002 - Domain Account Creation",
            "4740": "T1110 - Brute Force (Account Lockout)",
        }

    @staticmethod
    def get_privileged_group_names() -> List[str]:
        """A list of common privileged group names in AD for targeting."""
        return [
            "Domain Admins",
            "Enterprise Admins",
            "Schema Admins",
            "Administrators",
            "Account Operators",
            "Backup Operators",
            "Server Operators",
            "Print Operators",
            "DnsAdmins",
            "Group Policy Creator Owners",
        ]
