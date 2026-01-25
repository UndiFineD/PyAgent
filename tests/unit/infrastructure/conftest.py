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

import pytest
from tests.utils.agent_test_utils import agent_dir_on_path


@pytest.fixture(name="agent_backend_module")
def agent_backend_module():
    """Load the agent backend module with all subcomponents aggregated."""
    with agent_dir_on_path():
        import importlib

        # Load main execution engine
        main_mod = importlib.import_module(
            "src.infrastructure.compute.backend.execution_engine"
        )

        # Aggregate classes from other backend modules
        class_map = {
            "ABTestVariant": "src.infrastructure.compute.backend.ab_test_variant",
            "ABTester": "src.infrastructure.compute.backend.ab_tester",
            "AuditLogger": "src.infrastructure.compute.backend.audit_logger",
            "BackendHandlers": "src.infrastructure.compute.backend.runner_backends",
            "BatchRequest": "src.infrastructure.compute.backend.batch_request",
            "CachedResponse": "src.infrastructure.compute.backend.cached_response",
            "CapabilityDiscovery": "src.infrastructure.compute.backend.capability_discovery",
            "CircuitBreaker": "src.infrastructure.compute.backend.circuit_breaker",
            "CircuitState": "src.infrastructure.compute.backend.circuit_state",
            "ConfigHotReloader": "src.infrastructure.compute.backend.config_hot_reloader",
            "ConnectionPool": "src.infrastructure.compute.backend.connection_pool",
            "CopilotCliBackend": "src.infrastructure.compute.backend.llm_backends.copilot_cli_backend",
            "DiskCache": "src.infrastructure.compute.backend.disk_cache",
            "ExtractCodeTransformer": "src.infrastructure.compute.backend.extract_code_transformer",
            "ExtractJsonTransformer": "src.infrastructure.compute.backend.extract_json_transformer",
            "GitHubModelsBackend": "src.infrastructure.compute.backend.llm_backends.git_hub_models_backend",
            "LLMBackend": "src.infrastructure.compute.backend.llm_backends.llm_backend",
            "LLMClient": "src.infrastructure.compute.backend.llm_client",
            "LoadBalanceStrategy": "src.infrastructure.compute.backend.load_balance_strategy",
            "LoadBalancer": "src.infrastructure.compute.backend.load_balancer",
            "LocalContextRecorder": "src.infrastructure.compute.backend.local_context_recorder",
            "OllamaBackend": "src.infrastructure.compute.backend.llm_backends.ollama_backend",
            "PoolingCore": "src.infrastructure.compute.backend.core.pooling_core",
            "ProviderType": "src.infrastructure.compute.backend.provider_type",
            "QueuedRequest": "src.infrastructure.compute.backend.queued_request",
            "RecordedRequest": "src.infrastructure.compute.backend.recorded_request",
            "RequestBatcher": "src.infrastructure.compute.backend.request_batcher",
            "RequestCompressor": "src.infrastructure.compute.backend.request_compressor",
            "RequestContext": "src.infrastructure.compute.backend.request_context",
            "RequestDeduplicator": "src.infrastructure.compute.backend.request_deduplicator",
            "RequestPriority": "src.infrastructure.compute.backend.request_priority",
            "RequestQueue": "src.infrastructure.compute.backend.request_queue",
            "RequestRecorder": "src.infrastructure.compute.backend.request_recorder",
            "RequestSigner": "src.infrastructure.compute.backend.request_signer",
            "RequestThrottler": "src.infrastructure.compute.backend.request_throttler",
            "RequestTracer": "src.infrastructure.compute.backend.request_tracer",
            "ResponseTransform": "src.infrastructure.compute.backend.response_transform",
            "ResponseTransformerBase": "src.infrastructure.compute.backend.response_transformer_base",
            "SqlMetadataHandler": "src.infrastructure.compute.backend.sql_metadata_handler",
            "StripWhitespaceTransformer": "src.infrastructure.compute.backend.strip_whitespace_transformer",
            "SubagentCore": "src.infrastructure.compute.backend.subagent_core",
            "SubagentRunner": "src.infrastructure.compute.backend.subagent_runner",
            "SubagentStatus": "src.infrastructure.compute.backend.subagent_status",
            "SystemAnalytics": "src.infrastructure.compute.backend.system_analytics",
            "SystemCapability": "src.infrastructure.compute.backend.system_capability",
            "SystemConfig": "src.infrastructure.compute.backend.system_config",
            "SystemHealthMonitor": "src.infrastructure.compute.backend.system_health_monitor",
            "SystemHealthStatus": "src.infrastructure.compute.backend.system_health_status",
            "SystemResponse": "src.infrastructure.compute.backend.system_response",
            "SystemState": "src.infrastructure.compute.backend.system_state",
            "SystemVersion": "src.infrastructure.compute.backend.system_version",
            "TTLCache": "src.infrastructure.compute.backend.ttl_cache",
            "UsageQuota": "src.infrastructure.compute.backend.usage_quota",
            "UsageQuotaManager": "src.infrastructure.compute.backend.usage_quota_manager",
            "UsageRecord": "src.infrastructure.compute.backend.usage_record",
            "VersionNegotiator": "src.infrastructure.compute.backend.version_negotiator",
            "VllmBackend": "src.infrastructure.compute.backend.llm_backends.vllm_backend",
            "VllmNativeBackend": "src.infrastructure.compute.backend.llm_backends.vllm_native_backend",
            "VllmNativeEngine": "src.infrastructure.compute.backend.vllm_native_engine",
        }

        for cls_name, mod_path in class_map.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, cls_name):
                    setattr(main_mod, cls_name, getattr(sub_mod, cls_name))
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # Silently fail if optional modules are missing dependencies
                pass

        # Add legacy aliases
        aliases = {
            "BackendType": ("src.infrastructure.compute.backend.provider_type", "ProviderType"),
            "BackendState": ("src.infrastructure.compute.backend.system_state", "SystemState"),
        }
        for alias, (mod_path, real_name) in aliases.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, real_name):
                    setattr(main_mod, alias, getattr(sub_mod, real_name))
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass

        return main_mod
