import pytest
from tests.utils.agent_test_utils import agent_dir_on_path


@pytest.fixture(name="agent_backend_module")
def agent_backend_module():
    """Load the agent backend module with all subcomponents aggregated."""
    with agent_dir_on_path():
        import importlib

        # Load main execution engine
        main_mod = importlib.import_module(
            "src.infrastructure.backend.ExecutionEngine"
        )

        # Aggregate classes from other backend modules
        class_map = {
            "ABTestVariant": "src.infrastructure.backend.ABTestVariant",
            "ABTester": "src.infrastructure.backend.ABTester",
            "AuditLogger": "src.infrastructure.backend.AuditLogger",
            "BackendHandlers": "src.infrastructure.backend.RunnerBackends",
            "BatchRequest": "src.infrastructure.backend.BatchRequest",
            "CachedResponse": "src.infrastructure.backend.CachedResponse",
            "CapabilityDiscovery": "src.infrastructure.backend.CapabilityDiscovery",
            "CircuitBreaker": "src.infrastructure.backend.CircuitBreaker",
            "CircuitState": "src.infrastructure.backend.CircuitState",
            "ConfigHotReloader": "src.infrastructure.backend.ConfigHotReloader",
            "ConnectionPool": "src.infrastructure.backend.ConnectionPool",
            "CopilotCliBackend": "src.infrastructure.backend.llm_backends.CopilotCliBackend",
            "DiskCache": "src.infrastructure.backend.DiskCache",
            "ExtractCodeTransformer": "src.infrastructure.backend.ExtractCodeTransformer",
            "ExtractJsonTransformer": "src.infrastructure.backend.ExtractJsonTransformer",
            "GitHubModelsBackend": "src.infrastructure.backend.llm_backends.GitHubModelsBackend",
            "LLMBackend": "src.infrastructure.backend.llm_backends.LLMBackend",
            "LLMClient": "src.infrastructure.backend.LLMClient",
            "LoadBalanceStrategy": "src.infrastructure.backend.LoadBalanceStrategy",
            "LoadBalancer": "src.infrastructure.backend.LoadBalancer",
            "LocalContextRecorder": "src.infrastructure.backend.LocalContextRecorder",
            "OllamaBackend": "src.infrastructure.backend.llm_backends.OllamaBackend",
            "PoolingCore": "src.infrastructure.backend.core.PoolingCore",
            "ProviderType": "src.infrastructure.backend.ProviderType",
            "QueuedRequest": "src.infrastructure.backend.QueuedRequest",
            "RecordedRequest": "src.infrastructure.backend.RecordedRequest",
            "RequestBatcher": "src.infrastructure.backend.RequestBatcher",
            "RequestCompressor": "src.infrastructure.backend.RequestCompressor",
            "RequestContext": "src.infrastructure.backend.RequestContext",
            "RequestDeduplicator": "src.infrastructure.backend.RequestDeduplicator",
            "RequestPriority": "src.infrastructure.backend.RequestPriority",
            "RequestQueue": "src.infrastructure.backend.RequestQueue",
            "RequestRecorder": "src.infrastructure.backend.RequestRecorder",
            "RequestSigner": "src.infrastructure.backend.RequestSigner",
            "RequestThrottler": "src.infrastructure.backend.RequestThrottler",
            "RequestTracer": "src.infrastructure.backend.RequestTracer",
            "ResponseTransform": "src.infrastructure.backend.ResponseTransform",
            "ResponseTransformerBase": "src.infrastructure.backend.ResponseTransformerBase",
            "SqlMetadataHandler": "src.infrastructure.backend.SqlMetadataHandler",
            "StripWhitespaceTransformer": "src.infrastructure.backend.StripWhitespaceTransformer",
            "SubagentCore": "src.infrastructure.backend.SubagentCore",
            "SubagentRunner": "src.infrastructure.backend.SubagentRunner",
            "SubagentStatus": "src.infrastructure.backend.SubagentStatus",
            "SystemAnalytics": "src.infrastructure.backend.SystemAnalytics",
            "SystemCapability": "src.infrastructure.backend.SystemCapability",
            "SystemConfig": "src.infrastructure.backend.SystemConfig",
            "SystemHealthMonitor": "src.infrastructure.backend.SystemHealthMonitor",
            "SystemHealthStatus": "src.infrastructure.backend.SystemHealthStatus",
            "SystemResponse": "src.infrastructure.backend.SystemResponse",
            "SystemState": "src.infrastructure.backend.SystemState",
            "SystemVersion": "src.infrastructure.backend.SystemVersion",
            "TTLCache": "src.infrastructure.backend.TTLCache",
            "UsageQuota": "src.infrastructure.backend.UsageQuota",
            "UsageQuotaManager": "src.infrastructure.backend.UsageQuotaManager",
            "UsageRecord": "src.infrastructure.backend.UsageRecord",
            "VersionNegotiator": "src.infrastructure.backend.VersionNegotiator",
            "VllmBackend": "src.infrastructure.backend.llm_backends.VllmBackend",
            "VllmNativeBackend": "src.infrastructure.backend.llm_backends.VllmNativeBackend",
            "VllmNativeEngine": "src.infrastructure.backend.VllmNativeEngine",
        }

        for cls_name, mod_path in class_map.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, cls_name):
                    setattr(main_mod, cls_name, getattr(sub_mod, cls_name))
            except Exception:
                # Silently fail if optional modules are missing dependencies
                pass

        # Add legacy aliases
        aliases = {
            "BackendType": ("src.infrastructure.backend.ProviderType", "ProviderType"),
            "BackendState": ("src.infrastructure.backend.SystemState", "SystemState"),
        }
        for alias, (mod_path, real_name) in aliases.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, real_name):
                    setattr(main_mod, alias, getattr(sub_mod, real_name))
            except Exception:
                pass

        return main_mod
