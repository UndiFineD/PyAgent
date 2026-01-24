
"""
Operational cost agent.py module.
"""
# Copyright 2026 PyAgent Authors
# Apache 2.0 License

from __future__ import annotations

from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent


class OperationalCostAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Phase 286: Operational Cost Agent.
    Estimates the real-world dollar cost of improvement cycles based on model usage.
    """

    def __init__(self, file_path: str = "budget.audit") -> None:
        super().__init__(file_path)
        self.pricing = {
            "Ollama": 0.0,
            "GPT-4o": 15.00,  # Per 1M tokens
            "GPT-4o-mini": 0.15,
            "Claude-3.5-Sonnet": 3.00,
            "DeepSeek-V3": 0.20,
            "GLM-4": 0.10,
        }

    @as_tool
    async def calculate_run_cost(self, token_usage: dict[str, Any]) -> dict[str, Any]:
        """
        Calculates cost based on token usage.
        Example token_usage: {"GPT-4o": 500000, "Ollama": 1200000}
        """
        total_usd = 0.0
        details = []

        for model, count in token_usage.items():
            rate = self.pricing.get(model, 1.0)  # Default to 1.0/million if unknown
            cost = (count / 1_000_000) * rate
            total_usd += cost
            details.append({"model": model, "tokens": count, "cost_usd": round(cost, 4)})

        return {"total_usd": round(total_usd, 2), "breakdown": details}

    async def get_improvement_items(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        """Provides financial audit results."""
        _ = context
        # Financial agent doesn't modify code directly, it audits.
        return []

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Analyze operational cost based on prompt data."""
        _ = target_file
        # Assume prompt contains json of token usage
        import json

        try:
            usage = json.loads(prompt)
            report = await self.calculate_run_cost(usage)
            return f"Cost Analysis: ${report['total_usd']} USD."
        except json.JSONDecodeError:
            return "Usage: OperationalCostAgent requires a JSON string of token usage patterns."
