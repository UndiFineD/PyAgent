# FinancialAgent

**File**: `src\classes\specialized\FinancialAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 54  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in financial analysis and advice.

## Classes (1)

### `FinancialAgent`

**Inherits from**: BaseAgent

Agent for autonomous financial research and analysis (Dexter Pattern).

**Methods** (5):
- `__init__(self, file_path)`
- `plan_research(self, query)`
- `validate_sufficiency(self, data)`
- `analyze_market_trend(self, tickers)`
- `_get_default_content(self)`

## Dependencies

**Imports** (8):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
