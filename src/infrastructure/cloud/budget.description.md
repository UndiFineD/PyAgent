# budget

**File**: `src\infrastructure\cloud\budget.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 12 imports  
**Lines**: 261  
**Complexity**: 11 (moderate)

## Overview

Budget management for cloud AI spending.

Provides thread-safe cost tracking with daily/monthly limits and alerts.

## Classes (3)

### `CostRecord`

Record of a single cost event.

### `BudgetAlert`

Budget alert notification.

### `BudgetManager`

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
            provider="gemini",
            model="gemini-pro",
            tokens=response.tokens_used
        )

**Methods** (11):
- `__init__(self, daily_limit, monthly_limit, alert_threshold, alert_callback)`
- `today_spend(self)`
- `month_spend(self)`
- `can_make_request(self, estimated_cost)`
- `record_cost(self, cost, provider, model, tokens, request_id)`
- `get_remaining_budget(self)`
- `get_spend_by_provider(self)`
- `get_cost_history(self, since, provider, limit)`
- `reset_daily(self)`
- `_check_alerts(self)`
- ... and 1 more methods

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.date`
- `datetime.datetime`
- `logging`
- `threading`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
