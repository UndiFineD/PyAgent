# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.logic.agents.security.compliance_agent import ComplianceAgent

class PrivacyAssessmentMixin:
    """Mixin for conducting Privacy Impact Assessments in ComplianceAgent."""

    def generate_privacy_impact_assessment(
        self: ComplianceAgent, project_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Phase 240: Conducts a Privacy Impact Assessment (PIA)."""
        score = 100
        risks = []

        # Check for high-risk data types
        pii_found = project_data.get("pii_types", [])
        if any(t in ["ssn", "credit_card", "health_record"] for t in pii_found):
            score -= 40
            risks.append("High-risk PII collection (SSN/Financial/Health)")
        elif pii_found:
            score -= 15
            risks.append(f"Basic PII collection: {', '.join(pii_found)}")

        # Check for data retention policy
        retention = project_data.get("retention_period_days")
        if not retention:
            score -= 20
            risks.append("No clear data retention policy defined")
        elif retention > 365:
            score -= 10
            risks.append(
                f"Long retention period ({retention} days) increases exposure risk"
            )

        # Check for encryption status
        if not project_data.get("encrypted_at_rest", False):
            score -= 25
            risks.append("Data not encrypted at rest")

        # Check for purpose limitation
        if not project_data.get("collection_purpose"):
            score -= 10
            risks.append("Missing explicit collection purpose statement")

        return {
            "pia_score": max(0, score),
            "risk_assessment": "High"
            if score < 50
            else "Medium"
            if score < 80
            else "Low",
            "findings": risks,
            "recommendations": self._get_pia_recommendations(risks),
            "timestamp": time.time(),
        }

    def _get_pia_recommendations(self: ComplianceAgent, risks: list[str]) -> list[str]:
        recommendations = []
        for risk in risks:
            if "encryption" in risk.lower():
                recommendations.append(
                    "Implement AES-256 encryption at rest for all database shards."
                )
            if "retention" in risk.lower():
                recommendations.append(
                    "Implement automated data pruning for records older than 90 days."
                )
            if "High-risk PII" in risk:
                recommendations.append(
                    "Consider data tokenization or removal of SSN/Financial data if not strictly necessary."
                )
        return recommendations
