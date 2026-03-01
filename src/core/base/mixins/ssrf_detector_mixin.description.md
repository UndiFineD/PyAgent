# ssrf_detector_mixin

**File**: `src\core\base\mixins\ssrf_detector_mixin.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 11 imports  
**Lines**: 182  
**Complexity**: 16 (moderate)

## Overview

Python module containing implementation for ssrf_detector_mixin.

## Classes (2)

### `SSRFDetectorMixin`

Mixin providing SSRF detection capabilities using callback server pattern.

Inspired by aem-hacker's detector server for SSRF vulnerability detection.

**Methods** (10):
- `__init__(self)`
- `_generate_token(self)`
- `start_ssrf_detector(self, host, port)`
- `stop_ssrf_detector(self)`
- `get_ssrf_callback_url(self, host, port)`
- `check_ssrf_triggered(self, key, timeout)`
- `clear_ssrf_data(self)`
- `reset_ssrf_token(self)`
- `is_detector_running(self)`
- `get_ssrf_token(self)`

### `_DetectorHandler`

**Inherits from**: BaseHTTPRequestHandler

HTTP handler for SSRF detection callbacks.

**Methods** (6):
- `__init__(self, token, data_dict)`
- `log_message(self, format)`
- `do_GET(self)`
- `do_POST(self)`
- `do_PUT(self)`
- `_handle_request(self)`

## Dependencies

**Imports** (11):
- `asyncio`
- `http.server.BaseHTTPRequestHandler`
- `http.server.HTTPServer`
- `random`
- `string`
- `threading`
- `time`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
