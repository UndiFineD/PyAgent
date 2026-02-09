# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\praisonaiagents\guardrails\__init__.py
"""
Guardrails module for PraisonAI Agents.

This module provides validation and safety mechanisms for task outputs,
including both function-based and LLM-based guardrails.
"""

from .guardrail_result import GuardrailResult
from .llm_guardrail import LLMGuardrail

__all__ = ["GuardrailResult", "LLMGuardrail"]
