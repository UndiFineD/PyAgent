# core-system

**Project ID:** `prj0000002`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] Define core system requirements and architecture in `brainstorm.md`.
- [x] Implement `Runtime` with deterministic scheduling and validation (`src/core/runtime.py`).
- [x] Implement `TaskQueue` with enqueue/dequeue and validation (`src/core/task_queue.py`).
- [x] Implement `AgentRegistry` with registration and lookup functionality (`src/core/agent_registry.py`).
- [x] Implement `MemoryStore` as an in-memory key/value store with `validate()` (`src/core/memory.py`).
- [x] Implement `emit_metric()` and related helpers in `src/core/observability.py`.
- [x] Add meta-tests that assert core modules are importable, validate without side effects, and avoid circular imports.
- [x] Ensure CI runs the core test suite via `ci.yml` and pre-commit.
- [x] Keep docs updated and in sync with the actual implementation.

## Status

9 of 9 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\utils\system.rs`
  - `src\agents\specialization\specialized_core_binding.py`
  - `src\core\audit\AuditTrailCore.py`
  - `src\core\fuzzing\FuzzEngineCore.py`
  - `src\core\memory\AutoMemCore.py`
  - `src\core\n8nbridge\N8nBridgeCore.py`
  - `src\core\reasoning\CortCore.py`
  - `src\core\replay\ShadowExecutionCore.py`
  - `src\core\resilience\CircuitBreakerCore.py`
  - `src\core\universal\UniversalCoreRegistry.py`
  - `tests\agents\specialization\test_specialized_core_binding.py`
  - `tests\core\test_core.py`
  - `tests\test_AuditTrailCore.py`
  - `tests\test_AutoMemCore.py`
  - `tests\test_backend_system_metrics.py`
  - `tests\test_CircuitBreakerCore.py`
  - `tests\test_core_agent_registry.py`
  - `tests\test_core_agent_state_manager.py`
  - `tests\test_core_base_mixins_audit_mixin.py`
  - `tests\test_core_base_mixins_base_behavior_mixin.py`
  - `tests\test_core_base_mixins_migration_observability.py`
  - `tests\test_core_base_mixins_replay_mixin.py`
  - `tests\test_core_base_mixins_sandbox_mixin.py`
  - `tests\test_core_base_mixins_shim_registry.py`
  - `tests\test_core_config.py`
  - `tests\test_core_helpers.py`
  - `tests\test_core_memory.py`
  - `tests\test_core_observability.py`
  - `tests\test_core_providers_FlmChatAdapter.py`
  - `tests\test_core_providers_FlmModelProbe.py`
  - `tests\test_core_providers_FlmProviderConfig.py`
  - `tests\test_core_quality.py`
  - `tests\test_core_routing_classifier_schema.py`
  - `tests\test_core_routing_confidence_calibration.py`
  - `tests\test_core_routing_fallback_reason_taxonomy.py`
  - `tests\test_core_routing_guardrail_policy_engine.py`
  - `tests\test_core_routing_policy_versioning.py`
  - `tests\test_core_routing_prompt_semantic_classifier.py`
  - `tests\test_core_routing_request_normalizer.py`
  - `tests\test_core_routing_routing_fallback_policy.py`
  - `tests\test_core_routing_routing_models.py`
  - `tests\test_core_routing_routing_policy_loader.py`
  - `tests\test_core_routing_shadow_mode_router.py`
  - `tests\test_core_runtime.py`
  - `tests\test_core_task_queue.py`
  - `tests\test_core_workflow_engine.py`
  - `tests\test_FuzzEngineCore.py`
  - `tests\test_fuzzing_core.py`
  - `tests\test_N8nBridgeCore.py`
  - `tests\test_rust_core.py`
  - `tests\test_ShadowExecutionCore.py`
  - `tests\test_system_integration.py`
  - `tests\test_theme_system.py`
  - `tests\test_UniversalCoreRegistry.py`
  - `tests\unit\test_CortCore.py`