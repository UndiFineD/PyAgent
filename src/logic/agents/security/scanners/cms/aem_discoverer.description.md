# aem_discoverer

**File**: `src\logic\agents\security\scanners\cms\aem_discoverer.py`  
**Type**: Python Module  
**Summary**: 0 classes, 23 functions, 10 imports  
**Lines**: 491  
**Complexity**: 23 (complex)

## Overview

Python module containing implementation for aem_discoverer.

## Functions (23)

### `error(message)`

### `register(f)`

### `normalize_url(base_url, path)`

### `http_request(url, method, data, additional_headers, proxy)`

### `preflight(url, proxy)`

### `content_type(ct)`

### `by_login_page(base_url, debug, proxy)`

### `by_csrf_token(base_url, debug, proxy)`

### `by_geometrixx_page(base_url, debug, proxy)`

### `by_get_servlet(base_url, debug, proxy)`

## Dependencies

**Imports** (10):
- `argparse`
- `concurrent.futures`
- `datetime`
- `itertools`
- `json`
- `requests`
- `sys`
- `threading.Lock`
- `threading.Semaphore`
- `traceback`

---
*Auto-generated documentation*
