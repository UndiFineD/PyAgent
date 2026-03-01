# data_processing_mixin

**File**: `src\core\base\mixins\data_processing_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 189  
**Complexity**: 5 (moderate)

## Overview

Data Processing Mixin for PyAgent.

Provides utilities for processing and converting raw data into human-readable formats,
inspired by ADSpider's data transformation patterns.

## Classes (1)

### `DataProcessingMixin`

Mixin providing data processing utilities for agents.

Includes functions for converting binary flags, timestamps, and other
raw data formats to human-readable representations.

**Methods** (5):
- `convert_user_account_control(self, uac_value)`
- `convert_filetime_to_datetime(self, filetime_value)`
- `convert_account_expires(self, expires_value)`
- `process_change_record(self, record)`
- `format_change_output(self, changes, format_type)`

## Dependencies

**Imports** (7):
- `datetime`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
