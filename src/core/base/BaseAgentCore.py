#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""BaseAgentCore - Pure logic and calculation methods for agent operations.

This module contains all pure computational logic without I/O operations,
making it a candidate for Rust conversion. It handles:
- Anchoring strength calculations
- Self-verification logic
- Strategy matching and evaluation
- Configuration validation
- Response quality assessment
- Capability enumeration
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Tuple
from src.core.base.models import (
    AgentConfig,
    ResponseQuality,
    AgentPriority,
)
from src.core.base.verification import AgentVerifier

logger = logging.getLogger(__name__)


class BaseAgentCore:
    """Pure logic core for agent operations (Rust-convertible).
    
    Contains all computational methods without I/O dependencies.
    Designed for high performance and potential Rust translation.
    """

    def __init__(self) -> None:
        """Initialize the core logic engine."""
        self.context_pool: Dict[str, Any] = {}
        
    def calculate_anchoring_strength(self, result: str, context_pool: Optional[Dict[str, Any]] = None) -> float:
        """Calculate the 'Anchoring Strength' metric (Stanford Research 2025).
        
        Pure calculation based on result and context.
        No I/O operations.
        
        Args:
            result: The result string to evaluate
            context_pool: Optional context for anchoring calculation
            
        Returns:
            Anchoring strength score as float
        """
        if context_pool is None:
            context_pool = self.context_pool
        return AgentVerifier.calculate_anchoring_strength(result, context_pool)

    def verify_self(self, result: str) -> Tuple[bool, str]:
        """Self-verification layer (inspired by Keio University 2026 research).
        
        Pure validation logic without side effects.
        
        Args:
            result: The result string to verify
            
        Returns:
            Tuple of (is_valid, reason)
        """
        anchoring_score = self.calculate_anchoring_strength(result)
        return AgentVerifier.verify_self(result, anchoring_score)

    def validate_config(self, config: AgentConfig) -> Tuple[bool, str]:
        """Validate agent configuration.
        
        Pure validation without side effects.
        
        Args:
            config: AgentConfig to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not config.backend:
            return False, "Backend must be specified"
        
        if config.max_tokens <= 0:
            return False, "max_tokens must be > 0"
        
        if not (0.0 <= config.temperature <= 2.0):
            return False, "temperature must be between 0.0 and 2.0"
        
        if config.retry_count < 0:
            return False, "retry_count must be >= 0"
        
        if config.timeout <= 0:
            return False, "timeout must be > 0"
        
        return True, ""

    def set_strategy(self, strategy: Any) -> str:
        """Validate and prepare strategy for use.
        
        Pure logic without side effects.
        
        Args:
            strategy: An instance of AgentStrategy
            
        Returns:
            Status message
        """
        if strategy is None:
            return "ERROR: Strategy cannot be None"
        
        if not hasattr(strategy, 'execute'):
            return f"ERROR: Strategy {strategy.__class__.__name__} missing 'execute' method"
        
        return f"Strategy set to {strategy.__class__.__name__}"

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities list.
        
        Pure data retrieval without I/O.
        
        Returns:
            List of capability strings
        """
        return ["base", "calculation", "verification"]

    def assess_response_quality(self, response: str, metadata: Optional[Dict[str, Any]] = None) -> ResponseQuality:
        """Assess the quality of a response.
        
        Pure calculation based on response content and metadata.
        
        Args:
            response: The response string to assess
            metadata: Optional metadata for assessment
            
        Returns:
            ResponseQuality score
        """
        if metadata is None:
            metadata = {}
        
        # Pure calculation logic
        score = 0.5  # Base score
        
        # Check length
        if len(response) > 100:
            score += 0.1
        
        # Check for key indicators
        if "error" not in response.lower() and "fail" not in response.lower():
            score += 0.1
        
        # Check metadata
        if metadata.get("has_references"):
            score += 0.1
        
        if metadata.get("is_complete"):
            score += 0.1
        
        return ResponseQuality(
            score=min(1.0, score),
            has_errors=False,
            completeness=metadata.get("completeness", 0.8)
        )

    def filter_events(self, events: List[Dict[str, Any]], event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Filter events based on type.
        
        Pure filtering logic.
        
        Args:
            events: List of event dictionaries
            event_type: Optional type to filter by
            
        Returns:
            Filtered list of events
        """
        if not event_type:
            return events
        
        return [e for e in events if e.get("type") == event_type]

    def deduplicate_entries(self, entries: List[str]) -> List[str]:
        """Deduplicate string entries while preserving order.
        
        Pure deduplication logic.
        
        Args:
            entries: List of strings to deduplicate
            
        Returns:
            Deduplicated list preserving order
        """
        seen = set()
        result = []
        for entry in entries:
            if entry not in seen:
                seen.add(entry)
                result.append(entry)
        return result

    def calculate_priority_score(self, priority: AgentPriority, urgency: float) -> float:
        """Calculate effective priority score.
        
        Pure calculation combining priority level and urgency.
        
        Args:
            priority: AgentPriority level
            urgency: Urgency factor (0.0 to 1.0)
            
        Returns:
            Combined priority score
        """
        priority_base = {
            AgentPriority.LOW: 0.2,
            AgentPriority.NORMAL: 0.5,
            AgentPriority.HIGH: 0.8,
            AgentPriority.CRITICAL: 1.0,
        }.get(priority, 0.5)
        
        # Blend priority with urgency (70% priority, 30% urgency)
        return (priority_base * 0.7) + (urgency * 0.3)

    def merge_configurations(self, base: AgentConfig, override: AgentConfig) -> AgentConfig:
        """Merge two configurations, with override taking precedence.
        
        Pure configuration merging logic.
        
        Args:
            base: Base configuration
            override: Override configuration
            
        Returns:
            Merged configuration
        """
        return AgentConfig(
            backend=override.backend or base.backend,
            model=override.model or base.model,
            max_tokens=override.max_tokens if override.max_tokens != base.max_tokens else base.max_tokens,
            temperature=override.temperature if override.temperature != base.temperature else base.temperature,
            retry_count=override.retry_count if override.retry_count != base.retry_count else base.retry_count,
            timeout=override.timeout if override.timeout != base.timeout else base.timeout,
            cache_enabled=override.cache_enabled if override.cache_enabled != base.cache_enabled else base.cache_enabled,
            token_budget=override.token_budget if override.token_budget != base.token_budget else base.token_budget,
        )

    def normalize_response(self, response: str) -> str:
        """Normalize response text for consistency.
        
        Pure text normalization.
        
        Args:
            response: Response text to normalize
            
        Returns:
            Normalized response
        """
        # Strip whitespace
        normalized = response.strip()
        
        # Normalize line endings
        normalized = normalized.replace('\r\n', '\n')
        
        # Remove multiple spaces
        normalized = ' '.join(normalized.split())
        
        return normalized

    def calculate_token_estimate(self, text: str, chars_per_token: float = 4.0) -> int:
        """Estimate token count (pure calculation).
        
        Uses character-to-token ratio approximation.
        No API calls.
        
        Args:
            text: Text to estimate tokens for
            chars_per_token: Average characters per token (default: 4.0)
            
        Returns:
            Estimated token count
        """
        return max(1, int(len(text) / chars_per_token))

    def is_response_valid(self, response: str, min_length: int = 10) -> Tuple[bool, str]:
        """Validate response meets minimum criteria.
        
        Pure validation logic.
        
        Args:
            response: Response to validate
            min_length: Minimum response length
            
        Returns:
            Tuple of (is_valid, reason)
        """
        if not response:
            return False, "Response is empty"
        
        if len(response) < min_length:
            return False, f"Response too short (< {min_length} chars)"
        
        if len(response) > 1000000:
            return False, "Response too long (> 1M chars)"
        
        return True, ""
