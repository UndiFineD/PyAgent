# nuclei_template_engine

**File**: `src\core\base\logic\core\nuclei_template_engine.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 13 imports  
**Lines**: 425  
**Complexity**: 10 (moderate)

## Overview

Nuclei-style Vulnerability Template Engine

Inspired by Nuclei templates from .external/0day-templates repository.
Implements YAML-based vulnerability detection templates with DSL matchers.

## Classes (7)

### `TemplateInfo`

Template metadata

### `TemplateRequest`

HTTP request specification

### `MatcherCondition`

Matcher condition specification

### `TemplateHTTP`

HTTP template specification

### `NucleiTemplate`

Complete Nuclei template

### `ScanResult`

Result from template execution

### `NucleiTemplateEngine`

Nuclei-style vulnerability detection engine.

Based on patterns from .external/0day-templates repository.

**Methods** (10):
- `__init__(self)`
- `load_template_from_yaml(self, yaml_content)`
- `load_template_from_file(self, file_path)`
- `_build_url(self, base_url, path)`
- `_check_matchers(self, matchers, response, condition)`
- `_check_single_matcher(self, matcher, response)`
- `_check_dsl_matcher(self, dsl_expressions, response)`
- `_check_word_matcher(self, words, content)`
- `_check_regex_matcher(self, patterns, content)`
- `get_available_templates(self)`

## Dependencies

**Imports** (13):
- `asyncio`
- `dataclasses.dataclass`
- `logging`
- `pathlib.Path`
- `re`
- `requests`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`
- `urllib.parse.urlparse`
- `yaml`

---
*Auto-generated documentation*
