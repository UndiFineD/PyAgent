# DataScienceAgent

**File**: `src\classes\specialized\DataScienceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Data Science Agent for PyAgent.
Specializes in data cleaning, exploratory data analysis (EDA), statistical modeling, and insights.

## Classes (1)

### `DataScienceAgent`

**Inherits from**: BaseAgent

Agent designed for data-driven insights and statistical analysis.

**Methods** (5):
- `__init__(self, file_path)`
- `analyze_dataset(self, data_path)`
- `run_statistical_test(self, group_a, group_b, test_type)`
- `build_forecast_model(self, time_series_data)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
