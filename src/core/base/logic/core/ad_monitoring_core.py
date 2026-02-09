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
Active Directory Monitoring Core

This core implements real-time Active Directory change monitoring patterns inspired by ADSpider.
It provides comprehensive AD security monitoring using Update Sequence Numbers (USN) and replication metadata.

Key Features:
- Real-time AD change monitoring without full object enumeration
- USN-based change detection and filtering
- Human-readable change explanations
- Security-focused attribute monitoring
- Configurable filtering and alerting
- Historical change tracking
- Integration with security incident response workflows
"""

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Protocol, Set, Tuple, cast
from enum import Enum
import time
import threading

from src.core.base.common.base_core import BaseCore
from src.core.base.common.models.communication_models import CascadeContext

# Configure logging
logger = logging.getLogger(__name__)


class ChangeType(Enum):
    """Types of AD object changes"""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"


class AttributeChangeType(Enum):
    """Types of attribute changes"""
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"


class SecurityEventType(Enum):
    """Security-relevant event types"""
    USER_ACCOUNT_CONTROL_CHANGE = "user_account_control_change"
    PASSWORD_CHANGE = "password_change"
    GROUP_MEMBERSHIP_CHANGE = "group_membership_change"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    ACCOUNT_LOCKOUT = "account_lockout"
    SUSPICIOUS_LOGIN = "suspicious_login"
    ADMIN_ACCESS_CHANGE = "admin_access_change"


@dataclass
class ADObjectChange:
    """Represents a change to an Active Directory object"""
    object_dn: str
    object_guid: str
    object_class: str
    change_type: ChangeType
    timestamp: datetime
    usn: int
    version: int
    attributes: Dict[str, Any] = field(default_factory=dict)
    previous_values: Dict[str, Any] = field(default_factory=dict)
    security_events: List[SecurityEventType] = field(default_factory=list)
    explanation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttributeChange:
    """Represents a change to a specific attribute"""
    attribute_name: str
    new_value: Any
    old_value: Any = None
    change_type: AttributeChangeType = AttributeChangeType.MODIFIED
    timestamp: datetime = field(default_factory=datetime.now)
    usn: int = 0
    version: int = 1
    explanation: str = ""


@dataclass
class MonitoringSession:
    """Active Directory monitoring session"""
    session_id: str
    domain_controller: str
    start_usn: int
    current_usn: int
    is_active: bool = True
    last_check: datetime = field(default_factory=datetime.now)
    excluded_objects: Set[str] = field(default_factory=set)
    monitored_attributes: Set[str] = field(default_factory=set)
    security_filters: Dict[str, Any] = field(default_factory=dict)
    change_history: List[ADObjectChange] = field(default_factory=list)


@dataclass
class MonitoringConfig:
    """Configuration for AD monitoring"""
    domain_controllers: List[str]
    check_interval: int = 30  # seconds
    max_history_size: int = 10000
    excluded_attributes: Set[str] = field(default_factory=lambda: {"lastLogonTimestamp"})
    security_attributes: Set[str] = field(default_factory=lambda: {
        "userAccountControl", "member", "pwdLastSet", "lockoutTime",
        "accountExpires", "adminCount", "servicePrincipalName"
    })
    alert_thresholds: Dict[str, int] = field(default_factory=dict)
    retention_days: int = 30


class ADConnectionProvider(Protocol):
    """Protocol for Active Directory connection providers"""

    async def connect(self, domain_controller: str, credentials: Optional[Dict[str, Any]] = None) -> Any:
        """Establish connection to domain controller"""
        ...

    async def get_current_usn(self, connection: Any) -> int:
        """Get current Update Sequence Number"""
        ...

    async def get_changed_objects(
        self,
        connection: Any,
        start_usn: int,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get objects changed since specified USN"""
        ...

    async def get_object_attributes(self, connection: Any, object_guid: str) -> Dict[str, Any]:
        """Get replication metadata for object attributes"""
        ...

    async def disconnect(self, connection: Any) -> None:
        """Close connection to domain controller"""
        ...


