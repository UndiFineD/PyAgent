# job_market_intelligence_core

**File**: `src\core\base\logic\core\job_market_intelligence_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 15 imports  
**Lines**: 488  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for job_market_intelligence_core.

## Classes (3)

### `JobPosting`

Represents a job posting with all relevant data

**Methods** (3):
- `__post_init__(self)`
- `age_days(self)`
- `salary_display(self)`

### `JobMarketStats`

Statistics about the job market

### `JobMarketIntelligenceCore`

**Inherits from**: BaseCore

Job Market Intelligence Core for automated job data collection and analysis.

Provides capabilities to collect, analyze, and present job market intelligence
including salary trends, company hiring patterns, and market insights.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (15):
- `asyncio`
- `csv`
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `datetime.datetime`
- `datetime.timedelta`
- `json`
- `re`
- `src.core.base.logic.core.base_core.BaseCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
