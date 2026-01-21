"""Pytest fixtures for test_base_agent tests."""

import pytest
from typing import Any

# Add src to path

from tests.utils.legacy_support import create_legacy_agent_wrapper
from tests.utils.agent_test_utils import agent_dir_on_path


@pytest.fixture(autouse=True)
def disable_sessions(monkeypatch) -> None:
    """Disable sessions for all base_agent tests to ensure mocks work correctly."""
    monkeypatch.setenv("DV_AGENT_USE_SESSION", "false")


@pytest.fixture(name="base_agent_module")
def base_agent_module():
    with agent_dir_on_path():
        import importlib

        # Load BaseAgent
        try:
            mod = importlib.import_module("src.core.base.base_agent")
            importlib.reload(mod)
        except ImportError:
            # Fallback or handle error
            mod = importlib.import_module("src.core.base.base_agent")

        # Aggregate classes
        class_map = {
            "ABTest": "src.core.base.base_managers.OrchestrationManagers",
            "ARIAAttribute": "src.core.base.types.aria_attribute",
            "AccessibilityIssue": "src.core.base.types.accessibility_issue",
            "AccessibilityIssueType": "src.core.base.types.accessibility_issue_type",
            "AccessibilityReport": "src.core.base.types.accessibility_report",
            "AccessibilitySeverity": "src.core.base.types.accessibility_severity",
            "AgentCommandHandler": "src.core.base.agent_command_handler",
            "AgentComposer": "src.core.base.base_managers.OrchestrationManagers",
            "AgentConfig": "src.core.base.models.agent_models",
            "AgentConversationHistory": "src.core.base.agent_history",
            "AgentCore": "src.core.base.agent_core",
            "AgentDelegator": "src.core.base.agent_delegator",
            "AgentEvent": "src.core.base.models.core_enums",
            "AgentExecutionState": "src.core.base.models.core_enums",
            "AgentFileManager": "src.core.base.utils.agent_file_manager",
            "AgentGitHandler": "src.core.base.utils.agent_git_handler",
            "AgentHealthCheck": "src.core.base.models.agent_models",
            "AgentIdentity": "src.core.base.core.identity_core",
            "AgentInterface": "src.core.base.base_interfaces",
            "AgentMetrics": "src.core.base.base_managers.AgentMetrics",
            "AgentParallel": "src.core.base.models.agent_models",
            "AgentPipeline": "src.core.base.models.agent_models",
            "AgentPluginBase": "src.core.base.agent_plugin_base",
            "AgentPluginConfig": "src.core.base.models.agent_models",
            "AgentPriority": "src.core.base.models.core_enums",
            "AgentPriorityQueue": "src.core.base.utils.agent_priority_queue",
            "AgentRegistry": "src.core.base.agent_registry",
            "AgentRouter": "src.core.base.models.agent_models",
            "AgentScratchpad": "src.core.base.agent_scratchpad",
            "AgentState": "src.core.base.models.core_enums",
            "AgentStateManager": "src.core.base.agent_state_manager",
            "AgentTemplate": "src.core.base.utils.agent_template",
            "AgentType": "src.core.base.models.core_enums",
            "AgentUpdateManager": "src.core.base.agent_update_manager",
            "AgentVerifier": "src.core.base.agent_verification",
            "ArchitectureMapper": "src.core.base.architecture_mapper",
            "AuthConfig": "src.core.base.models.base_models",
            "AuthCore": "src.core.base.core.auth_core",
            "AuthManager": "src.core.base.base_managers.AuthManagers",
            "AuthMethod": "src.core.base.models.core_enums",
            "AuthProof": "src.core.base.core.auth_core",
            "AuthenticationManager": "src.core.base.base_managers.AuthManagers",
            "AutonomyCore": "src.core.base.core.autonomy_core",
            "BaseAgent": "src.core.base.base_agent",
            "BaseAgentCore": "src.core.base.base_agent_core",
            "BaseCore": "src.core.base.agent_core",
            "BaseModule": "src.core.base.base_modules",
            "BatchRequest": "src.core.base.models.communication_models",
            "BatchResult": "src.core.base.models.communication_models",
            "BinaryTransport": "src.core.base.connectivity_core",
            "CacheEntry": "src.core.base.models.base_models",
            "CachedResult": "src.core.base.models.communication_models",
            "CascadeContext": "src.core.base.models.communication_models",
            "ChangelogEntry": "src.core.base.types.changelog_entry",
            "CircuitBreaker": "src.core.base.circuit_breaker",
            "CodeLanguage": "src.core.base.types.code_language",
            "CodeMetrics": "src.core.base.types.code_metrics",
            "CodeQualityReport": "src.core.base.agent_core",
            "CodeSmell": "src.core.base.types.code_smell",
            "ColorContrastResult": "src.core.base.types.color_contrast_result",
            "ComplianceCategory": "src.core.base.types.compliance_category",
            "ComplianceResult": "src.core.base.types.compliance_result",
            "ComposedAgent": "src.core.base.models.agent_models",
            "ConditionalExecutor": "src.core.base.utils.conditional_executor",
            "ConfigFormat": "src.core.base.models.core_enums",
            "ConfigLoader": "src.core.base.config_loader",
            "ConfigProfile": "src.core.base.models.base_models",
            "ConfigValidator": "src.core.base.agent_verification",
            "ConfigurationError": "src.core.base.base_exceptions",
            "ConnectivityManager": "src.core.base.connectivity_manager",
            "ConsistencyIssue": "src.core.base.types.consistency_issue",
            "ContextRecorderInterface": "src.core.base.base_interfaces",
            "ContextWindow": "src.core.base.models.communication_models",
            "ConvergenceCore": "src.core.base.core.convergence_core",
            "ConversationHistory": "src.core.base.models.communication_models",
            "ConversationMessage": "src.core.base.models.communication_models",
            "CoreInterface": "src.core.base.base_interfaces",
            "CycleInterrupt": "src.core.base.base_exceptions",
            "DependencyGraph": "src.core.base.dependency_graph",
            "DependencyNode": "src.core.base.types.dependency_node",
            "DependencyType": "src.core.base.types.dependency_type",
            "DiffGenerator": "src.core.base.utils.diff_generator",
            "DiffOutputFormat": "src.core.base.models.core_enums",
            "DiffResult": "src.core.base.types.diff_result",
            "DiffViewMode": "src.core.base.types.diff_view_mode",
            "EmergencyEventLog": "src.core.base.agent_state_manager",
            "EntryTemplate": "src.core.base.types.entry_template",
            "EnvironmentSanitizer": "src.core.base.shell_executor",
            "ErrorMappingCore": "src.core.base.core.error_mapping_core",
            "EventManager": "src.core.base.base_managers.SystemManagers",
            "EventType": "src.core.base.models.core_enums",
            "ExecutionCondition": "src.core.base.models.base_models",
            "ExecutionProfile": "src.core.base.models.agent_models",
            "ExecutionScheduler": "src.core.base.utils.execution_scheduler",
            "FeedFormat": "src.core.base.types.feed_format",
            "FileLock": "src.core.base.utils.file_lock",
            "FileLockManager": "src.core.base.utils.file_lock_manager",
            "FilePriority": "src.core.base.models.core_enums",
            "FilePriorityConfig": "src.core.base.models.base_models",
            "FilePriorityManager": "src.core.base.base_managers.SystemManagers",
            "GracefulShutdown": "src.core.base.graceful_shutdown",
            "GroupingStrategy": "src.core.base.types.grouping_strategy",
            "HealthCheckResult": "src.core.base.models.fleet_models",
            "HealthChecker": "src.core.base.base_managers.SystemManagers",
            "HealthStatus": "src.core.base.models.core_enums",
            "HeartbeatSignal": "src.core.base.connectivity_core",
            "IdentityCore": "src.core.base.core.identity_core",
            "IncrementalProcessor": "src.core.base.incremental_processor",
            "IncrementalState": "src.core.base.models.fleet_models",
            "InfrastructureError": "src.core.base.base_exceptions",
            "InputType": "src.core.base.models.core_enums",
            "LinkedReference": "src.core.base.types.linked_reference",
            "LocalizationLanguage": "src.core.base.types.localization_language",
            "LocalizedEntry": "src.core.base.types.localized_entry",
            "LockType": "src.core.base.models.core_enums",
            "LogicCore": "src.core.base.agent_core",
            "LogicError": "src.core.base.base_exceptions",
            "MessageRole": "src.core.base.models.core_enums",
            "MigrationRule": "src.core.base.types.migration_rule",
            "MigrationStatus": "src.core.base.types.migration_status",
            "ModelConfig": "src.core.base.models.base_models",
            "ModelError": "src.core.base.base_exceptions",
            "ModelSelector": "src.core.base.base_managers.OrchestrationManagers",
            "ModernizationSuggestion": "src.core.base.types.modernization_suggestion",
            "ModuleLoader": "src.core.base.module_loader",
            "MonorepoEntry": "src.core.base.types.monorepo_entry",
            "MultimodalBuilder": "src.core.base.models.communication_models",
            "MultimodalInput": "src.core.base.models.communication_models",
            "MultimodalProcessor": "src.core.base.base_managers.ProcessorManagers",
            "NeuralPruningEngine": "src.core.base.neural_pruning_engine",
            "NotificationCore": "src.core.base.utils.notification_core",
            "NotificationManager": "src.core.base.utils.notification_manager",
            "OptimizationSuggestion": "src.core.base.types.optimization_suggestion",
            "OptimizationType": "src.core.base.types.optimization_type",
            "OrchestratorInterface": "src.core.base.base_interfaces",
            "ParallelProcessor": "src.core.base.utils.parallel_processor",
            "PluginManager": "src.core.base.base_managers.PluginManager",
            "PluginMetadata": "src.core.base.base_managers.PluginManager",
            "ProfileManager": "src.core.base.base_managers.SystemManagers",
            "ProfilingCategory": "src.core.base.types.profiling_category",
            "ProfilingSuggestion": "src.core.base.types.profiling_suggestion",
            "PromptTemplate": "src.core.base.models.communication_models",
            "PromptTemplateManager": "src.core.base.models.communication_models",
            "PromptVersion": "src.core.base.models.communication_models",
            "PromptVersionManager": "src.core.base.base_managers.PromptManagers",
            "PruningCore": "src.core.base.core.pruning_core",
            "PyAgentException": "src.core.base.base_exceptions",
            "QualityScore": "src.core.base.types.quality_score",
            "QualityScorer": "src.core.base.base_managers.OrchestrationManagers",
            "QuotaConfig": "src.core.base.base_managers.ResourceQuotaManager",
            "RateLimitConfig": "src.core.base.models.fleet_models",
            "RateLimitStrategy": "src.core.base.models.core_enums",
            "RateLimiter": "src.core.base.utils.rate_limiter",
            "RefactoringPattern": "src.core.base.types.refactoring_pattern",
            "ReleaseNote": "src.core.base.types.release_note",
            "RequestBatcher": "src.core.base.base_managers.BatchManagers",
            "ResilienceCore": "src.core.base.core.resilience_core",
            "ResourceQuotaManager": "src.core.base.base_managers.ResourceQuotaManager",
            "ResourceUsage": "src.core.base.base_managers.ResourceQuotaManager",
            "ResponseCache": "src.core.base.base_managers.SystemManagers",
            "ResponsePostProcessor": "src.core.base.models.communication_models",
            "ResponseQuality": "src.core.base.models.core_enums",
            "ResultCache": "src.core.base.utils.result_cache",
            "ReviewCategory": "src.core.base.types.review_category",
            "ReviewFinding": "src.core.base.types.review_finding",
            "SandboxManager": "src.core.base.sandbox_manager",
            "ScheduledExecution": "src.core.base.utils.scheduled_execution",
            "SearchResult": "src.core.base.types.search_result",
            "SecurityError": "src.core.base.base_exceptions",
            "SecurityIssueType": "src.core.base.types.security_issue_type",
            "SecurityVulnerability": "src.core.base.types.security_vulnerability",
            "SerializationConfig": "src.core.base.models.base_models",
            "SerializationFormat": "src.core.base.models.core_enums",
            "SerializationManager": "src.core.base.base_managers.ProcessorManagers",
            "ShardedKnowledgeCore": "src.core.base.sharded_knowledge_core",
            "ShellExecutor": "src.core.base.shell_executor",
            "ShutdownState": "src.core.base.models.fleet_models",
            "SpanContext": "src.core.base.models.communication_models",
            "StatePersistence": "src.core.base.base_managers.SystemManagers",
            "StateTransaction": "src.core.base.agent_state_manager",
            "StyleRule": "src.core.base.types.style_rule",
            "StyleRuleSeverity": "src.core.base.types.style_rule_severity",
            "SynapticWeight": "src.core.base.core.pruning_core",
            "TelemetryCollector": "src.core.base.utils.telemetry_collector",
            "TelemetrySpan": "src.core.base.models.communication_models",
            "TemplateManager": "src.core.base.utils.template_manager",
            "TestGap": "src.core.base.types.test_gap",
            "TokenBudget": "src.core.base.models.fleet_models",
            "ValidationRule": "src.core.base.models.base_models",
            "ValidationRuleManager": "src.core.base.utils.validation_rule_manager",
            "VersioningStrategy": "src.core.base.types.versioning_strategy",
            "WCAGLevel": "src.core.base.types.wcag_level",
        }

        for cls_name, mod_path in class_map.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, cls_name):
                    setattr(mod, cls_name, getattr(sub_mod, cls_name))
            except Exception:
                pass

        # Apply legacy wrapper
        if hasattr(mod, "BaseAgent"):
            wrapper = create_legacy_agent_wrapper(mod.BaseAgent)
            mod.BaseAgent = wrapper
            # Also alias Agent to wrapper if needed
            mod.Agent = wrapper

        return mod


@pytest.fixture
def base_agent(base_agent_module: Any) -> Any:
    """Create a BaseAgent instance for testing."""

    # BaseAgent might be abstract, so we might need a concrete implementation
    # or just use the class if it's not strictly abstract in a way that prevents instantiation.
    class ConcreteAgent(base_agent_module.BaseAgent):
        def _process_logic(self, content: str) -> str:
            return content

    return ConcreteAgent()
