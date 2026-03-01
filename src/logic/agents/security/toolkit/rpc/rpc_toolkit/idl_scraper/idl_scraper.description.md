# idl_scraper

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\idl_scraper\idl_scraper.py`  
**Type**: Python Module  
**Summary**: 0 classes, 11 functions, 9 imports  
**Lines**: 184  
**Complexity**: 11 (moderate)

## Overview

Python module containing implementation for idl_scraper.

## Functions (11)

### `get_protocol_names()`

Fetch the list of protocol names from Microsoft's technical documents page.

### `get_toc_items_from_protocol_name(protocol_name)`

Fetch the table of contents JSON file for a specific protocol, and return its "items" list.
This is the first step towards getting the URLs for all relvant IDL files.

### `get_dicts_rec(array)`

Recursively yields all dicationary objects from the table of content JSON.
This is a helper function for get_idl_page_uuids_from_toc_items().

### `get_idl_page_uuids_from_toc_items(items)`

Fetch the UUIDs of the pages where IDL files are documented.
These are *not* the UUIDs of the interfaces! :) Just pages identifiers.

### `generate_urls_from_uuids(protocol_name, idl_uuids)`

### `get_idl_urls(protocol_name)`

### `get_idl_from_url(idl_url)`

### `download_protocol_idls(protocol_name, output)`

### `download_all_protocols_idls(output)`

### `get_args()`

## Dependencies

**Imports** (9):
- `argparse`
- `bs4.BeautifulSoup`
- `json`
- `logging`
- `os`
- `posixpath.join`
- `re`
- `requests`
- `tqdm.tqdm`

---
*Auto-generated documentation*
