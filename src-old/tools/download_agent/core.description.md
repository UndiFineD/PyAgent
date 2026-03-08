# core

**File**: `src\tools\download_agent\core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 350  
**Complexity**: 10 (moderate)

## Overview

Core download agent functionality.

## Classes (1)

### `DownloadAgent`

Main download agent that handles different URL types.

**Methods** (10):
- `__init__(self, config)`
- `ensure_directory(self, path)`
- `download_github_repo(self, url, metadata)`
- `download_github_gist(self, url, metadata)`
- `download_file(self, url, metadata, filename)`
- `download_arxiv_paper(self, url, metadata)`
- `open_webpage(self, url, metadata)`
- `process_url(self, url)`
- `process_urls_file(self)`
- `save_results(self, results, output_file)`

## Dependencies

**Imports** (14):
- `classifiers.URLClassifier`
- `datetime.datetime`
- `json`
- `models.DownloadConfig`
- `models.DownloadResult`
- `os`
- `pathlib.Path`
- `requests`
- `subprocess`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
