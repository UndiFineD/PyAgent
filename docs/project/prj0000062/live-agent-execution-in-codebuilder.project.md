# live-agent-execution-in-codebuilder

**Project ID:** `prj0000062`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

_No checkbox tasks found in the plan file._

## Status

0 of 0 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\agents\byzantine.rs`
  - `rust_core\src\agents\pruning.rs`
  - `rust_core\src\agents.rs`
  - `rust_core\src\base\error_mapping.rs`
  - `rust_core\src\base\logging.rs`
  - `rust_core\src\base\pruning.rs`
  - `rust_core\src\inference\engine.rs`
  - `rust_core\src\inference\hashing.rs`
  - `rust_core\src\inference\input.rs`
  - `rust_core\src\inference\pooling.rs`
  - `rust_core\src\inference\sampling\filtering.rs`
  - `rust_core\src\inference\sampling.rs`
  - `rust_core\src\inference.rs`
  - `rust_core\src\multimodal\container.rs`
  - `rust_core\src\multimodal\image\processing.rs`
  - `rust_core\src\neural\clustering.rs`
  - `rust_core\src\neural\inference_utils.rs`
  - `rust_core\src\quantlora\sampling.rs`
  - `rust_core\src\scheduling.rs`
  - `rust_core\src\security\injection.rs`
  - `rust_core\src\stats\profiling.rs`
  - `rust_core\src\stats\tracing.rs`
  - `rust_core\src\text\matching.rs`
  - `rust_core\src\text\processing.rs`
  - `rust_core\src\transport\peer\link.rs`
  - `scripts\AgentDocFrequency.py`
  - `scripts\fix_indentation.py`
  - `src\__init__.py`
  - `src\agents\__init__.py`
  - `src\agents\BaseAgent.py`
  - `src\chat\__init__.py`
  - `src\chat\streaming.py`
  - `src\context_manager\__init__.py`
  - `src\context_manager\window.py`
  - `src\core\__init__.py`
  - `src\core\agent_registry.py`
  - `src\core\agent_state_manager.py`
  - `src\core\audit\__init__.py`
  - `src\core\audit\AuditTrailMixin.py`
  - `src\core\base\__init__.py`
  - `src\core\fuzzing\__init__.py`
  - `src\core\fuzzing\FuzzEngineCore.py`
  - `src\core\memory\__init__.py`
  - `src\core\n8nbridge\__init__.py`
  - `src\core\n8nbridge\N8nBridgeMixin.py`
  - `src\core\providers\__init__.py`
  - `src\core\reasoning\__init__.py`
  - `src\core\reasoning\CortAgent.py`
  - `src\core\reasoning\EvaluationEngine.py`
  - `src\core\replay\__init__.py`
  - `src\core\replay\ReplayMixin.py`
  - `src\core\replay\ShadowExecutionCore.py`
  - `src\core\resilience\__init__.py`
  - `src\core\resilience\CircuitBreakerMixin.py`
  - `src\core\sandbox\__init__.py`
  - `src\core\sandbox\SandboxMixin.py`
  - `src\core\scaffold\__init__.py`
  - `src\core\universal\__init__.py`
  - `src\core\universal\UniversalAgentShell.py`
  - `src\core\universal\UniversalIntentRouter.py`
  - `src\core\workflow\engine.py`
  - `src\cort\__init__.py`
  - `src\importer\__init__.py`
  - `src\mcp\__init__.py`
  - `src\memory\__init__.py`
  - `src\multimodal\__init__.py`
  - `src\observability\stats\legacy_engine.py`
  - `src\observability\stats\metrics_engine.py`
  - `src\plugins\__init__.py`
  - `src\plugins\PluginManager.py`
  - `src\rl\__init__.py`
  - `src\roadmap\__init__.py`
  - `src\roadmap\innovation.py`
  - `src\runtime\__init__.py`
  - `src\runtime_py\__init__.py`
  - `src\security\__init__.py`
  - `src\security\models\__init__.py`
  - `src\security\rotation_checkpoint_service.py`
  - `src\skills_registry\__init__.py`
  - `src\speculation\__init__.py`
  - `src\swarm\__init__.py`
  - `src\swarm\agent_registry.py`
  - `src\tools\__init__.py`
  - `src\tools\__main__.py`
  - `src\tools\agent_plugins.py`
  - `src\tools\nginx.py`
  - `src\tools\plugin_loader.py`
  - `src\tools\pm\__init__.py`
  - `src\transactions\__init__.py`
  - `src\transport\__init__.py`
  - `tests\agents\__init__.py`
  - `tests\agents\test_agents.py`
  - `tests\agents\test_base_agent.py`
  - `tests\core\__init__.py`
  - `tests\docs\test_agent_workflow_policy_docs.py`
  - `tests\docs\test_copilot_instructions_governance.py`
  - `tests\fixtures\__init__.py`
  - `tests\observability\test_legacy_engine.py`
  - `tests\observability\test_metrics_engine.py`
  - `tests\security\__init__.py`
  - `tests\security\fixtures\__init__.py`
  - `tests\security\test_containment_cleanup.py`
  - `tests\security\test_rotation_checkpoint_service.py`
  - `tests\structure\test_architecture_naming.py`
  - `tests\structure\test_install_script.py`
  - `tests\test_agent_doc_frequency.py`
  - `tests\test_agent_memory.py`
  - `tests\test_agent_registry.py`
  - `tests\test_api_versioning.py`
  - `tests\test_AuditTrailMixin.py`
  - `tests\test_chat_streaming.py`
  - `tests\test_CircuitBreakerMixin.py`
  - `tests\test_consolidate_llm_context_docstrings.py`
  - `tests\test_consolidate_llm_context_integration.py`
  - `tests\test_context_window.py`
  - `tests\test_core_agent_registry.py`
  - `tests\test_core_agent_state_manager.py`
  - `tests\test_core_workflow_engine.py`
  - `tests\test_FuzzEngineCore.py`
  - `tests\test_fuzzing_core.py`
  - `tests\test_innovation_tracker.py`
  - `tests\test_lint_config.py`
  - `tests\test_N8nBridgeMixin.py`
  - `tests\test_pipeline_execution.py`
  - `tests\test_plugin_marketplace.py`
  - `tests\test_plugins.py`
  - `tests\test_rate_limiting.py`
  - `tests\test_ReplayMixin.py`
  - `tests\test_rust_p2p_binary.py`
  - `tests\test_SandboxMixin.py`
  - `tests\test_ShadowExecutionCore.py`
  - `tests\test_structured_logging.py`
  - `tests\test_swarm_agent_registry.py`
  - `tests\test_system_integration.py`
  - `tests\test_tracing.py`
  - `tests\test_UniversalAgentShell.py`
  - `tests\test_UniversalIntentRouter.py`
  - `tests\test_workflow_engine.py`
  - `tests\tools\test_plugin_loader.py`
  - `tests\tools\test_self_healing.py`
  - `tests\unit\__init__.py`
  - `tests\unit\test_CortAgent.py`
  - `tests\unit\test_EvaluationEngine.py`
  - `tests\zzz\test_zza_lint_config.py`