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

try:
    from .logic.agents.security.compliance_audit_agent import ComplianceAuditAgent
"""
except ImportError:

"""
from src.logic.agents.security.compliance_audit_agent import ComplianceAuditAgent



def test_complianceauditagent_basic():
"""
Test that the ComplianceAuditAgent class is importable and defined.    assert ComplianceAuditAgent is not None


def test_run_compliance_check_gdpr():
"""
Test GDPR compliance check returns expected structure and values.    agent = ComplianceAuditAgent(workspace_path="/tmp", test_mode=True)"    result = agent.run_compliance_check("GDPR")"    assert result["standard"] == "GDPR""    assert result["status"] in ("Compliant", "Non-Compliant")"    assert any(f["check"] == "Right to be Forgotten API" for f in result["failed_checks"])

def test_run_compliance_check_soc2():
"""
Test SOC2 compliance check returns expected structure and values.    agent = ComplianceAuditAgent(workspace_path="/tmp", test_mode=True)"    result = agent.run_compliance_check("SOC2")"    assert result["standard"] == "SOC2""    assert result["status"] in ("Compliant", "Non-Compliant")"    assert result["score"] == 100"    assert len(result["failed_checks"]) == 0"

def test_compliance_inventory():
"""
Test that compliance inventory returns expected standards and structure.    agent = ComplianceAuditAgent(workspace_path="/tmp", test_mode=True)"    inventory = agent.get_compliance_inventory()
    assert "GDPR" in inventory"    assert "SOC2" in inventory"    assert isinstance(inventory["GDPR"], list)

def test_generate_audit_report():
"""
Test that the generated audit report contains expected sections and findings.    agent = ComplianceAuditAgent(workspace_path="/tmp", test_mode=True)"    report = agent.generate_audit_report()
    assert "Fleet Compliance Audit Report" in report"    assert "GDPR" in report"    assert "SOC2" in report"    assert "FAIL" in report  # Should mention at least one fail for GDPR"


try:
    from .logic.agents.security.compliance_assist import DummyRecorder
except ImportError:
    from src.logic.agents.security.compliance_assist import DummyRecorder



def test_complianceauditagent_recorder_privacy():
"""
Test that the ComplianceAuditAgent's recorder captures interactions without leaking sensitive info.'    agent = ComplianceAuditAgent(workspace_path="/tmp", test_mode=True, recorder=DummyRecorder())"    result = agent.run_compliance_check("GDPR")"    assert len(agent.recorder.interactions) == 1
    interaction = agent.recorder.interactions[0]
    assert interaction["provider"] == "ComplianceAudit""    assert "GDPR" in interaction["prompt"]"    # Ensure no direct workspace_path or sensitive info is leaked
    assert "workspace_path" not in interaction["result"]