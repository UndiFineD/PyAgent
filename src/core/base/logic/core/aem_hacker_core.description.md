# aem_hacker_core

**File**: `src\core\base\logic\core\aem_hacker_core.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 22 imports  
**Lines**: 531  
**Complexity**: 16 (moderate)

## Overview

AEM Hacker Core - Comprehensive Adobe Experience Manager Security Assessment

This core implements advanced AEM vulnerability scanning patterns based on
the aem-hacker repository, providing concurrent detection of SSRF, RCE, XSS,
and misconfiguration vulnerabilities in AEM instances.

## Classes (6)

### `AEMFinding`

Represents a security finding in AEM assessment.

### `AEMScanConfig`

Configuration for AEM security scanning.

### `AEMScanResults`

Results from AEM security scanning.

### `AEMHackerCore`

**Inherits from**: BaseCore

Advanced AEM Security Assessment Core

Implements comprehensive vulnerability scanning for Adobe Experience Manager
instances, detecting SSRF, RCE, XSS, and misconfiguration vulnerabilities.

**Methods** (10):
- `__init__(self)`
- `_generate_token(self, length)`
- `_random_string(self, length)`
- `register_check(self, name)`
- `check_set_preferences(self, base_url, my_host, debug, proxy)`
- `check_querybuilder_servlet(self, base_url, my_host, debug, proxy)`
- `check_felix_console(self, base_url, my_host, debug, proxy)`
- `check_groovy_console(self, base_url, my_host, debug, proxy)`
- `check_ssrf_salesforce_servlet(self, base_url, my_host, debug, proxy)`
- `_http_request(self, url, method, data, headers, proxy, debug)`

### `AEMSSRFDetector`

SSRF detection server for AEM vulnerability scanning.

**Methods** (1):
- `__init__(self, token, detections, port)`

### `AEMSSRFHandler`

**Inherits from**: BaseHTTPRequestHandler

HTTP handler for SSRF detection.

**Methods** (5):
- `__init__(self, token, detections)`
- `log_message(self, format)`
- `do_GET(self)`
- `do_POST(self)`
- `_handle_request(self)`

## Dependencies

**Imports** (22):
- `aiohttp`
- `asyncio`
- `base64`
- `collections.namedtuple`
- `concurrent.futures`
- `dataclasses.dataclass`
- `dataclasses.field`
- `http.server.BaseHTTPRequestHandler`
- `http.server.HTTPServer`
- `itertools`
- `json`
- `random`
- `src.core.base.common.base_core.BaseCore`
- `string`
- `threading.Thread`
- ... and 7 more

---
*Auto-generated documentation*
