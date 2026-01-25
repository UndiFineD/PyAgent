#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
            mod = importlib.import_module("src.core.base.lifecycle.base_agent")
            importlib.reload(mod)
        except ImportError:
            # Fallback or handle error
            mod = importlib.import_module("src.core.base.lifecycle.base_agent")

        # Aggregate classes
        class_map = {
            "ABTest": "src.core.base.common.base_managers.OrchestrationManagers",
            "ARIAAttribute": "src.core.base.common.types.aria_attribute",
            "AccessibilityIssue": "src.core.base.common.types.accessibility_issue",
            "AccessibilityIssueType": "src.core.base.common.types.accessibility_issue_type",
            "AccessibilityReport": "src.core.base.common.types.accessibility_report",
            "AccessibilitySeverity": "src.core.base.common.types.accessibility_severity",
            "AgentCommandHandler": "src.core.base.execution.agent_command_handler",
            "AgentComposer": "src.core.base.common.base_managers.OrchestrationManagers",
            "AgentConfig": "src.core.base.common.models.agent_models",
            "AgentConversationHistory": "src.core.base.state.agent_history",
            "AgentCore": "src.core.base.lifecycle.agent_core",
            "AgentDelegator": "src.core.base.execution.agent_delegator",
            "AgentEvent": "src.core.base.common.models.core_enums",
            "AgentExecutionState": "src.core.base.common.models.core_enums",
            "AgentFileManager": "src.core.base.common.utils.agent_file_manager",
            "AgentGitHandler": "src.core.base.common.utils.agent_git_handler",
            "AgentHealthCheck": "src.core.base.common.models.agent_models",
            "AgentIdentity": "src.core.base.logic.core.identity_core",
            "AgentInterface": "src.core.base.common.base_interfaces",
            "AgentMetrics": "src.core.base.common.base_managers.AgentMetrics",
            "AgentParallel": "src.core.base.common.models.agent_models",
            "AgentPipeline": "src.core.base.common.models.agent_models",
            "AgentPluginBase": "src.core.base.logic.agent_plugin_base",
            "AgentPluginConfig": "src.core.base.common.models.agent_models",
            "AgentPriority": "src.core.base.common.models.core_enums",
            "AgentPriorityQueue": "src.core.base.common.utils.agent_priority_queue",
            "AgentRegistry": "src.core.base.registry.agent_registry",
            "AgentRouter": "src.core.base.common.models.agent_models",
            "AgentScratchpad": "src.core.base.state.agent_scratchpad",
            "AgentState": "src.core.base.common.models.core_enums",
            "AgentStateManager": "src.core.base.state.agent_state_manager",
            "AgentTemplate": "src.core.base.common.utils.agent_template",
            "AgentType": "src.core.base.common.models.core_enums",
            "AgentUpdateManager": "src.core.base.lifecycle.agent_update_manager",
            "AgentVerifier": "src.core.base.logic.agent_verification",
            "ArchitectureMapper": "src.core.base.registry.architecture_mapper",
            "AuthConfig": "src.core.base.common.models.base_models",
            "AuthCore": "src.core.base.logic.core.auth_core",
            "AuthManager": "src.core.base.common.base_managers.AuthManagers",
            "AuthMethod": "src.core.base.common.models.core_enums",
            "AuthProof": "src.core.base.logic.core.auth_core",
            "AuthenticationManager": "src.core.base.common.base_managers.AuthManagers",
            "AutonomyCore": "src.core.base.logic.core.autonomy_core",
            "BaseAgent": "src.core.base.lifecycle.base_agent",
            "BaseAgentCore": "src.core.base.lifecycle.base_agent_core",
            "BaseCore": "src.core.base.lifecycle.agent_core",
            "BaseModule": "src.core.base.common.base_modules",
            "BatchRequest": "src.core.base.common.models.communication_models",
            "BatchResult": "src.core.base.common.models.communication_models",
            "BinaryTransport": "src.core.base.logic.connectivity_core",
            "CacheEntry": "src.core.base.common.models.base_models",
            "CachedResult": "src.core.base.common.models.communication_models",
            "CascadeContext": "src.core.base.common.models.communication_models",
            "ChangelogEntry": "src.core.base.common.types.changelog_entry",
            "CircuitBreaker": "src.core.base.logic.circuit_breaker",
            "CodeLanguage": "src.core.base.common.types.code_language",
            "CodeMetrics": "src.core.base.common.types.code_metrics",
            "CodeQualityReport": "src.core.base.lifecycle.agent_core",
            "CodeSmell": "src.core.base.common.types.code_smell",
            "ColorContrastResult": "src.core.base.common.types.color_contrast_result",
            "ComplianceCategory": "src.core.base.common.types.compliance_category",
            "ComplianceResult": "src.core.base.common.types.compliance_result",
            "ComposedAgent": "src.core.base.common.models.agent_models",
            "ConditionalExecutor": "src.core.base.common.utils.conditional_executor",
            "ConfigFormat": "src.core.base.common.models.core_enums",
            "ConfigLoader": "src.core.base.common.config_loader",
            "ConfigProfile": "src.core.base.common.models.base_models",
            "ConfigValidator": "src.core.base.logic.agent_verification",
            "ConfigurationError": "src.core.base.common.base_exceptions",
            "ConnectivityManager": "src.core.base.logic.connectivity_manager",
            "ConsistencyIssue": "src.core.base.common.types.consistency_issue",
            "ContextRecorderInterface": "src.core.base.common.base_interfaces",
            "ContextWindow": "src.core.base.common.models.communication_models",
            "ConvergenceCore": "src.core.base.logic.core.convergence_core",
            "ConversationHistory": "src.core.base.common.models.communication_models",
            "ConversationMessage": "src.core.base.common.models.communication_models",
            "CoreInterface": "src.core.base.common.base_interfaces",
            "CycleInterrupt": "src.core.base.common.base_exceptions",
            "DependencyGraph": "src.core.base.logic.dependency_graph",
            "DependencyNode": "src.core.base.common.types.dependency_node",
            "DependencyType": "src.core.base.common.types.dependency_type",
            "DiffGenerator": "src.core.base.common.utils.diff_generator",
            "DiffOutputFormat": "src.core.base.common.models.core_enums",
            "DiffResult": "src.core.base.common.types.diff_result",
            "DiffViewMode": "src.core.base.common.types.diff_view_mode",
            "EmergencyEventLog": "src.core.base.state.agent_state_manager",
            "EntryTemplate": "src.core.base.common.types.entry_template",
            "EnvironmentSanitizer": "src.core.base.execution.shell_executor",
            "ErrorMappingCore": "src.core.base.logic.core.error_mapping_core",
            "EventManager": "src.core.base.common.base_managers.SystemManagers",
            "EventType": "src.core.base.common.models.core_enums",
            "ExecutionCondition": "src.core.base.common.models.base_models",
            "ExecutionProfile": "src.core.base.common.models.agent_models",
            "ExecutionScheduler": "src.core.base.common.utils.execution_scheduler",
            "FeedFormat": "src.core.base.common.types.feed_format",
            "FileLock": "src.core.base.common.utils.file_lock",
            "FileLockManager": "src.core.base.common.utils.file_lock_manager",
            "FilePriority": "src.core.base.common.models.core_enums",
            "FilePriorityConfig": "src.core.base.common.models.base_models",
            "FilePriorityManager": "src.core.base.common.base_managers.SystemManagers",
            "GracefulShutdown": "src.core.base.lifecycle.graceful_shutdown",
            "GroupingStrategy": "src.core.base.common.types.grouping_strategy",
            "HealthCheckResult": "src.core.base.common.models.fleet_models",
            "HealthChecker": "src.core.base.common.base_managers.SystemManagers",
            "HealthStatus": "src.core.base.common.models.core_enums",
            "HeartbeatSignal": "src.core.base.logic.connectivity_core",
            "IdentityCore": "src.core.base.logic.core.identity_core",
            "IncrementalProcessor": "src.core.base.logic.incremental_processor",
            "IncrementalState": "src.core.base.common.models.fleet_models",
            "InfrastructureError": "src.core.base.common.base_exceptions",
            "InputType": "src.core.base.common.models.core_enums",
            "LinkedReference": "src.core.base.common.types.linked_reference",
            "LocalizationLanguage": "src.core.base.common.types.localization_language",
            "LocalizedEntry": "src.core.base.common.types.localized_entry",
            "LockType": "src.core.base.common.models.core_enums",
            "LogicCore": "src.core.base.lifecycle.agent_core",
            "LogicError": "src.core.base.common.base_exceptions",
            "MessageRole": "src.core.base.common.models.core_enums",
            "MigrationRule": "src.core.base.common.types.migration_rule",
            "MigrationStatus": "src.core.base.common.types.migration_status",
            "ModelConfig": "src.core.base.common.models.base_models",
            "ModelError": "src.core.base.common.base_exceptions",
            "ModelSelector": "src.core.base.common.base_managers.OrchestrationManagers",
            "ModernizationSuggestion": "src.core.base.common.types.modernization_suggestion",
            "ModuleLoader": "src.core.base.registry.module_loader",
            "MonorepoEntry": "src.core.base.common.types.monorepo_entry",
            "MultimodalBuilder": "src.core.base.common.models.communication_models",
            "MultimodalInput": "src.core.base.common.models.communication_models",
            "MultimodalProcessor": "src.core.base.common.base_managers.ProcessorManagers",
            "NeuralPruningEngine": "src.core.base.logic.neural_pruning_engine",
            "NotificationCore": "src.core.base.common.utils.notification_core",
            "NotificationManager": "src.core.base.common.utils.notification_manager",
            "OptimizationSuggestion": "src.core.base.common.types.optimization_suggestion",
            "OptimizationType": "src.core.base.common.types.optimization_type",
            "OrchestratorInterface": "src.core.base.common.base_interfaces",
            "ParallelProcessor": "src.core.base.common.utils.parallel_processor",
            "PluginManager": "src.core.base.common.base_managers.PluginManager",
            "PluginMetadata": "src.core.base.common.base_managers.PluginManager",
            "ProfileManager": "src.core.base.common.base_managers.SystemManagers",
            "ProfilingCategory": "src.core.base.common.types.profiling_category",
            "ProfilingSuggestion": "src.core.base.common.types.profiling_suggestion",
            "PromptTemplate": "src.core.base.common.models.communication_models",
            "PromptTemplateManager": "src.core.base.common.models.communication_models",
            "PromptVersion": "src.core.base.common.models.communication_models",
            "PromptVersionManager": "src.core.base.common.base_managers.PromptManagers",
            "PruningCore": "src.core.base.logic.core.pruning_core",
            "PyAgentException": "src.core.base.common.base_exceptions",
            "QualityScore": "src.core.base.common.types.quality_score",
            "QualityScorer": "src.core.base.common.base_managers.OrchestrationManagers",
            "QuotaConfig": "src.core.base.common.base_managers.ResourceQuotaManager",
            "RateLimitConfig": "src.core.base.common.models.fleet_models",
            "RateLimitStrategy": "src.core.base.common.models.core_enums",
            "RateLimiter": "src.core.base.common.utils.rate_limiter",
            "RefactoringPattern": "src.core.base.common.types.refactoring_pattern",
            "ReleaseNote": "src.core.base.common.types.release_note",
            "RequestBatcher": "src.core.base.common.base_managers.BatchManagers",
            "ResilienceCore": "src.core.base.logic.core.resilience_core",
            "ResourceQuotaManager": "src.core.base.common.base_managers.ResourceQuotaManager",
            "ResourceUsage": "src.core.base.common.base_managers.ResourceQuotaManager",
            "ResponseCache": "src.core.base.common.base_managers.SystemManagers",
            "ResponsePostProcessor": "src.core.base.common.models.communication_models",
            "ResponseQuality": "src.core.base.common.models.core_enums",
            "ResultCache": "src.core.base.common.utils.result_cache",
            "ReviewCategory": "src.core.base.common.types.review_category",
            "ReviewFinding": "src.core.base.common.types.review_finding",
            "SandboxManager": "src.core.base.logic.sandbox_manager",
            "ScheduledExecution": "src.core.base.common.utils.scheduled_execution",
            "SearchResult": "src.core.base.common.types.search_result",
            "SecurityError": "src.core.base.common.base_exceptions",
            "SecurityIssueType": "src.core.base.common.types.security_issue_type",
            "SecurityVulnerability": "src.core.base.common.types.security_vulnerability",
            "SerializationConfig": "src.core.base.common.models.base_models",
            "SerializationFormat": "src.core.base.common.models.core_enums",
            "SerializationManager": "src.core.base.common.base_managers.ProcessorManagers",
            "ShardedKnowledgeCore": "src.core.base.logic.sharded_knowledge_core",
            "ShellExecutor": "src.core.base.execution.shell_executor",
            "ShutdownState": "src.core.base.common.models.fleet_models",
            "SpanContext": "src.core.base.common.models.communication_models",
            "StatePersistence": "src.core.base.common.base_managers.SystemManagers",
            "StateTransaction": "src.core.base.state.agent_state_manager",
            "StyleRule": "src.core.base.common.types.style_rule",
            "StyleRuleSeverity": "src.core.base.common.types.style_rule_severity",
            "SynapticWeight": "src.core.base.logic.core.pruning_core",
            "TelemetryCollector": "src.core.base.common.utils.telemetry_collector",
            "TelemetrySpan": "src.core.base.common.models.communication_models",
            "TemplateManager": "src.core.base.common.utils.template_manager",
            "TestGap": "src.core.base.common.types.test_gap",
            "TokenBudget": "src.core.base.common.models.fleet_models",
            "ValidationRule": "src.core.base.common.models.base_models",
            "ValidationRuleManager": "src.core.base.common.utils.validation_rule_manager",
            "VersioningStrategy": "src.core.base.common.types.versioning_strategy",
            "WCAGLevel": "src.core.base.common.types.wcag_level",
        }

        for cls_name, mod_path in class_map.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, cls_name):
                    setattr(mod, cls_name, getattr(sub_mod, cls_name))
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
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
