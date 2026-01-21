# Copyright 2026 PyAgent Authors
import logging
from typing import Any, Dict, Optional, List, Tuple
from src.core.base.common.models import ResponseQuality, AgentPriority
from src.core.base.logic.agent_verification import AgentVerifier

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)

class MetricsCore:
    def calculate_anchoring_strength(self, result: str, context_pool: Optional[Dict[str, Any]] = None) -> float:
        """Calculate the 'Anchoring Strength' metric (Stanford Research 2025)."""
        return AgentVerifier.calculate_anchoring_strength(result, context_pool or {})

    def verify_self(self, result: str, anchoring_score: float) -> Tuple[bool, str]:
        """Self-verification layer."""
        return AgentVerifier.verify_self(result, anchoring_score)

    def assess_response_quality(self, response: str, metadata: Optional[Dict[str, Any]] = None) -> ResponseQuality:
        """Assess the quality of a response."""
        if rc:
            try:
                final_score = rc.assess_response_quality(response, metadata)
            except Exception:
                final_score = self._assess_quality_python(response, metadata)
        else:
            final_score = self._assess_quality_python(response, metadata)

        if final_score >= 0.9: return ResponseQuality.EXCELLENT
        elif final_score >= 0.7: return ResponseQuality.GOOD
        elif final_score >= 0.5: return ResponseQuality.ACCEPTABLE
        elif final_score >= 0.3: return ResponseQuality.POOR
        else: return ResponseQuality.INVALID

    def _assess_quality_python(self, response: str, metadata: Optional[Dict[str, Any]] = None) -> float:
        """Fallback Python implementation of quality assessment."""
        if metadata is None: metadata = {}
        score = 0.5
        if len(response) > 100: score += 0.1
        if "error" not in response.lower() and "fail" not in response.lower(): score += 0.1
        if metadata.get("has_references"): score += 0.1
        if metadata.get("is_complete"): score += 0.1
        return min(1.0, score)

    def calculate_priority_score(self, priority: AgentPriority, urgency: float) -> float:
        """Calculate effective priority score."""
        priority_base = {
            AgentPriority.LOW: 0.2,
            AgentPriority.NORMAL: 0.5,
            AgentPriority.HIGH: 0.8,
            AgentPriority.CRITICAL: 1.0,
        }.get(priority, 0.5)

        if rc:
            try:
                return rc.calculate_priority_score(priority_base, urgency)
            except Exception:
                pass
        return (priority_base * 0.7) + (urgency * 0.3)

    def calculate_token_estimate(self, text: str, chars_per_token: float = 4.0) -> int:
        """Estimate token count."""
        if rc:
            try:
                return rc.calculate_token_estimate(text, chars_per_token)
            except Exception:
                pass
        return max(1, int(len(text) / chars_per_token))
