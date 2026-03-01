# subdomain_permutation_core

**File**: `src\core\base\logic\core\subdomain_permutation_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 14 imports  
**Lines**: 358  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for subdomain_permutation_core.

## Classes (3)

### `PermutationResult`

Result of subdomain permutation generation.

### `PermutationConfig`

Configuration for permutation generation.

### `SubdomainPermutationCore`

**Inherits from**: BaseCore

Subdomain Permutation Core implementing intelligent wordlist generation.

Inspired by AlterX, this core provides:
- DSL-based pattern generation
- Automatic word enrichment from input domains
- Cluster bomb permutation algorithms
- Configurable payloads and patterns

**Methods** (12):
- `__init__(self, config)`
- `generate_permutations(self, domains)`
- `_parse_domain(self, domain)`
- `_enrich_payloads(self, inputs)`
- `_get_payloads(self)`
- `_generate_domain_permutations(self, input_data, patterns, payloads)`
- `_resolve_pattern(self, pattern, input_data)`
- `_extract_payload_vars(self, pattern)`
- `_cluster_bomb(self, payloads, variables)`
- `_apply_payloads(self, pattern, payload_combo)`
- ... and 2 more methods

## Dependencies

**Imports** (14):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `itertools`
- `re`
- `src.core.base.common.base_core.BaseCore`
- `tldextract`
- `typing.Any`
- `typing.Dict`
- `typing.Iterator`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
