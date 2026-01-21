import pytest
from tests.utils.agent_test_utils import agent_dir_on_path


@pytest.fixture(name="agent_backend_module")
def agent_backend_module():
    """Load the agent backend module with all subcomponents aggregated."""
    with agent_dir_on_path():
        import importlib

        # Load main execution engine
        main_mod = importlib.import_module(
            "src.infrastructure.backend.execution_engine"
        )

        # Aggregate classes from other backend modules
        class_map = {
            "ABTestVariant": "src.infrastructure.backend.ab_test_variant",
            "ABTester": "src.infrastructure.backend.ab_tester",
            "AuditLogger": "src.infrastructure.backend.audit_logger",
            "BackendHandlers": "src.infrastructure.backend.runner_backends",
            "BatchRequest": "src.infrastructure.backend.batch_request",
            "CachedResponse": "src.infrastructure.backend.cached_response",
            "CapabilityDiscovery": "src.infrastructure.backend.capability_discovery",
            "CircuitBreaker": "src.infrastructure.backend.circuit_breaker",
            "CircuitState": "src.infrastructure.backend.circuit_state",
            "ConfigHotReloader": "src.infrastructure.backend.config_hot_reloader",
            "ConnectionPool": "src.infrastructure.backend.connection_pool",
            "CopilotCliBackend": "src.infrastructure.backend.llm_backends.copilot_cli_backend",
            "DiskCache": "src.infrastructure.backend.disk_cache",
            "ExtractCodeTransformer": "src.infrastructure.backend.extract_code_transformer",
            "ExtractJsonTransformer": "src.infrastructure.backend.extract_json_transformer",
            "GitHubModelsBackend": "src.infrastructure.backend.llm_backends.git_hub_models_backend",
            "LLMBackend": "src.infrastructure.backend.llm_backends.llm_backend",
            "LLMClient": "src.infrastructure.backend.llm_client",
            "LoadBalanceStrategy": "src.infrastructure.backend.load_balance_strategy",
            "LoadBalancer": "src.infrastructure.backend.load_balancer",
            "LocalContextRecorder": "src.infrastructure.backend.local_context_recorder",
            "OllamaBackend": "src.infrastructure.backend.llm_backends.ollama_backend",
            "PoolingCore": "src.infrastructure.backend.core.pooling_core",
            "ProviderType": "src.infrastructure.backend.provider_type",
            "QueuedRequest": "src.infrastructure.backend.queued_request",
            "RecordedRequest": "src.infrastructure.backend.recorded_request",
            "RequestBatcher": "src.infrastructure.backend.request_batcher",
            "RequestCompressor": "src.infrastructure.backend.request_compressor",
            "RequestContext": "src.infrastructure.backend.request_context",
            "RequestDeduplicator": "src.infrastructure.backend.request_deduplicator",
            "RequestPriority": "src.infrastructure.backend.request_priority",
            "RequestQueue": "src.infrastructure.backend.request_queue",
            "RequestRecorder": "src.infrastructure.backend.request_recorder",
            "RequestSigner": "src.infrastructure.backend.request_signer",
            "RequestThrottler": "src.infrastructure.backend.request_throttler",
            "RequestTracer": "src.infrastructure.backend.request_tracer",
            "ResponseTransform": "src.infrastructure.backend.response_transform",
            "ResponseTransformerBase": "src.infrastructure.backend.response_transformer_base",
            "SqlMetadataHandler": "src.infrastructure.backend.sql_metadata_handler",
            "StripWhitespaceTransformer": "src.infrastructure.backend.strip_whitespace_transformer",
            "SubagentCore": "src.infrastructure.backend.subagent_core",
            "SubagentRunner": "src.infrastructure.backend.subagent_runner",
            "SubagentStatus": "src.infrastructure.backend.subagent_status",
            "SystemAnalytics": "src.infrastructure.backend.system_analytics",
            "SystemCapability": "src.infrastructure.backend.system_capability",
            "SystemConfig": "src.infrastructure.backend.system_config",
            "SystemHealthMonitor": "src.infrastructure.backend.system_health_monitor",
            "SystemHealthStatus": "src.infrastructure.backend.system_health_status",
            "SystemResponse": "src.infrastructure.backend.system_response",
            "SystemState": "src.infrastructure.backend.system_state",
            "SystemVersion": "src.infrastructure.backend.system_version",
            "TTLCache": "src.infrastructure.backend.ttl_cache",
            "UsageQuota": "src.infrastructure.backend.usage_quota",
            "UsageQuotaManager": "src.infrastructure.backend.usage_quota_manager",
            "UsageRecord": "src.infrastructure.backend.usage_record",
            "VersionNegotiator": "src.infrastructure.backend.version_negotiator",
            "VllmBackend": "src.infrastructure.backend.llm_backends.vllm_backend",
            "VllmNativeBackend": "src.infrastructure.backend.llm_backends.vllm_native_backend",
            "VllmNativeEngine": "src.infrastructure.backend.vllm_native_engine",
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
            "BackendType": ("src.infrastructure.backend.provider_type", "ProviderType"),
            "BackendState": ("src.infrastructure.backend.system_state", "SystemState"),
        }
        for alias, (mod_path, real_name) in aliases.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, real_name):
                    setattr(main_mod, alias, getattr(sub_mod, real_name))
            except Exception:
                pass

        return main_mod
