"""Pytest fixtures for test_base_agent tests."""

import pytest
from typing import Any

# Add src to path

from tests.utils.LegacySupport import create_legacy_agent_wrapper
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
            mod = importlib.import_module("src.core.base.BaseAgent")
            importlib.reload(mod)
        except ImportError:
            # Fallback or handle error
            mod = importlib.import_module("src.core.base.BaseAgent")

        # Aggregate classes
        class_map = {
            "ABTest": "src.core.base.BaseManagers.OrchestrationManagers",
            "ARIAAttribute": "src.core.base.types.ARIAAttribute",
            "AccessibilityIssue": "src.core.base.types.AccessibilityIssue",
            "AccessibilityIssueType": "src.core.base.types.AccessibilityIssueType",
            "AccessibilityReport": "src.core.base.types.AccessibilityReport",
            "AccessibilitySeverity": "src.core.base.types.AccessibilitySeverity",
            "AgentCommandHandler": "src.core.base.AgentCommandHandler",
            "AgentComposer": "src.core.base.BaseManagers.OrchestrationManagers",
            "AgentConfig": "src.core.base.models.AgentModels",
            "AgentConversationHistory": "src.core.base.AgentHistory",
            "AgentCore": "src.core.base.AgentCore",
            "AgentDelegator": "src.core.base.AgentDelegator",
            "AgentEvent": "src.core.base.models.CoreEnums",
            "AgentExecutionState": "src.core.base.models.CoreEnums",
            "AgentFileManager": "src.core.base.utils.AgentFileManager",
            "AgentGitHandler": "src.core.base.utils.AgentGitHandler",
            "AgentHealthCheck": "src.core.base.models.AgentModels",
            "AgentIdentity": "src.core.base.core.IdentityCore",
            "AgentInterface": "src.core.base.BaseInterfaces",
            "AgentMetrics": "src.core.base.BaseManagers.AgentMetrics",
            "AgentParallel": "src.core.base.models.AgentModels",
            "AgentPipeline": "src.core.base.models.AgentModels",
            "AgentPluginBase": "src.core.base.AgentPluginBase",
            "AgentPluginConfig": "src.core.base.models.AgentModels",
            "AgentPriority": "src.core.base.models.CoreEnums",
            "AgentPriorityQueue": "src.core.base.utils.AgentPriorityQueue",
            "AgentRegistry": "src.core.base.AgentRegistry",
            "AgentRouter": "src.core.base.models.AgentModels",
            "AgentScratchpad": "src.core.base.AgentScratchpad",
            "AgentState": "src.core.base.models.CoreEnums",
            "AgentStateManager": "src.core.base.AgentStateManager",
            "AgentTemplate": "src.core.base.utils.AgentTemplate",
            "AgentType": "src.core.base.models.CoreEnums",
            "AgentUpdateManager": "src.core.base.AgentUpdateManager",
            "AgentVerifier": "src.core.base.AgentVerification",
            "ArchitectureMapper": "src.core.base.ArchitectureMapper",
            "AuthConfig": "src.core.base.models.BaseModels",
            "AuthCore": "src.core.base.core.AuthCore",
            "AuthManager": "src.core.base.BaseManagers.AuthManagers",
            "AuthMethod": "src.core.base.models.CoreEnums",
            "AuthProof": "src.core.base.core.AuthCore",
            "AuthenticationManager": "src.core.base.BaseManagers.AuthManagers",
            "AutonomyCore": "src.core.base.core.AutonomyCore",
            "BaseAgent": "src.core.base.BaseAgent",
            "BaseAgentCore": "src.core.base.BaseAgentCore",
            "BaseCore": "src.core.base.AgentCore",
            "BaseModule": "src.core.base.BaseModules",
            "BatchRequest": "src.core.base.models.CommunicationModels",
            "BatchResult": "src.core.base.models.CommunicationModels",
            "BinaryTransport": "src.core.base.ConnectivityCore",
            "CacheEntry": "src.core.base.models.BaseModels",
            "CachedResult": "src.core.base.models.CommunicationModels",
            "CascadeContext": "src.core.base.models.CommunicationModels",
            "ChangelogEntry": "src.core.base.types.ChangelogEntry",
            "CircuitBreaker": "src.core.base.CircuitBreaker",
            "CodeLanguage": "src.core.base.types.CodeLanguage",
            "CodeMetrics": "src.core.base.types.CodeMetrics",
            "CodeQualityReport": "src.core.base.AgentCore",
            "CodeSmell": "src.core.base.types.CodeSmell",
            "ColorContrastResult": "src.core.base.types.ColorContrastResult",
            "ComplianceCategory": "src.core.base.types.ComplianceCategory",
            "ComplianceResult": "src.core.base.types.ComplianceResult",
            "ComposedAgent": "src.core.base.models.AgentModels",
            "ConditionalExecutor": "src.core.base.utils.ConditionalExecutor",
            "ConfigFormat": "src.core.base.models.CoreEnums",
            "ConfigLoader": "src.core.base.ConfigLoader",
            "ConfigProfile": "src.core.base.models.BaseModels",
            "ConfigValidator": "src.core.base.AgentVerification",
            "ConfigurationError": "src.core.base.BaseExceptions",
            "ConnectivityManager": "src.core.base.ConnectivityManager",
            "ConsistencyIssue": "src.core.base.types.ConsistencyIssue",
            "ContextRecorderInterface": "src.core.base.BaseInterfaces",
            "ContextWindow": "src.core.base.models.CommunicationModels",
            "ConvergenceCore": "src.core.base.core.ConvergenceCore",
            "ConversationHistory": "src.core.base.models.CommunicationModels",
            "ConversationMessage": "src.core.base.models.CommunicationModels",
            "CoreInterface": "src.core.base.BaseInterfaces",
            "CycleInterrupt": "src.core.base.BaseExceptions",
            "DependencyGraph": "src.core.base.DependencyGraph",
            "DependencyNode": "src.core.base.types.DependencyNode",
            "DependencyType": "src.core.base.types.DependencyType",
            "DiffGenerator": "src.core.base.utils.DiffGenerator",
            "DiffOutputFormat": "src.core.base.models.CoreEnums",
            "DiffResult": "src.core.base.types.DiffResult",
            "DiffViewMode": "src.core.base.types.DiffViewMode",
            "EmergencyEventLog": "src.core.base.AgentStateManager",
            "EntryTemplate": "src.core.base.types.EntryTemplate",
            "EnvironmentSanitizer": "src.core.base.ShellExecutor",
            "ErrorMappingCore": "src.core.base.core.ErrorMappingCore",
            "EventManager": "src.core.base.BaseManagers.SystemManagers",
            "EventType": "src.core.base.models.CoreEnums",
            "ExecutionCondition": "src.core.base.models.BaseModels",
            "ExecutionProfile": "src.core.base.models.AgentModels",
            "ExecutionScheduler": "src.core.base.utils.ExecutionScheduler",
            "FeedFormat": "src.core.base.types.FeedFormat",
            "FileLock": "src.core.base.utils.FileLock",
            "FileLockManager": "src.core.base.utils.FileLockManager",
            "FilePriority": "src.core.base.models.CoreEnums",
            "FilePriorityConfig": "src.core.base.models.BaseModels",
            "FilePriorityManager": "src.core.base.BaseManagers.SystemManagers",
            "GracefulShutdown": "src.core.base.GracefulShutdown",
            "GroupingStrategy": "src.core.base.types.GroupingStrategy",
            "HealthCheckResult": "src.core.base.models.FleetModels",
            "HealthChecker": "src.core.base.BaseManagers.SystemManagers",
            "HealthStatus": "src.core.base.models.CoreEnums",
            "HeartbeatSignal": "src.core.base.ConnectivityCore",
            "IdentityCore": "src.core.base.core.IdentityCore",
            "IncrementalProcessor": "src.core.base.IncrementalProcessor",
            "IncrementalState": "src.core.base.models.FleetModels",
            "InfrastructureError": "src.core.base.BaseExceptions",
            "InputType": "src.core.base.models.CoreEnums",
            "LinkedReference": "src.core.base.types.LinkedReference",
            "LocalizationLanguage": "src.core.base.types.LocalizationLanguage",
            "LocalizedEntry": "src.core.base.types.LocalizedEntry",
            "LockType": "src.core.base.models.CoreEnums",
            "LogicCore": "src.core.base.AgentCore",
            "LogicError": "src.core.base.BaseExceptions",
            "MessageRole": "src.core.base.models.CoreEnums",
            "MigrationRule": "src.core.base.types.MigrationRule",
            "MigrationStatus": "src.core.base.types.MigrationStatus",
            "ModelConfig": "src.core.base.models.BaseModels",
            "ModelError": "src.core.base.BaseExceptions",
            "ModelSelector": "src.core.base.BaseManagers.OrchestrationManagers",
            "ModernizationSuggestion": "src.core.base.types.ModernizationSuggestion",
            "ModuleLoader": "src.core.base.ModuleLoader",
            "MonorepoEntry": "src.core.base.types.MonorepoEntry",
            "MultimodalBuilder": "src.core.base.models.CommunicationModels",
            "MultimodalInput": "src.core.base.models.CommunicationModels",
            "MultimodalProcessor": "src.core.base.BaseManagers.ProcessorManagers",
            "NeuralPruningEngine": "src.core.base.NeuralPruningEngine",
            "NotificationCore": "src.core.base.utils.NotificationCore",
            "NotificationManager": "src.core.base.utils.NotificationManager",
            "OptimizationSuggestion": "src.core.base.types.OptimizationSuggestion",
            "OptimizationType": "src.core.base.types.OptimizationType",
            "OrchestratorInterface": "src.core.base.BaseInterfaces",
            "ParallelProcessor": "src.core.base.utils.ParallelProcessor",
            "PluginManager": "src.core.base.BaseManagers.PluginManager",
            "PluginMetadata": "src.core.base.BaseManagers.PluginManager",
            "ProfileManager": "src.core.base.BaseManagers.SystemManagers",
            "ProfilingCategory": "src.core.base.types.ProfilingCategory",
            "ProfilingSuggestion": "src.core.base.types.ProfilingSuggestion",
            "PromptTemplate": "src.core.base.models.CommunicationModels",
            "PromptTemplateManager": "src.core.base.models.CommunicationModels",
            "PromptVersion": "src.core.base.models.CommunicationModels",
            "PromptVersionManager": "src.core.base.BaseManagers.PromptManagers",
            "PruningCore": "src.core.base.core.PruningCore",
            "PyAgentException": "src.core.base.BaseExceptions",
            "QualityScore": "src.core.base.types.QualityScore",
            "QualityScorer": "src.core.base.BaseManagers.OrchestrationManagers",
            "QuotaConfig": "src.core.base.BaseManagers.ResourceQuotaManager",
            "RateLimitConfig": "src.core.base.models.FleetModels",
            "RateLimitStrategy": "src.core.base.models.CoreEnums",
            "RateLimiter": "src.core.base.utils.RateLimiter",
            "RefactoringPattern": "src.core.base.types.RefactoringPattern",
            "ReleaseNote": "src.core.base.types.ReleaseNote",
            "RequestBatcher": "src.core.base.BaseManagers.BatchManagers",
            "ResilienceCore": "src.core.base.core.ResilienceCore",
            "ResourceQuotaManager": "src.core.base.BaseManagers.ResourceQuotaManager",
            "ResourceUsage": "src.core.base.BaseManagers.ResourceQuotaManager",
            "ResponseCache": "src.core.base.BaseManagers.SystemManagers",
            "ResponsePostProcessor": "src.core.base.models.CommunicationModels",
            "ResponseQuality": "src.core.base.models.CoreEnums",
            "ResultCache": "src.core.base.utils.ResultCache",
            "ReviewCategory": "src.core.base.types.ReviewCategory",
            "ReviewFinding": "src.core.base.types.ReviewFinding",
            "SandboxManager": "src.core.base.SandboxManager",
            "ScheduledExecution": "src.core.base.utils.ScheduledExecution",
            "SearchResult": "src.core.base.types.SearchResult",
            "SecurityError": "src.core.base.BaseExceptions",
            "SecurityIssueType": "src.core.base.types.SecurityIssueType",
            "SecurityVulnerability": "src.core.base.types.SecurityVulnerability",
            "SerializationConfig": "src.core.base.models.BaseModels",
            "SerializationFormat": "src.core.base.models.CoreEnums",
            "SerializationManager": "src.core.base.BaseManagers.ProcessorManagers",
            "ShardedKnowledgeCore": "src.core.base.ShardedKnowledgeCore",
            "ShellExecutor": "src.core.base.ShellExecutor",
            "ShutdownState": "src.core.base.models.FleetModels",
            "SpanContext": "src.core.base.models.CommunicationModels",
            "StatePersistence": "src.core.base.BaseManagers.SystemManagers",
            "StateTransaction": "src.core.base.AgentStateManager",
            "StyleRule": "src.core.base.types.StyleRule",
            "StyleRuleSeverity": "src.core.base.types.StyleRuleSeverity",
            "SynapticWeight": "src.core.base.core.PruningCore",
            "TelemetryCollector": "src.core.base.utils.TelemetryCollector",
            "TelemetrySpan": "src.core.base.models.CommunicationModels",
            "TemplateManager": "src.core.base.utils.TemplateManager",
            "TestGap": "src.core.base.types.TestGap",
            "TokenBudget": "src.core.base.models.FleetModels",
            "ValidationRule": "src.core.base.models.BaseModels",
            "ValidationRuleManager": "src.core.base.utils.ValidationRuleManager",
            "VersioningStrategy": "src.core.base.types.VersioningStrategy",
            "WCAGLevel": "src.core.base.types.WCAGLevel",
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
