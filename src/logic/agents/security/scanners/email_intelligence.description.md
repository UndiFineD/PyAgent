# email_intelligence

**File**: `src\logic\agents\security\scanners\email_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 97  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for email_intelligence.

## Classes (1)

### `EmailIntelligence`

Intelligence engine for handling ephemeral/temporary emails and OTP extraction.

**Methods** (3):
- `__init__(self, session)`
- `extract_otp(self, text)`
- `extract_links(self, text)`

## Dependencies

**Imports** (10):
- `aiohttp`
- `asyncio`
- `random`
- `re`
- `src.core.base.logic.logger.logger`
- `string`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
