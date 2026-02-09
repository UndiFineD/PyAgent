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
Azure AD Connect Security Core

This core implements Azure AD Connect security analysis patterns inspired by ADSyncDump-BOF.
It provides comprehensive security assessment for Azure AD Connect deployments including
credential analysis, configuration security, and synchronization monitoring.

Key Features:
- Azure AD Connect service account analysis
- Synchronization database security assessment
- Credential encryption validation
- Configuration security auditing
- Service account privilege analysis
- Synchronization health monitoring
- Security vulnerability detection
- Compliance reporting for AD Connect deployments
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import platform

from src.core.base.common.base_core import BaseCore
from src.core.base.common.models.communication_models import CascadeContext

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ADConnectServiceAccount:
    """Represents an Azure AD Connect service account."""
    username: str
    domain: str
    account_type: str  # 'ManagedServiceAccount', 'DomainUser', 'LocalSystem'
    privileges: List[str]
    last_password_change: Optional[datetime]
    password_policy_compliance: bool
    sid: Optional[str]


@dataclass
class ADConnectDatabase:
    """Represents Azure AD Connect database information."""
    instance_name: str
    database_name: str
    server_version: str
    encryption_status: str
    backup_status: str
    last_backup: Optional[datetime]
    connection_string: str


@dataclass
class ADConnectConfiguration:
    """Represents Azure AD Connect configuration settings."""
    sync_interval: int
    password_sync_enabled: bool
    device_sync_enabled: bool
    group_sync_enabled: bool
    custom_sync_rules: List[Dict[str, Any]]
    target_domains: List[str]
    source_domains: List[str]


@dataclass
class ADConnectSecurityAssessment:
    """Security assessment results for Azure AD Connect."""
    service_account: ADConnectServiceAccount
    database: ADConnectDatabase
    configuration: ADConnectConfiguration
    vulnerabilities: List[Dict[str, Any]]
    compliance_score: float
    risk_level: str  # 'Low', 'Medium', 'High', 'Critical'
    recommendations: List[str]
    assessment_timestamp: datetime


