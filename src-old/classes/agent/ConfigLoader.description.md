# ConfigLoader

**File**: `src\classes\agent\ConfigLoader.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 178  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ConfigLoader`

Loads agent configuration from YAML / TOML / JSON files.

Supports multiple configuration file formats and provides
validation and merging of configuration options.

Attributes:
    config_path: Path to configuration file.
    format: Configuration file format.

**Methods** (5):
- `__init__(self, config_path)`
- `load(self)`
- `_parse_content(self, content)`
- `_build_config(self, data)`
- `find_config_file(repo_root)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.AgentConfig.AgentConfig`
- `src.core.base.models.AgentPluginConfig`
- `src.core.base.models.ConfigFormat`
- `src.core.base.models.RateLimitConfig`
- `src.core.base.version.VERSION`
- `toml`
- `tomllib`
- `typing.Any`
- `typing.Optional`
- `typing.cast`
- `yaml`

---
*Auto-generated documentation*
