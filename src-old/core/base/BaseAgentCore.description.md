# BaseAgentCore

**File**: `src\core\base\BaseAgentCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 21 imports  
**Lines**: 166  
**Complexity**: 13 (moderate)

## Overview

BaseAgentCore - Pure logic and calculation methods for agent operations.

Modularized via the 'core_logic' subpackage to maintain <500 line limit.

## Classes (1)

### `BaseAgentCore`

**Inherits from**: ValidationCore, MetricsCore, FormattingCore, UtilsCore, EventCore

Pure logic core for agent operations (Rust-convertible).

Inherits from logic mixins to satisfy the 500-line modularization rule.

**Methods** (13):
- `__init__(self)`
- `fix_markdown_content(self, content)`
- `prepare_capability_payload(self, agent_name, capabilities)`
- `load_config_from_env(self)`
- `process_token_tracking(self, input_tokens, output_tokens, model)`
- `check_token_budget(self, current_usage, estimated_tokens, budget)`
- `get_cache_stats(self, cache)`
- `perform_health_check(self, backend_status, cache_len, plugins)`
- `collect_tools(self, agent)`
- `get_capabilities(self)`
- ... and 3 more methods

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `core_logic.EventCore`
- `core_logic.FormattingCore`
- `core_logic.MetricsCore`
- `core_logic.UtilsCore`
- `core_logic.ValidationCore`
- `inspect`
- `logging`
- `os`
- `rust_core`
- `src.core.base.models.AgentConfig`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.ConversationMessage`
- `src.core.base.models.EventType`
- `src.core.base.models.ResponseQuality`
- ... and 6 more

---
*Auto-generated documentation*
