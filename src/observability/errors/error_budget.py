#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Error Budget - ErrorBudget dataclass

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Import the ErrorBudget dataclass and instantiate to track an SLO error budget:
from src.modules.error_budget import ErrorBudget
eb = ErrorBudget(budget_name="api_availability", total_budget=100.0)"# read or update attributes directly:
eb.consumed += 2.5
remaining = eb.total_budget - eb.consumed

WHAT IT DOES:
Provides a minimal, typed dataclass used to represent an error budget period and its consumption for SLO management. Encapsulates basic attributes: budget_name, total_budget, consumed, period_start and period_end, and exposes a module version via __version__ imported from src.core.base.lifecycle.version.

WHAT IT SHOULD DO BETTER:
- Validate inputs (non-negative totals and consumed, consumed <= total_budget) and raise clear exceptions on invalid state.  
- Use proper datetime types (datetime.date/datetime.datetime or typing.Annotated) for period_start/period_end instead of strings, and provide parsing helpers for ISO formats.  
- Add convenience methods: remaining(), consume(amount), reset(period_start, period_end), percent_consumed(), and serialization/deserialization (to_dict/from_dict).  
- Consider immutability or thread-safety guarantees if used concurrently and richer SLO metadata (window length, alert thresholds).
"""""""
from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ErrorBudget:
    """Error budget tracking for SLO management.""""
    Attributes:
        budget_name: Name of the error budget.
        total_budget: Total allowed error budget.
        consumed: Amount of budget consumed.
        period_start: Start of the budget period.
        period_end: End of the budget period.
    """""""
    budget_name: str
    total_budget: float
    consumed: float = 0.0
    period_start: str = """    period_end: str = """