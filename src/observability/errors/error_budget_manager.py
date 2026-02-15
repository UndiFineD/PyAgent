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



# Error Budget Manager - Manage SLO error budgets

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # # [Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
# USAGE:
# Import ErrorBudgetManager from this module and use it to create and track named error budgets for SLOs: create_budget(name, total, period_days=30), consume(name, amount), get_remaining(name), get_consumption_rate(name), is_exceeded(name).

# WHAT IT DOES:
# Provides an in-memory manager for ErrorBudget objects allowing creation of time-bounded budgets, consumption tracking, remaining-budget queries, consumption-rate calculation, and simple exceeded checks.

# WHAT IT SHOULD DO BETTER:
# Persist budgets to durable storage, enforce and roll budgets on period boundaries, add concurrency protection and validation, expose asynchronous APIs for integration with asyncio-based agents, emit metrics/events on consumption and breaches, and add tests for edge cases (zero budgets, negative consumes, missing budgets).

# FILE CONTENT SUMMARY:
Auto-extracted class from agent_errors.py


from __future__ import annotations

from datetime import datetime, timedelta

from src.core.base.lifecycle.version import VERSION

from .error_budget import ErrorBudget

__version__ = VERSION


# class ErrorBudgetManager:
    Manages error budgets for SLO tracking.

    Tracks error budget consumption over time periods
    to support SLO management.

    Attributes:
        budgets: Map of budget names to ErrorBudget objects.
    

    def __init__(self) -> None:
        Initialize the error budget manager.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.budgets: dict[str, ErrorBudget] = {}

    def create_budget(self, name: str, total: float, period_days: int = 30) -> ErrorBudget:
        Create an error budget.

        Args:
            name: Budget name.
            total: Total budget amount.
            period_days: Budget period in days.

        Returns:
            The created ErrorBudget.
        
        now = datetime.now()
        end = now + timedelta(days=period_days)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         budget = ErrorBudget(
            budget_name=name,
            total_budget=total,
            period_start=now.isoformat(),
            period_end=end.isoformat(),
        )
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.budgets[name] = budget
        return budget

    def consume(self, name: str, amount: float) -> bool:
        Consume error budget.

        Args:
            name: Budget name.
            amount: Amount to consume.

        Returns:
            True if budget was consumed, False if exceeded.
        
        if name not in self.budgets:
            return False
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        if budget.consumed + amount > budget.total_budget:
            return False
        budget.consumed += amount
        return True

    def get_remaining(self, name: str) -> float:
        Get remaining budget.

        Args:
            name: Budget name.

        Returns:
            Remaining budget amount.
        
        if name not in self.budgets:
            return 0.0
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        return budget.total_budget - budget.consumed

    def get_consumption_rate(self, name: str) -> float:
        Get budget consumption rate as percentage.
        if name not in self.budgets:
            return 0.0
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        if budget.total_budget == 0:
            return 100.0
        return (budget.consumed / budget.total_budget) * 100

    def is_exceeded(self, name: str) -> bool:
        Check if budget is exceeded.
        if name not in self.budgets:
            return True
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        return budget.consumed >= budget.total_budget


from __future__ import annotations

from datetime import datetime, timedelta

from src.core.base.lifecycle.version import VERSION

from .error_budget import ErrorBudget

__version__ = VERSION


class ErrorBudgetManager:
    Manages error budgets for SLO tracking.

    Tracks error budget consumption over time periods
    to support SLO management.

    Attributes:
        budgets: Map of budget names to ErrorBudget objects.
    

    def __init__(self) -> None:
        Initialize the error budget manager.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.budgets: dict[str, ErrorBudget] = {}

    def create_budget(self, name: str, total: float, period_days: int = 30) -> ErrorBudget:
        Create an error budget.

        Args:
            name: Budget name.
            total: Total budget amount.
            period_days: Budget period in days.

        Returns:
            The created ErrorBudget.
        
        now = datetime.now()
        end = now + timedelta(days=period_days)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         budget = ErrorBudget(
            budget_name=name,
            total_budget=total,
            period_start=now.isoformat(),
            period_end=end.isoformat(),
        )
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self.budgets[name] = budget
        return budget

    def consume(self, name: str, amount: float) -> bool:
        Consume error budget.

        Args:
            name: Budget name.
            amount: Amount to consume.

        Returns:
            True if budget was consumed, False if exceeded.
        
        if name not in self.budgets:
            return False
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        if budget.consumed + amount > budget.total_budget:
            return False
        budget.consumed += amount
        return True

    def get_remaining(self, name: str) -> float:
        Get remaining budget.

        Args:
            name: Budget name.

        Returns:
            Remaining budget amount.
        
        if name not in self.budgets:
            return 0.0
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        return budget.total_budget - budget.consumed

    def get_consumption_rate(self, name: str) -> float:
        Get budget consumption rate as percentage.
        if name not in self.budgets:
            return 0.0
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        if budget.total_budget == 0:
            return 100.0
        return (budget.consumed / budget.total_budget) * 100

    def is_exceeded(self, name: str) -> bool:
        Check if budget is exceeded.
        if name not in self.budgets:
            return True
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         budget = self.budgets[name]
        return budget.consumed >= budget.total_budget
