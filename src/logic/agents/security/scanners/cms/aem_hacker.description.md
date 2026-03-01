# aem_hacker

**File**: `src\logic\agents\security\scanners\cms\aem_hacker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 39 functions, 17 imports  
**Lines**: 1676  
**Complexity**: 45 (complex)

## Overview

Python module containing implementation for aem_hacker.

## Classes (1)

### `Detector`

**Inherits from**: BaseHTTPRequestHandler

Class Detector implementation.

**Methods** (6):
- `__init__(self, token, d)`
- `log_message(self, format)`
- `do_GET(self)`
- `do_POST(self)`
- `do_PUT(self)`
- `serve(self)`

## Functions (39)

### `random_string(length)`

### `register(name)`

### `normalize_url(base_url, path)`

### `content_type(ct)`

### `error(message)`

### `http_request(url, method, data, additional_headers, proxy, debug)`

### `http_request_multipart(url, method, data, additional_headers, proxy, debug)`

### `preflight(url, proxy, debug)`

### `exposed_set_preferences(base_url, my_host, debug, proxy)`

### `exposed_merge_metadata(base_url, my_host, debug, proxy)`

## Dependencies

**Imports** (17):
- `argparse`
- `base64`
- `collections.namedtuple`
- `concurrent.futures`
- `datetime`
- `http.server.BaseHTTPRequestHandler`
- `http.server.HTTPServer`
- `itertools`
- `json`
- `random.choice`
- `random.randint`
- `requests`
- `string.ascii_letters`
- `sys`
- `threading.Thread`
- ... and 2 more

---
*Auto-generated documentation*
