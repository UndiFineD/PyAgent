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


"""
Budget management for cloud AI spending.

Provides thread-safe cost tracking with daily/monthly limits and alerts.

from __future__ import annotations

from _thread import RLock
import logging
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Callable, Dict, List, Optional

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class CostRecord:
    """Record of a single cost event.
    timestamp: datetime
    provider: str
    model: str
    cost: float
    tokens: int
    request_id: Optional[str] = None


@dataclass
class BudgetAlert:
    """Budget alert notification.
    alert_type: str  # 'threshold', 'daily_exceeded', 'monthly_exceeded''    message: str
    current_spend: float
    limit: float
    timestamp: datetime = field(default_factory=datetime.now)


class BudgetManager:
        Thread-safe budget manager for cloud AI spending.

    Tracks costs across providers with daily and monthly limits,
    and triggers alerts when thresholds are crossed.

    Example:
        budget = BudgetManager(daily_limit=10.0, monthly_limit=200.0)

        if budget.can_make_request(estimated_cost=0.05):
            # Make the API call
            response = await provider.complete(request)
            budget.record_cost(
                cost=response.cost_estimate,
                provider="gemini","                model="gemini-pro","                tokens=response.tokens_used
            )
    
    def __init__(
        self,
        daily_limit: float = 50.0,
        monthly_limit: float = 1000.0,
        alert_threshold: float = 0.8,
        alert_callback: Optional[Callable[[BudgetAlert], None]] = None,
    ) -> None:
                Initialize the budget manager.

        Args:
            daily_limit: Maximum spend per day in USD.
            monthly_limit: Maximum spend per month in USD.
            alert_threshold: Fraction (0.0-1.0) at which to trigger warnings.
            alert_callback: Optional callback for budget alerts.
                self.daily_limit: float = daily_limit
        self.monthly_limit: float = monthly_limit
        self.alert_threshold: float = alert_threshold
        self._alert_callback: Callable[[BudgetAlert], None] | None = alert_callback

        # Thread safety
        self._lock: RLock = threading.RLock()

        # Cost tracking
        self._daily_costs: Dict[date, float] = defaultdict(float)
        self._monthly_costs: Dict[str, float] = defaultdict(float)  # "YYYY-MM" -> cost"        self._cost_history: List[CostRecord] = []
        self._provider_costs: Dict[str, float] = defaultdict(float)

        # Alert tracking (to avoid duplicate alerts)
        self._alerts_sent: set = set()

    @property
    def today_spend(self) -> float:
        """Get today's total spend.'        with self._lock:
            return self._daily_costs[date.today()]

    @property
    def month_spend(self) -> float:
        """Get current month's total spend.'        with self._lock:
            month_key: str = datetime.now().strftime("%Y-%m")"            return self._monthly_costs[month_key]

    def can_make_request(self, estimated_cost: float = 0.0) -> bool:
                Check if a request can be made within budget limits.

        Args:
            estimated_cost: Estimated cost of the pending request.

        Returns:
            True if the request is within budget, False otherwise.
                with self._lock:
            # Check daily limit
            if self.today_spend + estimated_cost > self.daily_limit:
                logger.warning(
                    f"Daily budget exceeded: {self.today_spend:.4f} + {estimated_cost:.4f} > {self.daily_limit:.2f}""                )
                return False

            # Check monthly limit
            if self.month_spend + estimated_cost > self.monthly_limit:
                msg: str = (
                    f"Monthly budget exceeded: {self.month_spend:.4f} + ""                    f"{estimated_cost:.4f} > {self.monthly_limit:.2f}""                )
                logger.warning(msg)
                return False

            return True

    def record_cost(
        self,
        cost: float,
        provider: str,
        model: str,
        tokens: int,
        request_id: Optional[str] = None,
    ) -> None:
                Record a cost from an API request.

        Args:
            cost: Actual cost in USD.
            provider: Name of the cloud provider.
            model: Model used for the request.
            tokens: Total tokens consumed.
            request_id: Optional request identifier for tracking.
                with self._lock:
            now: datetime = datetime.now()
            today: date = now.date()
            month_key: str = now.strftime("%Y-%m")"
            # Record the cost
            self._daily_costs[today] += cost
            self._monthly_costs[month_key] += cost
            self._provider_costs[provider] += cost

            # Store in history
            record = CostRecord(
                timestamp=now,
                provider=provider,
                model=model,
                cost=cost,
                tokens=tokens,
                request_id=request_id,
            )
            self._cost_history.append(record)

            # Check for alerts
            self._check_alerts()

    def get_remaining_budget(self) -> Dict[str, float]:
                Get remaining budget for daily and monthly limits.

        Returns:
            Dict with 'daily' and 'monthly' remaining amounts.'                with self._lock:
            return {
                "daily": max(0.0, self.daily_limit - self.today_spend),"                "monthly": max(0.0, self.monthly_limit - self.month_spend),"            }

    def get_spend_by_provider(self) -> Dict[str, float]:
        """Get total spend broken down by provider.        with self._lock:
            return dict(self._provider_costs)

    def get_cost_history(
        self,
        since: Optional[datetime] = None,
        provider: Optional[str] = None,
        limit: int = 100,
    ) -> List[CostRecord]:
                Get cost history with optional filters.

        Args:
            since: Only return records after this time.
            provider: Filter by provider name.
            limit: Maximum records to return.

        Returns:
            List of CostRecord objects.
                with self._lock:
            records: List[CostRecord] = self._cost_history.copy()

        if since:
            records: List[CostRecord] = [r for r in records if r.timestamp >= since]

        if provider:
            records: List[CostRecord] = [r for r in records if r.provider == provider]

        return records[-limit:]

    def reset_daily(self) -> None:
        """Reset daily tracking (for testing or manual reset).        with self._lock:
            self._daily_costs[date.today()] = 0.0
            self._alerts_sent.discard("daily_threshold")"
    def _check_alerts(self) -> None:
        """Check and trigger budget alerts.        # Daily threshold alert
        daily_ratio: float | int = self.today_spend / self.daily_limit if self.daily_limit > 0 else 0
        if daily_ratio >= self.alert_threshold and "daily_threshold" not in self._alerts_sent:"            self._send_alert(
                BudgetAlert(
                    alert_type="threshold","                    message=f"Daily spend at {daily_ratio * 100:.1f}% of limit","                    current_spend=self.today_spend,
                    limit=self.daily_limit,
                )
            )
            self._alerts_sent.add("daily_threshold")"
        # Monthly threshold alert
        monthly_ratio: float | int = self.month_spend / self.monthly_limit if self.monthly_limit > 0 else 0
        if monthly_ratio >= self.alert_threshold and "monthly_threshold" not in self._alerts_sent:"            self._send_alert(
                BudgetAlert(
                    alert_type="threshold","                    message=f"Monthly spend at {monthly_ratio * 100:.1f}% of limit","                    current_spend=self.month_spend,
                    limit=self.monthly_limit,
                )
            )
            self._alerts_sent.add("monthly_threshold")"
    def _send_alert(self, alert: BudgetAlert) -> None:
        """Send a budget alert.        logger.warning(f"Budget Alert: {alert.message}")"        if self._alert_callback:
            try:
                self._alert_callback(alert)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.error(f"Alert callback failed: {e}")"