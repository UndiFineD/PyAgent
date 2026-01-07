#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

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

@dataclass
class ErrorBudget:
    """Error budget tracking for SLO management.

    Attributes:
        budget_name: Name of the error budget.
        total_budget: Total allowed error budget.
        consumed: Amount of budget consumed.
        period_start: Start of the budget period.
        period_end: End of the budget period.
    """
    budget_name: str
    total_budget: float
    consumed: float = 0.0
    period_start: str = ""
    period_end: str = ""
