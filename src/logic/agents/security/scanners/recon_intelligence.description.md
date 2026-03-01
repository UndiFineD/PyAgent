# recon_intelligence

**File**: `src\logic\agents\security\scanners\recon_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 416  
**Complexity**: 11 (moderate)

## Overview

Python module containing implementation for recon_intelligence.

## Classes (1)

### `ReconIntelligence`

Advanced reconnaissance intelligence module for assets, subdomains, and technical profiling.
Ported from BBTz and other recon tools.

**Methods** (11):
- `get_service_banner_signatures()`
- `get_secret_regex_patterns()`
- `get_git_repo_discovery_patterns()`
- `get_eviltree_sensitive_patterns()`
- `get_common_http_ports(scale)`
- `__init__(self, session)`
- `get_shodan_favicon_query(self, mmh3_hash)`
- `parse_csp_domains(self, csp_header)`
- `check_redos_local(self, regex)`
- `extract_js_words(self, js_content)`
- ... and 1 more methods

## Dependencies

**Imports** (14):
- `PIL.Image`
- `aiohttp`
- `asyncio`
- `base64`
- `hashlib`
- `io`
- `json`
- `mmh3`
- `re`
- `string`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
