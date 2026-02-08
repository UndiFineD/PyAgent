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
Advanced Threat Hunting Core

Inspired by APT-Hunter tool for Windows event log analysis.
Implements threat hunting patterns using detection rules and statistical analysis.
"""

import logging
import re
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import pandas as pd
from datetime import datetime


@dataclass
class DetectionRule:
    """Threat detection rule"""
    id: str
    name: str
    description: str
    event_ids: List[int]
    conditions: Dict[str, Any]
    severity: str
    tags: List[str]


@dataclass
class ThreatFinding:
    """Threat hunting finding"""
    rule_id: str
    timestamp: datetime
    event_id: int
    description: str
    severity: str
    indicators: Dict[str, Any]
    raw_event: Dict[str, Any]


@dataclass
class HuntingResult:
    """Result from threat hunting analysis"""
    total_events: int
    findings: List[ThreatFinding]
    statistics: Dict[str, Any]
    timeline: List[Dict[str, Any]]


class AdvancedThreatHuntingCore:
    """
    Core for advanced threat hunting and APT detection.

    Based on APT-Hunter patterns for Windows event log analysis.
    Implements rule-based detection with statistical analysis.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rules: Dict[str, DetectionRule] = {}
        self.load_default_rules()

    def load_default_rules(self):
        """Load default threat detection rules"""
        self.rules = {
            "lateral_movement_psexec": DetectionRule(
                id="lateral_movement_psexec",
                name="PsExec Lateral Movement",
                description="Detects PsExec service creation for lateral movement",
                event_ids=[7045, 4688],
                conditions={
                    "service_name": r"psexesvc",
                    "image_path": r"\\.*\\psexesvc\.exe"
                },
                severity="high",
                tags=["lateral_movement", "psexec", "apt"]
            ),
            "suspicious_logon": DetectionRule(
                id="suspicious_logon",
                name="Suspicious Logon Pattern",
                description="Detects unusual logon patterns that may indicate compromise",
                event_ids=[4625, 4624],
                conditions={
                    "logon_type": [3, 10],  # Network, RemoteInteractive
                    "failure_reason": "0xC000006A"  # Wrong password with correct username
                },
                severity="medium",
                tags=["authentication", "brute_force"]
            ),
            "privilege_escalation": DetectionRule(
                id="privilege_escalation",
                name="Privilege Escalation Attempt",
                description="Detects attempts to escalate privileges",
                event_ids=[4672, 4673, 4674],
                conditions={
                    "special_privileges": ["SeDebugPrivilege", "SeTakeOwnershipPrivilege"]
                },
                severity="high",
                tags=["privilege_escalation", "apt"]
            ),
            "unusual_process": DetectionRule(
                id="unusual_process",
                name="Unusual Process Execution",
                description="Detects execution of unusual or suspicious processes",
                event_ids=[4688],
                conditions={
                    "parent_process": r"(?:services|svchost)\.exe",
                    "command_line": r"(?:powershell|cmd)\.exe.*(?:-enc|-encodedcommand|\/c)"
                },
                severity="medium",
                tags=["process_execution", "suspicious"]
            ),
            "reconnaissance": DetectionRule(
                id="reconnaissance",
                name="System Reconnaissance",
                description="Detects system reconnaissance activities",
                event_ids=[4663, 5145],
                conditions={
                    "object_access": ["ReadData", "ListDirectory"],
                    "sensitive_paths": [r"C:\\Windows\\System32\\config", r"C:\\Users\\.*\\Documents"]
                },
                severity="low",
                tags=["reconnaissance", "discovery"]
            )
        }

    async def hunt_threats(self, event_logs: List[Dict[str, Any]],
                          time_range: Optional[tuple] = None,
                          rules_filter: Optional[List[str]] = None) -> HuntingResult:
        """
        Perform threat hunting analysis on event logs.

        Args:
            event_logs: List of Windows event log entries
            time_range: Optional (start_time, end_time) tuple
            rules_filter: Optional list of rule IDs to apply

        Returns:
            HuntingResult with findings and statistics
        """
        findings = []
        active_rules = rules_filter or list(self.rules.keys())

        # Filter events by time range if specified
        filtered_events = event_logs
        if time_range:
            start_time, end_time = time_range
            filtered_events = [
                event for event in event_logs
                if start_time <= datetime.fromisoformat(event.get('timestamp', '1970-01-01')) <= end_time
            ]

        # Apply detection rules
        for event in filtered_events:
            for rule_id in active_rules:
                if rule_id not in self.rules:
                    continue

                rule = self.rules[rule_id]
                if event.get('event_id') in rule.event_ids:
                    if self._matches_conditions(event, rule.conditions):
                        finding = ThreatFinding(
                            rule_id=rule.id,
                            timestamp=datetime.fromisoformat(event.get('timestamp', '1970-01-01')),
                            event_id=event.get('event_id', 0),
                            description=rule.description,
                            severity=rule.severity,
                            indicators=self._extract_indicators(event, rule.conditions),
                            raw_event=event
                        )
                        findings.append(finding)

        # Generate statistics
        statistics = self._generate_statistics(findings, filtered_events)

        # Create timeline
        timeline = self._create_timeline(findings)

        return HuntingResult(
            total_events=len(filtered_events),
            findings=findings,
            statistics=statistics,
            timeline=timeline
        )

    def _matches_conditions(self, event: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
        """Check if event matches rule conditions"""
        for key, expected in conditions.items():
            if key not in event:
                continue

            actual = event[key]

            if isinstance(expected, list):
                if actual not in expected:
                    return False
            elif isinstance(expected, str) and expected.startswith('r'):
                # Regex pattern
                if not re.search(expected, str(actual), re.IGNORECASE):
                    return False
            else:
                if actual != expected:
                    return False

        return True

    def _extract_indicators(self, event: Dict[str, Any], conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant indicators from matching event"""
        indicators = {}
        for key in conditions.keys():
            if key in event:
                indicators[key] = event[key]
        return indicators

    def _generate_statistics(self, findings: List[ThreatFinding],
                           events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistical analysis of findings"""
        stats = {
            "total_findings": len(findings),
            "severity_breakdown": {},
            "rule_breakdown": {},
            "event_id_frequency": {},
            "temporal_distribution": {}
        }

        # Severity breakdown
        for finding in findings:
            stats["severity_breakdown"][finding.severity] = \
                stats["severity_breakdown"].get(finding.severity, 0) + 1

        # Rule breakdown
        for finding in findings:
            stats["rule_breakdown"][finding.rule_id] = \
                stats["rule_breakdown"].get(finding.rule_id, 0) + 1

        # Event ID frequency
        for event in events:
            event_id = event.get('event_id', 'unknown')
            stats["event_id_frequency"][str(event_id)] = \
                stats["event_id_frequency"].get(str(event_id), 0) + 1

        # Temporal distribution (hourly)
        for finding in findings:
            hour = finding.timestamp.hour
            stats["temporal_distribution"][str(hour)] = \
                stats["temporal_distribution"].get(str(hour), 0) + 1

        return stats

    def _create_timeline(self, findings: List[ThreatFinding]) -> List[Dict[str, Any]]:
        """Create chronological timeline of findings"""
        timeline = []
        sorted_findings = sorted(findings, key=lambda x: x.timestamp)

        for finding in sorted_findings:
            timeline.append({
                "timestamp": finding.timestamp.isoformat(),
                "rule_id": finding.rule_id,
                "severity": finding.severity,
                "description": finding.description,
                "indicators": finding.indicators
            })

        return timeline

    def export_results(self, result: HuntingResult,
                           output_format: str = "json",
                           filename: str = "threat_hunt_results") -> str:
        """
        Export hunting results to file.

        Args:
            result: HuntingResult to export
            output_format: "json", "csv", or "excel"
            filename: Base filename for output

        Returns:
            Path to exported file
        """
        if output_format == "json":
            data = {
                "summary": {
                    "total_events": result.total_events,
                    "total_findings": len(result.findings),
                    "statistics": result.statistics
                },
                "findings": [
                    {
                        "rule_id": f.rule_id,
                        "timestamp": f.timestamp.isoformat(),
                        "severity": f.severity,
                        "description": f.description,
                        "indicators": f.indicators
                    } for f in result.findings
                ],
                "timeline": result.timeline
            }

            filepath = "{}.json".format(filename)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            return filepath

        elif output_format == "csv":
            # Export findings as CSV
            findings_data = []
            for finding in result.findings:
                findings_data.append({
                    "timestamp": finding.timestamp.isoformat(),
                    "rule_id": finding.rule_id,
                    "severity": finding.severity,
                    "description": finding.description,
                    **finding.indicators
                })

            df = pd.DataFrame(findings_data)
            filepath = "{}_findings.csv".format(filename)
            df.to_csv(filepath, index=False)

            # Export timeline as separate CSV
            timeline_data = []
            for entry in result.timeline:
                timeline_data.append({
                    "timestamp": entry["timestamp"],
                    "rule_id": entry["rule_id"],
                    "severity": entry["severity"],
                    "description": entry["description"]
                })

            df_timeline = pd.DataFrame(timeline_data)
            timeline_filepath = "{}_timeline.csv".format(filename)
            df_timeline.to_csv(timeline_filepath, index=False)

            return filepath

        else:
            raise ValueError("Unsupported output format: " + output_format)
