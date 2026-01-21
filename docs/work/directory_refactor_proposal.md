# PyAgent Directory Refactor Proposal (Phase I)

## 1. Overview
The current codebase has grown to over 1,800 Python files. `src/infrastructure/` and `src/core/base/` have become particularly cluttered, hindering maintainability and discovery. This proposal outlines a tiered reorganization strategy.

## 2. Proposed Structure: `src/infrastructure/`

We propose grouping the existing 60+ subdirectories into functional tiers.

### Tier 1: Engine & Core Inference (`src/infrastructure/engine/`)
Consolidates the core LLM execution logic.
- `attention/` -> `engine/attention/`
- `decoding/` -> `engine/decoding/`
- `sampling/` -> `engine/sampling/`
- `logprobs/` -> `engine/logprobs/`
- `tokenization/` & `tokenizer/` -> `engine/tokenization/`
- `position/` -> `engine/position/`
- `structured_output/` -> `engine/structured/`
- `speculative_v2/` -> `engine/speculative/`

### Tier 2: Compute & Acceleration (`src/infrastructure/compute/`)
Hardware-specific and optimization layers.
- `cuda/`
- `quantization/`
- `compilation/`
- `tensorizer/`
- `lora/`
- `moe/`
- `ssm/`
- `backend/`

### Tier 3: Memory & Storage (`src/infrastructure/storage/`)
Data persistence and caching.
- `memory/`
- `cache/`
- `kv_transfer/`
- `serialization/`
- `db/` (if moved from root)

### Tier 4: Swarm & Scaling (`src/infrastructure/swarm/`)
Distributed computing and multi-agent orchestration.
- `fleet/`
- `distributed/`
- `parallel/`
- `network/`
- `worker/`
- `orchestration/` (infra side)
- `voyager/`

### Tier 5: Operational Services (`src/infrastructure/services/`)
IO, API, and system utilities.
- `logging/`
- `metrics/`
- `api/`
- `openai_api/`
- `docker/`
- `cloud/`
- `mediaio/`
- `sandbox/`
- `execution/`
- `resilience/`
- `plugins/`

## 3. Proposed Structure: `src/core/base/`

The current flat structure of 50+ files will be grouped:

- `registry/`: `agent_registry.py`, `architecture_mapper.py`, `module_loader.py`
- `state/`: `agent_state_manager.py`, `agent_history.py`, `agent_scratchpad.py`
- `lifecycle/`: `agent_core.py`, `base_agent.py`, `graceful_shutdown.py`, `agent_update_manager.py`
- `execution/`: `agent_command_handler.py`, `agent_delegator.py`, `shell_executor.py`
- `common/`: `base_defaults.py`, `base_exceptions.py`, `base_interfaces.py`, `base_utilities.py`

## 4. Implementation Plan
1. **Scripted Moves**: Utilize a Python script to move directories and track target locations.
2. **Import Updating**: Use `ripgrep` to identify and update all internal imports.
3. **Facade Creation**: Temporary `__init__.py` facades in old locations for backward compatibility during the transition.
4. **Test Verification**: Run the full 3,800+ test suite to ensure no regressions.

## 5. Next Steps
- [ ] Review and approve the tier groupings.
- [ ] Initialize the Tier 1 migration (Engine).
