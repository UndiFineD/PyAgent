# reconnaissance_mixin

**File**: `src\core\base\mixins\reconnaissance_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 248  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for reconnaissance_mixin.

## Classes (1)

### `ReconnaissanceMixin`

Mixin providing reconnaissance capabilities for target discovery.

Inspired by aem_discoverer.py patterns for identifying vulnerable services.

**Methods** (6):
- `__init__(self)`
- `_load_default_patterns(self)`
- `_discover_single_target(self, base_url, patterns, timeout, proxy)`
- `_is_interesting_response(self, response)`
- `add_discovery_pattern(self, category, patterns)`
- `get_discovery_patterns(self, category)`

## Dependencies

**Imports** (10):
- `asyncio`
- `concurrent.futures`
- `re`
- `requests`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urljoin`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