class AlertProvider(Protocol):
    """Protocol for alert/notification providers"""

    async def send_alert(self, change: ADObjectChange, severity: str, context: Dict[str, Any]) -> None:
        """Send alert for detected change"""
        ...

    async def send_security_alert(self, events: List[SecurityEventType], change: ADObjectChange) -> None:
        """Send security-specific alert"""
        ...


class ADMonitoringCore(BaseCore):
    """
    Active Directory Monitoring Core

    Provides real-time monitoring of Active Directory changes using USN-based detection,
    inspired by ADSpider's approach to efficient AD monitoring.

    Key Capabilities:
    - USN-based change detection without full enumeration
    - Security-focused attribute monitoring
    - Human-readable change explanations
    - Configurable alerting and filtering
    - Historical change tracking and analysis
    - Integration with security incident response
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config or {})

        # Core components
        self.ad_provider: Optional[ADConnectionProvider] = None
        self.alert_provider: Optional[AlertProvider] = None

        # Monitoring state
        self.monitoring_sessions: Dict[str, MonitoringSession] = {}
        self.monitoring_config: MonitoringConfig = MonitoringConfig([])
        self.change_history: List[ADObjectChange] = []
        self.security_events: List[Tuple[SecurityEventType, ADObjectChange]] = []

        # Control flags
        self.is_monitoring: bool = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.stop_event: threading.Event = threading.Event()

        # Initialize core
        self._initialize_core()

    def _initialize_core(self) -> None:
        """Initialize the AD monitoring core"""
        logger.info("Initializing Active Directory Monitoring Core")

        # Load configuration
        self._load_monitoring_config()

        # Initialize security monitoring rules
        self._initialize_security_rules()

    def _load_monitoring_config(self) -> None:
        """Load monitoring configuration"""
        config = self.config.get("ad_monitoring", {})

        self.monitoring_config = MonitoringConfig(
            domain_controllers=config.get("domain_controllers", []),
            check_interval=config.get("check_interval", 30),
            max_history_size=config.get("max_history_size", 10000),
            excluded_attributes=set(config.get("excluded_attributes", ["lastLogonTimestamp"])),
            security_attributes=set(config.get("security_attributes", [
                "userAccountControl", "member", "pwdLastSet", "lockoutTime",
                "accountExpires", "adminCount", "servicePrincipalName"
            ])),
            alert_thresholds=config.get("alert_thresholds", {}),
            retention_days=config.get("retention_days", 30)
        )

    def _initialize_security_rules(self) -> None:
        """Initialize security monitoring rules"""
        # These would be loaded from configuration or database
        self.security_rules = {
            "user_account_control": self._check_user_account_control,
            "group_membership": self._check_group_membership,
            "password_changes": self._check_password_changes,
            "privilege_escalation": self._check_privilege_escalation,
            "admin_access": self._check_admin_access
        }

    async def start_monitoring(
        self,
        domain_controllers: Optional[List[str]] = None,
        context: Optional[CascadeContext] = None
    ) -> str:
        """Start AD monitoring session"""
        if not self.ad_provider:
            raise ValueError("No AD connection provider configured")

        session_id = str(uuid.uuid4())
        dc_list = domain_controllers or self.monitoring_config.domain_controllers

        if not dc_list:
            raise ValueError("No domain controllers specified")

        # Create monitoring sessions for each DC
        for dc in dc_list:
            session = MonitoringSession(
                session_id=f"{session_id}_{dc}",
                domain_controller=dc,
                start_usn=0,
                current_usn=0,
                monitored_attributes=self.monitoring_config.security_attributes.copy()
            )
            self.monitoring_sessions[session.session_id] = session

            # Initialize USN for each session
            await self._initialize_session_usn(session)

        # Start monitoring thread
        self.is_monitoring = True
        self.stop_event.clear()
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

        logger.info(f"Started AD monitoring session {session_id} for {len(dc_list)} domain controllers")
        return session_id

    async def stop_monitoring(
        self,
        session_id: Optional[str] = None,
        context: Optional[CascadeContext] = None
    ) -> None:
        """Stop AD monitoring"""
        self.is_monitoring = False
        self.stop_event.set()

        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)

        if session_id:
            # Remove specific session
            sessions_to_remove = [
                s for s in self.monitoring_sessions.keys()
                if s.startswith(session_id)
            ]
            for session_key in sessions_to_remove:
                del self.monitoring_sessions[session_key]
        else:
            # Stop all sessions
            self.monitoring_sessions.clear()

        logger.info(f"Stopped AD monitoring session {session_id or 'all'}")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while not self.stop_event.is_set() and self.is_monitoring:
            try:
                # Run monitoring check
                asyncio.run(self._check_for_changes())

                # Wait for next check interval
                self.stop_event.wait(self.monitoring_config.check_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Brief pause before retry

    async def _check_for_changes(self) -> None:
        """Check for AD changes across all monitoring sessions"""
        for session in self.monitoring_sessions.values():
            if not session.is_active:
                continue

            try:
                await self._check_session_changes(session)
            except Exception as e:
                logger.error(f"Error checking changes for session {session.session_id}: {e}")

    async def _check_session_changes(self, session: MonitoringSession) -> None:
        """Check for changes in a specific monitoring session"""
        if not self.ad_provider:
            return

        # Connect to domain controller
        connection = await self.ad_provider.connect(session.domain_controller)

        try:
            # Get current USN
            current_usn = await self.ad_provider.get_current_usn(connection)

            if current_usn > session.current_usn:
                # Get changed objects
                changed_objects = await self.ad_provider.get_changed_objects(
                    connection, session.current_usn
                )

                # Process changes
                for obj_data in changed_objects:
                    if obj_data.get("objectGUID") in session.excluded_objects:
                        continue

                    change = await self._process_object_change(obj_data, session)
                    if change:
                        await self._handle_change_detection(change, session)

                # Update session USN
                session.current_usn = current_usn
                session.last_check = datetime.now()

        finally:
            await self.ad_provider.disconnect(connection)

    async def _process_object_change(
        self,
        obj_data: Dict[str, Any],
        session: MonitoringSession
    ) -> Optional[ADObjectChange]:
        """Process a detected object change"""
        object_guid = obj_data.get("objectGUID")
        if not object_guid:
            return None

        # Get replication metadata
        if not self.ad_provider:
            return None

        connection = await self.ad_provider.connect(session.domain_controller)
        try:
            attributes = await self.ad_provider.get_object_attributes(connection, object_guid)
        finally:
            await self.ad_provider.disconnect(connection)

        # Filter for monitored attributes
        relevant_changes: Dict[str, AttributeChange] = {}
        security_events = []

        for attr_name, attr_data in attributes.items():
            if attr_name in session.monitored_attributes:
                attr_change = self._analyze_attribute_change(attr_name, attr_data)
                if attr_change:
                    relevant_changes[attr_name] = attr_change

                    # Check for security events
                    security_event = self._detect_security_event(attr_name, attr_change)
                    if security_event:
                        security_events.append(security_event)

        if not relevant_changes:
            return None

        # Create change record
        change = ADObjectChange(
            object_dn=obj_data.get("distinguishedName", ""),
            object_guid=object_guid,
            object_class=obj_data.get("objectClass", ""),
            change_type=ChangeType.MODIFIED,  # Could be determined from metadata
            timestamp=datetime.now(),
            usn=obj_data.get("uSNChanged", 0),
            version=max(attr_data.get("version", 1) for attr_data in attributes.values()),
            attributes=cast(Dict[str, Any], relevant_changes),
            security_events=security_events,
            explanation=self._generate_change_explanation(relevant_changes)
        )

        return change

    async def _handle_change_detection(self, change: ADObjectChange, session: MonitoringSession) -> None:
        """Handle detected change"""
        # Add to history
        self.change_history.append(change)
        session.change_history.append(change)

        # Trim history if needed
        if len(self.change_history) > self.monitoring_config.max_history_size:
            self.change_history = self.change_history[-self.monitoring_config.max_history_size:]

        max_session_history = self.monitoring_config.max_history_size // max(1, len(self.monitoring_sessions))
        if len(session.change_history) > max_session_history:
            session.change_history = session.change_history[-max_session_history:]

        # Record security events
        for event_type in change.security_events:
            self.security_events.append((event_type, change))

        # Send alerts if configured
        if self.alert_provider:
            severity = self._determine_change_severity(change)
            await self.alert_provider.send_alert(change, severity, {"session_id": session.session_id})

            if change.security_events:
                await self.alert_provider.send_security_alert(change.security_events, change)

        logger.info(f"Detected AD change: {change.object_dn} - {change.explanation}")

    def _analyze_attribute_change(self, attr_name: str, attr_data: Dict[str, Any]) -> Optional[AttributeChange]:
        """Analyze an attribute change"""
        current_value = attr_data.get("attributeValue")
        previous_value = attr_data.get("previousValue")

        if current_value == previous_value:
            return None

        change_type = AttributeChangeType.MODIFIED
        if previous_value is None:
            change_type = AttributeChangeType.ADDED
        elif current_value is None:
            change_type = AttributeChangeType.DELETED

        return AttributeChange(
            attribute_name=attr_name,
            new_value=current_value,
            old_value=previous_value,
            change_type=change_type,
            usn=attr_data.get("localChangeUsn", 0),
            version=attr_data.get("version", 1),
            explanation=self._explain_attribute_change(attr_name, current_value, previous_value)
        )

    def _detect_security_event(self, attr_name: str, change: AttributeChange) -> Optional[SecurityEventType]:
        """Detect security-relevant events"""
        if attr_name == "userAccountControl":
            return SecurityEventType.USER_ACCOUNT_CONTROL_CHANGE
        elif attr_name in ["pwdLastSet", "unicodePwd"]:
            return SecurityEventType.PASSWORD_CHANGE
        elif attr_name == "member":
            return SecurityEventType.GROUP_MEMBERSHIP_CHANGE
        elif attr_name == "adminCount" and change.new_value:
            return SecurityEventType.PRIVILEGE_ESCALATION

        return None

    def _generate_change_explanation(self, changes: Dict[str, AttributeChange]) -> str:
        """Generate human-readable explanation for changes"""
        explanations = []
        for attr_name, change in changes.items():
            explanations.append(change.explanation or f"{attr_name}: {change.change_type.value}")

        return "; ".join(explanations)

    def _explain_attribute_change(self, attr_name: str, new_value: Any, old_value: Any) -> str:
        """Generate explanation for attribute change"""
        if attr_name == "userAccountControl":
            return self._explain_uac_change(new_value, old_value)
        elif attr_name == "member":
            return self._explain_membership_change(new_value, old_value)
        elif attr_name in ["pwdLastSet", "lockoutTime"]:
            return self._explain_time_change(attr_name, new_value)
        elif attr_name == "accountExpires":
            return self._explain_account_expiry(new_value)

        return f"Changed from '{old_value}' to '{new_value}'"

    def _explain_uac_change(self, new_value: int, old_value: int) -> str:
        """Explain User Account Control changes"""
        uac_flags = {
            0x0001: "SCRIPT",
            0x0002: "ACCOUNTDISABLE",
            0x0008: "HOMEDIR_REQUIRED",
            0x0010: "LOCKOUT",
            0x0020: "PASSWD_NOTREQD",
            0x0040: "PASSWD_CANT_CHANGE",
            0x0080: "ENCRYPTED_TEXT_PWD_ALLOWED",
            0x0100: "TEMP_DUPLICATE_ACCOUNT",
            0x0200: "NORMAL_ACCOUNT",
            0x1000: "INTERDOMAIN_TRUST_ACCOUNT",
            0x2000: "WORKSTATION_TRUST_ACCOUNT",
            0x4000: "SERVER_TRUST_ACCOUNT",
            0x8000: "DONT_EXPIRE_PASSWORD",
            0x10000: "MNS_LOGON_ACCOUNT",
            0x20000: "SMARTCARD_REQUIRED",
            0x40000: "TRUSTED_FOR_DELEGATION",
            0x80000: "NOT_DELEGATED",
            0x100000: "USE_DES_KEY_ONLY",
            0x200000: "DONT_REQ_PREAUTH",
            0x400000: "PASSWORD_EXPIRED",
            0x800000: "TRUSTED_TO_AUTH_FOR_DELEGATION"
        }

        new_flags = [value for flag, value in uac_flags.items() if new_value & flag]
        old_flags = [value for flag, value in uac_flags.items() if old_value & flag]

        added = set(new_flags) - set(old_flags)
        removed = set(old_flags) - set(new_flags)

        changes = []
        if added:
            changes.append(f"Added: {', '.join(added)}")
        if removed:
            changes.append(f"Removed: {', '.join(removed)}")

        return "; ".join(changes) if changes else "UAC flags changed"

    def _explain_membership_change(self, new_value: Any, old_value: Any) -> str:
        """Explain group membership changes"""
        # This would analyze member additions/removals
        return "Group membership changed"

    def _explain_time_change(self, attr_name: str, value: Any) -> str:
        """Explain time-based attribute changes"""
        if isinstance(value, int) and value > 0:
            try:
                dt = datetime.fromtimestamp(value / 10000000 - 11644473600)  # Windows FILETIME to Unix
                return f"{attr_name}: {dt.isoformat()}"
            except Exception:
                pass
        return f"{attr_name} changed"

    def _explain_account_expiry(self, value: Any) -> str:
        """Explain account expiry changes"""
        if value == 0 or (isinstance(value, int) and value > 9223372036854775807):
            return "Account set to never expire"
        elif isinstance(value, int):
            try:
                dt = datetime.fromtimestamp(value / 10000000 - 11644473600)
                return f"Account expires: {dt.isoformat()}"
            except Exception:
                pass
        return "Account expiry changed"

    def _determine_change_severity(self, change: ADObjectChange) -> str:
        """Determine severity level for change"""
        if any(event in [
            SecurityEventType.PRIVILEGE_ESCALATION,
            SecurityEventType.ADMIN_ACCESS_CHANGE
        ] for event in change.security_events):
            return "critical"

        if any(event in [
            SecurityEventType.PASSWORD_CHANGE,
            SecurityEventType.USER_ACCOUNT_CONTROL_CHANGE
        ] for event in change.security_events):
            return "high"

        if change.security_events:
            return "medium"

        return "low"

    async def _initialize_session_usn(self, session: MonitoringSession) -> None:
        """Initialize USN for monitoring session"""
        if not self.ad_provider:
            return

        connection = await self.ad_provider.connect(session.domain_controller)
        try:
            session.start_usn = await self.ad_provider.get_current_usn(connection)
            session.current_usn = session.start_usn
        finally:
            await self.ad_provider.disconnect(connection)

    async def get_change_history(
        self,
        session_id: Optional[str] = None,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ADObjectChange]:
        """Get change history with optional filtering"""
        history = self.change_history
        if session_id:
            session = self.monitoring_sessions.get(session_id)
            if session:
                history = session.change_history

        # Apply filters
        if filters:
            filtered_history = []
            for change in history:
                if self._matches_filters(change, filters):
                    filtered_history.append(change)
            history = filtered_history

        return history[-limit:] if limit > 0 else history

    async def get_security_events(
        self,
        event_types: Optional[List[SecurityEventType]] = None,
        limit: int = 100
    ) -> List[Tuple[SecurityEventType, ADObjectChange]]:
        """Get security events"""
        events = self.security_events
        if event_types:
            events = [e for e in events if e[0] in event_types]

        return events[-limit:] if limit > 0 else events

    def _matches_filters(self, change: ADObjectChange, filters: Dict[str, Any]) -> bool:
        """Check if change matches filters"""
        for key, value in filters.items():
            if key == "object_class" and change.object_class != value:
                return False
            elif key == "change_type" and change.change_type != value:
                return False
            elif key == "security_events" and not any(e in change.security_events for e in value):
                return False
            elif key == "time_range":
                start_time, end_time = value
                if not (start_time <= change.timestamp <= end_time):
                    return False

        return True

    # Placeholder methods for security rule checks
    def _check_user_account_control(self, change: AttributeChange) -> Optional[SecurityEventType]:
        """Check for suspicious UAC changes"""
        # Implementation would analyze UAC flag changes for security implications
        return None

    def _check_group_membership(self, change: AttributeChange) -> Optional[SecurityEventType]:
        """Check for group membership changes"""
        return SecurityEventType.GROUP_MEMBERSHIP_CHANGE

    def _check_password_changes(self, change: AttributeChange) -> Optional[SecurityEventType]:
        """Check for password changes"""
        return SecurityEventType.PASSWORD_CHANGE

    def _check_privilege_escalation(self, change: AttributeChange) -> Optional[SecurityEventType]:
        """Check for privilege escalation indicators"""
        return None

    def _check_admin_access(self, change: AttributeChange) -> Optional[SecurityEventType]:
        """Check for admin access changes"""
        return None

    # Provider setters
    def set_ad_provider(self, provider: ADConnectionProvider) -> None:
        """Set the AD connection provider"""
        self.ad_provider = provider

    def set_alert_provider(self, provider: AlertProvider) -> None:
        """Set the alert provider"""
        self.alert_provider = provider

    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self.stop_monitoring()

        # Clear history beyond retention period
        cutoff_date = datetime.now() - timedelta(days=self.monitoring_config.retention_days)
        self.change_history = [c for c in self.change_history if c.timestamp > cutoff_date]
        self.security_events = [e for e in self.security_events if e[1].timestamp > cutoff_date]

        logger.info("AD Monitoring Core cleaned up")

    # BaseCore interface implementation
    async def initialize(self, context: CascadeContext = None) -> bool:
        """Initialize the core"""
        try:
            self._initialize_core()
            return True
        except Exception as e:
            logger.error(f"Failed to initialize AD Monitoring Core: {e}")
            return False

    async def shutdown(self, context: CascadeContext = None) -> bool:
        """Shutdown the core"""
        try:
            await self.cleanup()
            return True
        except Exception as e:
            logger.error(f"Failed to shutdown AD Monitoring Core: {e}")
            return False

    async def health_check(self, context: CascadeContext = None) -> Dict[str, Any]:
        """Health check for the core"""
        active_sessions = sum(1 for s in self.monitoring_sessions.values() if s.is_active)

        return {
            "status": "healthy" if active_sessions > 0 or not self.monitoring_sessions else "idle",
            "active_sessions": active_sessions,
            "total_sessions": len(self.monitoring_sessions),
            "change_history_size": len(self.change_history),
            "security_events_count": len(self.security_events),
            "providers_configured": {
                "ad_connection": self.ad_provider is not None,
                "alert": self.alert_provider is not None
            },
            "is_monitoring": self.is_monitoring
        }

    async def get_metrics(self, context: CascadeContext = None) -> Dict[str, Any]:
        """Get core metrics"""
        return {
            "monitoring_sessions": len(self.monitoring_sessions),
            "changes_detected": len(self.change_history),
            "security_events": len(self.security_events),
            "uptime": 0,  # Would track actual uptime
            "average_check_interval": self.monitoring_config.check_interval,
            "domain_controllers": len(self.monitoring_config.domain_controllers)
        }

    async def process_task(
        self,
        task_data: Dict[str, Any],
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Process a task through the monitoring core"""
        task_type = task_data.get("type", "unknown")

        if task_type == "start_monitoring":
            dc_list = cast(List[str], task_data.get("domain_controllers"))
            session_id = await self.start_monitoring(dc_list, context)
            return {"session_id": session_id, "status": "started"}

        elif task_type == "stop_monitoring":
            session_id = cast(str, task_data.get("session_id"))
            await self.stop_monitoring(session_id, context)
            return {"status": "stopped"}

        elif task_type == "get_changes":
            session_id = cast(str, task_data.get("session_id"))
            limit = task_data.get("limit", 100)
            filters = task_data.get("filters", {})
            changes = await self.get_change_history(session_id, limit, filters)
            return {"changes": [self._change_to_dict(c) for c in changes]}

        elif task_type == "get_security_events":
            event_types = cast(List[SecurityEventType], task_data.get("event_types"))
            limit = task_data.get("limit", 100)
            events = await self.get_security_events(event_types, limit)
            return {"events": [(e[0].value, self._change_to_dict(e[1])) for e in events]}

        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _change_to_dict(self, change: ADObjectChange) -> Dict[str, Any]:
        """Convert change object to dictionary"""
        return {
            "object_dn": change.object_dn,
            "object_guid": change.object_guid,
            "object_class": change.object_class,
            "change_type": change.change_type.value,
            "timestamp": change.timestamp.isoformat(),
            "usn": change.usn,
            "version": change.version,
            "attributes": {k: str(v) for k, v in change.attributes.items()},
            "security_events": [e.value for e in change.security_events],
            "explanation": change.explanation
        }
