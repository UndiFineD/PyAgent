#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from .ErrorBudget import ErrorBudget

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess

class ErrorBudgetManager:
    """Manages error budgets for SLO tracking.

    Tracks error budget consumption over time periods
    to support SLO management.

    Attributes:
        budgets: Map of budget names to ErrorBudget objects.
    """

    def __init__(self) -> None:
        """Initialize the error budget manager."""
        self.budgets: Dict[str, ErrorBudget] = {}

    def create_budget(
        self,
        name: str,
        total: float,
        period_days: int = 30
    ) -> ErrorBudget:
        """Create an error budget.

        Args:
            name: Budget name.
            total: Total budget amount.
            period_days: Budget period in days.

        Returns:
            The created ErrorBudget.
        """
        now = datetime.now()
        end = now + timedelta(days=period_days)
        budget = ErrorBudget(
            budget_name=name,
            total_budget=total,
            period_start=now.isoformat(),
            period_end=end.isoformat()
        )
        self.budgets[name] = budget
        return budget

    def consume(self, name: str, amount: float) -> bool:
        """Consume error budget.

        Args:
            name: Budget name.
            amount: Amount to consume.

        Returns:
            True if budget was consumed, False if exceeded.
        """
        if name not in self.budgets:
            return False
        budget = self.budgets[name]
        if budget.consumed + amount > budget.total_budget:
            return False
        budget.consumed += amount
        return True

    def get_remaining(self, name: str) -> float:
        """Get remaining budget.

        Args:
            name: Budget name.

        Returns:
            Remaining budget amount.
        """
        if name not in self.budgets:
            return 0.0
        budget = self.budgets[name]
        return budget.total_budget - budget.consumed

    def get_consumption_rate(self, name: str) -> float:
        """Get budget consumption rate as percentage."""
        if name not in self.budgets:
            return 0.0
        budget = self.budgets[name]
        if budget.total_budget == 0:
            return 100.0
        return (budget.consumed / budget.total_budget) * 100

    def is_exceeded(self, name: str) -> bool:
        """Check if budget is exceeded."""
        if name not in self.budgets:
            return True
        budget = self.budgets[name]
        return budget.consumed >= budget.total_budget