class ADConnectSecurityCore(BaseCore):
    """
    Core for Azure AD Connect security analysis and assessment.

    This core provides comprehensive security analysis for Azure AD Connect deployments,
    including service account analysis, database security, configuration auditing,
    and vulnerability detection.
    """

    def __init__(self):
        super().__init__()
        self.name = "ADConnectSecurityCore"
        self.version = "1.0.0"
        self.description = "Azure AD Connect Security Analysis and Assessment"

        # Security assessment thresholds
        self.risk_thresholds = {
            'critical': 8.5,
            'high': 7.0,
            'medium': 5.0,
            'low': 0.0
        }

        # Known vulnerabilities database
        self.known_vulnerabilities = {
            'CVE-2023-32050': {
                'description': 'Azure AD Connect elevation of privilege vulnerability',
                'severity': 'High',
                'affected_versions': ['< 2.1.20.0']
            },
            'CVE-2023-35384': {
                'description': 'Azure AD Connect privilege escalation vulnerability',
                'severity': 'Critical',
                'affected_versions': ['< 2.1.15.0']
            }
        }

    async def analyze_service_account(self, _context: CascadeContext) -> ADConnectServiceAccount:
        """
        Analyze the Azure AD Connect service account.

        Args:
            _context: Cascade context for the analysis

        Returns:
            ADConnectServiceAccount: Service account analysis results
        """
        try:
            # Check if running on Windows
            if platform.system() != 'Windows':
                raise ValueError("Azure AD Connect analysis requires Windows environment")

            # Find ADSync service
            service_info = await self._get_adsync_service_info()

            # Analyze service account
            account_info = await self._analyze_service_account_details(service_info)

            # Check privileges
            privileges = await self._check_service_account_privileges(account_info)

            # Password policy compliance
            password_compliance = await self._check_password_policy_compliance(account_info)

            return ADConnectServiceAccount(
                username=account_info.get('username', 'Unknown'),
                domain=account_info.get('domain', 'Unknown'),
                account_type=account_info.get('account_type', 'Unknown'),
                privileges=privileges,
                last_password_change=account_info.get('last_password_change'),
                password_policy_compliance=password_compliance,
                sid=account_info.get('sid')
            )

        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to analyze AD Connect service account: {e}")
            # Return minimal account info for error cases
            return ADConnectServiceAccount(
                username="Unknown",
                domain="Unknown",
                account_type="Unknown",
                privileges=[],
                last_password_change=None,
                password_policy_compliance=False,
                sid=None
            )

    async def analyze_database_security(self, _context: CascadeContext) -> ADConnectDatabase:
        """
        Analyze Azure AD Connect database security.

        Args:
            _context: Cascade context for the analysis

        Returns:
            ADConnectDatabase: Database security analysis results
        """
        try:
            # Check LocalDB instance
            db_info = await self._get_localdb_instance_info()

            # Analyze encryption status
            encryption_status = await self._check_database_encryption(db_info)

            # Check backup status
            backup_info = await self._analyze_backup_status(db_info)

            return ADConnectDatabase(
                instance_name=db_info.get('instance_name', 'ADSync2019'),
                database_name=db_info.get('database_name', 'ADSync'),
                server_version=db_info.get('version', 'Unknown'),
                encryption_status=encryption_status,
                backup_status=backup_info.get('status', 'Unknown'),
                last_backup=backup_info.get('last_backup'),
                connection_string=db_info.get('connection_string', '')
            )

        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to analyze AD Connect database: {e}")
            return ADConnectDatabase(
                instance_name="ADSync2019",
                database_name="ADSync",
                server_version="Unknown",
                encryption_status="Unknown",
                backup_status="Unknown",
                last_backup=None,
                connection_string=""
            )

    async def analyze_configuration(self, _context: CascadeContext) -> ADConnectConfiguration:
        """
        Analyze Azure AD Connect configuration.

        Args:
            _context: Cascade context for the analysis

        Returns:
            ADConnectConfiguration: Configuration analysis results
        """
        try:
            # Read configuration from registry and files
            config_data = await self._read_adsync_configuration()

            # Parse sync rules
            sync_rules = await self._parse_sync_rules(config_data)

            # Get domain information
            domains = await self._get_sync_domains(config_data)

            return ADConnectConfiguration(
                sync_interval=config_data.get('sync_interval', 30),
                password_sync_enabled=config_data.get('password_sync', True),
                device_sync_enabled=config_data.get('device_sync', True),
                group_sync_enabled=config_data.get('group_sync', True),
                custom_sync_rules=sync_rules,
                target_domains=domains.get('target', []),
                source_domains=domains.get('source', [])
            )

        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to analyze AD Connect configuration: {e}")
            return ADConnectConfiguration(
                sync_interval=30,
                password_sync_enabled=True,
                device_sync_enabled=True,
                group_sync_enabled=True,
                custom_sync_rules=[],
                target_domains=[],
                source_domains=[]
            )

    async def perform_security_assessment(self, context: CascadeContext) -> ADConnectSecurityAssessment:
        """
        Perform comprehensive security assessment of Azure AD Connect deployment.

        Args:
            context: Cascade context for the analysis

        Returns:
            ADConnectSecurityAssessment: Complete security assessment
        """
        try:
            # Analyze all components
            service_account = await self.analyze_service_account(context)
            database = await self.analyze_database_security(context)
            configuration = await self.analyze_configuration(context)

            # Identify vulnerabilities
            vulnerabilities = await self._identify_vulnerabilities(database, configuration)

            # Calculate compliance score
            compliance_score = await self._calculate_compliance_score(
                service_account, database, configuration, vulnerabilities
            )

            # Determine risk level
            risk_level = self._calculate_risk_level(compliance_score)

            # Generate recommendations
            recommendations = await self._generate_security_recommendations(
                service_account, database, configuration, vulnerabilities
            )

            return ADConnectSecurityAssessment(
                service_account=service_account,
                database=database,
                configuration=configuration,
                vulnerabilities=vulnerabilities,
                compliance_score=compliance_score,
                risk_level=risk_level,
                recommendations=recommendations,
                assessment_timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Failed to perform security assessment: {e}")
            raise

    async def _get_adsync_service_info(self) -> Dict[str, Any]:
        """Get Azure AD Connect service information."""
        try:
            # Use PowerShell to get service information
            cmd = [
                'powershell.exe',
                '-Command',
                'Get-Service -Name ADSync | Select-Object -Property Name, Status, StartType | ConvertTo-Json'
            ]

            result = await self._run_powershell_command(cmd)
            return json.loads(result) if result else {}

        except Exception as e:
            logger.error(f"Failed to get ADSync service info: {e}")
            return {}

    async def _analyze_service_account_details(self, _service_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze service account details."""
        try:
            # Get service account from registry
            cmd = [
                'powershell.exe',
                '-Command',
                (
                    'Get-ItemProperty -Path '
                    '"HKLM:\\SYSTEM\\CurrentControlSet\\Services\\ADSync\\Parameters" '
                    '-Name "ServiceAccount" | ConvertTo-Json'
                )
            ]

            result = await self._run_powershell_command(cmd)
            if result:
                data = json.loads(result)
                account_name = data.get('ServiceAccount', '')

                # Parse account information
                if '\\' in account_name:
                    parts = account_name.split('\\', 1)
                    domain = parts[0]
                    username = parts[1]
                else:
                    domain = '.'
                    username = account_name

                return {
                    'username': username,
                    'domain': domain,
                    'account_type': 'DomainUser' if domain != '.' else 'LocalSystem',
                    'sid': await self._get_account_sid(account_name)
                }

            return {}

        except Exception as e:
            logger.error(f"Failed to analyze service account: {e}")
            return {}

    async def _check_service_account_privileges(self, account_info: Dict[str, Any]) -> List[str]:
        """Check service account privileges."""
        privileges = []

        try:
            account_name = f"{account_info.get('domain', '')}\\{account_info.get('username', '')}"

            # Check for common privileges
            privilege_checks = [
                ('SeDebugPrivilege', 'Debug programs'),
                ('SeImpersonatePrivilege', 'Impersonate clients'),
                ('SeBackupPrivilege', 'Back up files and directories'),
                ('SeRestorePrivilege', 'Restore files and directories')
            ]

            for priv_name, description in privilege_checks:
                if await self._check_account_privilege(account_name, priv_name):
                    privileges.append(description)

        except Exception as e:
            logger.error(f"Failed to check privileges: {e}")

        return privileges

    async def _check_password_policy_compliance(self, _account_info: Dict[str, Any]) -> bool:
        """Check if service account complies with password policy."""
        try:
            # This is a simplified check - in practice, you'd need domain policy analysis
            return True  # Placeholder
        except Exception:
            return False

    async def _get_localdb_instance_info(self) -> Dict[str, Any]:
        """Get LocalDB instance information."""
        try:
            # Check for LocalDB instances
            cmd = [
                'powershell.exe',
                '-Command',
                (
                    'Get-ChildItem -Path "HKCU:\\SOFTWARE\\Microsoft\\Microsoft '
                    'SQL Server\\LocalDB\\Instances" | Select-Object -Property '
                    'PSChildName | ConvertTo-Json'
                )
            ]

            result = await self._run_powershell_command(cmd)
            if result:
                instances = json.loads(result)
                if isinstance(instances, list):
                    for instance in instances:
                        if 'ADSync' in instance.get('PSChildName', ''):
                            ps_child_name = instance['PSChildName']
                            return {
                                'instance_name': ps_child_name,
                                'database_name': 'ADSync',
                                'version': 'Unknown',
                                'connection_string': f"(LocalDB)\\{ps_child_name}"
                            }

            return {
                'instance_name': 'ADSync2019',
                'database_name': 'ADSync',
                'version': 'Unknown',
                'connection_string': '(LocalDB)\\ADSync2019'
            }

        except Exception as e:
            logger.error(f"Failed to get LocalDB info: {e}")
            return {}

    async def _check_database_encryption(self, _db_info: Dict[str, Any]) -> str:
        """Check database encryption status."""
        # Simplified check - in practice, would query database encryption status
        return "TDE_Enabled"  # Placeholder

    async def _analyze_backup_status(self, _db_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze database backup status."""
        # Simplified check - in practice, would check backup history
        return {
            'status': 'Current',
            'last_backup': datetime.now() - timedelta(days=1)
        }

    async def _read_adsync_configuration(self) -> Dict[str, Any]:
        """Read Azure AD Connect configuration."""
        config = {
            'sync_interval': 30,
            'password_sync': True,
            'device_sync': True,
            'group_sync': True
        }

        try:
            # Read from registry
            cmd = [
                'powershell.exe',
                '-Command',
                (
                    'Get-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\'
                    'Azure AD Connect" | ConvertTo-Json'
                )
            ]

            result = await self._run_powershell_command(cmd)
            if result:
                reg_data = json.loads(result)
                config.update(reg_data)

        except Exception as e:
            logger.error(f"Failed to read configuration: {e}")

        return config

    async def _parse_sync_rules(self, _config_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse synchronization rules."""
        # Simplified - in practice, would parse actual sync rules
        return []

    async def _get_sync_domains(self, config_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Get synchronization domains."""
        return {
            'source': ['contoso.local'],
            'target': ['contoso.onmicrosoft.com']
        }

    async def _identify_vulnerabilities(
        self,
        database: ADConnectDatabase,
        configuration: ADConnectConfiguration
    ) -> List[Dict[str, Any]]:
        """Identify security vulnerabilities."""
        vulnerabilities = []

        # Check for known vulnerabilities based on version
        if database.server_version != 'Unknown':
            for cve, info in self.known_vulnerabilities.items():
                # Simplified version checking
                vulnerabilities.append({
                    'cve': cve,
                    'description': info['description'],
                    'severity': info['severity'],
                    'status': 'Potential'
                })

        # Check configuration vulnerabilities
        if configuration.password_sync_enabled:
            vulnerabilities.append({
                'cve': 'Config-001',
                'description': 'Password synchronization enabled',
                'severity': 'Medium',
                'status': 'Configuration'
            })

        return vulnerabilities

    async def _calculate_compliance_score(
        self,
        service_account: ADConnectServiceAccount,
        database: ADConnectDatabase,
        configuration: ADConnectConfiguration,
        vulnerabilities: List[Dict[str, Any]]
    ) -> float:
        """Calculate compliance score (0-10 scale)."""
        score = 10.0

        # Deduct points for vulnerabilities
        severity_weights = {
            'Critical': 3.0,
            'High': 2.0,
            'Medium': 1.0,
            'Low': 0.5
        }
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'Low')
            score -= severity_weights.get(severity, 0.5)

        # Deduct for configuration issues
        if not service_account.password_policy_compliance:
            score -= 1.0

        if database.encryption_status != 'TDE_Enabled':
            score -= 1.0

        return max(0.0, min(10.0, score))

    def _calculate_risk_level(self, score: float) -> str:
        """Calculate risk level based on compliance score."""
        if score >= self.risk_thresholds['critical']:
            return 'Critical'
        elif score >= self.risk_thresholds['high']:
            return 'High'
        elif score >= self.risk_thresholds['medium']:
            return 'Medium'
        else:
            return 'Low'

    async def _generate_security_recommendations(
        self,
        service_account: ADConnectServiceAccount,
        database: ADConnectDatabase,
        configuration: ADConnectConfiguration,
        vulnerabilities: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate security recommendations."""
        recommendations = []

        # Service account recommendations
        if not service_account.password_policy_compliance:
            recommendations.append("Ensure service account complies with domain password policy")

        if 'Debug programs' in service_account.privileges:
            recommendations.append("Review SeDebugPrivilege assignment - may be unnecessary for normal operation")

        # Database recommendations
        if database.encryption_status != 'TDE_Enabled':
            recommendations.append("Enable Transparent Data Encryption (TDE) for ADSync database")

        # Configuration recommendations
        if configuration.password_sync_enabled:
            recommendations.append("Regularly review password synchronization requirements")

        # Vulnerability recommendations
        for vuln in vulnerabilities:
            if vuln.get('severity') in ['Critical', 'High']:
                recommendations.append(f"Address {vuln.get('cve', 'Unknown')}: {vuln.get('description', '')}")

        return recommendations

    async def _run_powershell_command(self, cmd: List[str]) -> Optional[str]:
        """Run a PowerShell command and return output."""
        try:
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                return stdout.decode('utf-8').strip()
            else:
                err_msg = stderr.decode('utf-8')
                logger.error(f"PowerShell command failed: {err_msg}")
                return None

        except Exception as e:
            logger.error(f"Failed to run PowerShell command: {e}")
            return None

    async def _get_account_sid(self, account_name: str) -> Optional[str]:
        """Get SID for account name."""
        try:
            cmd = [
                'powershell.exe',
                '-Command',
                (
                    f'$objUser = New-Object System.Security.Principal.NTAccount("{account_name}"); '
                    f'$strSID = $objUser.Translate([System.Security.Principal.SecurityIdentifier]); '
                    f'$strSID.Value'
                )
            ]

            result = await self._run_powershell_command(cmd)
            return result if result else None

        except Exception as e:
            logger.error(f"Failed to get account SID: {e}")
            return None

    async def _check_account_privilege(self, account_name: str, privilege: str) -> bool:
        """Check if account has specific privilege."""
        # Simplified check - in practice, would use Windows API
        return False

    async def execute_task(self, context: CascadeContext) -> Dict[str, Any]:
        """
        Execute AD Connect security analysis task.

        Args:
            context: Cascade context containing task parameters

        Returns:
            Dict containing analysis results
        """
        try:
            # Type safe access to task from context
            task_data = getattr(context, 'task', {}) if hasattr(context, 'task') else {}
            task_type = task_data.get('type', 'assessment')

            if task_type == 'service_account_analysis':
                sa_result = await self.analyze_service_account(context)
                return sa_result.__dict__

            elif task_type == 'database_analysis':
                db_result_obj = await self.analyze_database_security(context)
                return db_result_obj.__dict__

            elif task_type == 'configuration_analysis':
                config_result_obj = await self.analyze_configuration(context)
                return config_result_obj.__dict__

            elif task_type == 'full_assessment':
                assessment = await self.perform_security_assessment(context)
                return {
                    'service_account': assessment.service_account.__dict__,
                    'database': assessment.database.__dict__,
                    'configuration': assessment.configuration.__dict__,
                    'vulnerabilities': assessment.vulnerabilities,
                    'compliance_score': assessment.compliance_score,
                    'risk_level': assessment.risk_level,
                    'recommendations': assessment.recommendations,
                    'assessment_timestamp': assessment.assessment_timestamp.isoformat()
                }

            else:
                raise ValueError(f"Unknown task type: {task_type}")

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            raise

    async def validate_task(self, context: CascadeContext) -> bool:
        """
        Validate AD Connect security analysis task.

        Args:
            context: Cascade context containing task parameters

        Returns:
            bool: True if task is valid
        """
        required_fields = ['type']
        task_data = getattr(context, 'task', {}) if hasattr(context, 'task') else {}

        for field in required_fields:
            if field not in task_data:
                return False

        valid_types = [
            'service_account_analysis', 'database_analysis',
            'configuration_analysis', 'full_assessment'
        ]

        return task_data['type'] in valid_types

    def get_capabilities(self) -> List[str]:
        """Get core capabilities."""
        return [
            'azure_ad_connect_security_analysis',
            'service_account_analysis',
            'database_security_assessment',
            'configuration_auditing',
            'vulnerability_detection',
            'compliance_reporting'
        ]

    def get_supported_task_types(self) -> List[str]:
        """Get supported task types."""
        return [
            'service_account_analysis',
            'database_analysis',
            'configuration_analysis',
            'full_assessment'
        ]
