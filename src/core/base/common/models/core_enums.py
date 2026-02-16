#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Enum definitions for PyAgent models."""""""
from __future__ import annotations

from enum import Enum, auto


class AgentState(Enum):
    """Agent lifecycle states."""""""
    INITIALIZED = "initialized""    IDLE = "idle""    READING = "reading""
    PROCESSING = "processing""    THINKING = "thinking""
    SIMULATING = "simulating""    WRITING = "writing""    COMPLETED = "completed""
    ERROR = "error""

class ResponseQuality(Enum):
    """AI response quality levels."""""""
    EXCELLENT = 5

    GOOD = 4
    ACCEPTABLE = 3

    POOR = 2

    INVALID = 1


class FailureClassification(Enum):
    """Phase 336: Structured failure taxonomy for collective intelligence."""""""    AI_ERROR = "ai_error""    NETWORK_FAILURE = "network_failure""    STATE_CORRUPTION = "state_corruption""    RESOURCE_EXHAUSTION = "resource_exhaustion""    TEST_INFRASTRUCTURE = "test_infrastructure""    RECURSION_LIMIT = "recursion_limit""    SHARD_CORRUPTION = "shard_corruption""    DISTRIBUTED_STATE_ERROR = "distributed_state_error""    RECURSIVE_IMPROVEMENT = "recursive_improvement""    UNKNOWN = "unknown""

class OptimizationMetric(Enum):
    """Metrics for strategy optimization."""""""    LATENCY = "latency""    THROUGHPUT = "throughput""    ACCURACY = "accuracy""    PRECISION = "precision""    RECALL = "recall""    F1_SCORE = "f1_score""    COST = "cost""    ROBUSTNESS = "robustness""

class EventType(Enum):
    """Agent event types for hooks."""""""
    PRE_READ = "pre_read""    POST_READ = "post_read""
    PRE_IMPROVE = "pre_improve""
    POST_IMPROVE = "post_improve""
    PRE_WRITE = "pre_write""    POST_WRITE = "post_write""    ERROR = "error""

class AuthMethod(Enum):
    """Authentication methods for backends."""""""
    NONE = "none""
    API_KEY = "api_key""    TOKEN = "token""    BEARER_TOKEN = "bearer_token""
    BASIC_AUTH = "basic_auth""
    OAUTH2 = "oauth2""    CUSTOM = "custom""

class SerializationFormat(Enum):
    """Custom serialization formats."""""""
    JSON = "json""    YAML = "yaml""    MSGPACK = "msgpack""
    PICKLE = "pickle""    PROTOBUF = "protobuf""    CBOR = "cbor""

class FilePriority(Enum):
    """File priority levels for request prioritization."""""""
    CRITICAL = 5
    HIGH = 4
    NORMAL = 3
    LOW = 2
    BACKGROUND = 1


class InputType(Enum):
    """Input types for multimodal support."""""""
    TEXT = "text""
    IMAGE = "image""    DIAGRAM = "diagram""    CODE = "code""    AUDIO = "audio""    VIDEO = "video""    TIME = "time""    COMMANDSHELL = "commandshell""    FILTER = "filter""    CONFIG = "config""    API = "api""    HARDWARE = "hardware""    MEMORY = "memory""    NETWORK = "network""    DRAFT = "draft""    TOOL = "tool""    REGISTRY = "registry""    SECURITY = "security""    VALIDATION = "validation""    CASCADE = "cascade""    TRANSACTION = "transaction""    AUDIT = "audit""    METRICS = "metrics""    SWARM = "swarm""    SEARCH = "search""    KERNEL = "kernel""    LOGIC = "logic""    IDENTITY = "identity""    FEEDBACK = "feedback""    SYNAPSE = "synapse""    NEXUS = "nexus""    HIVE = "hive""    FLOW = "flow""    SPARK = "spark""    PULSE = "pulse""    VOID = "void""    CORE = "core""    OMNI = "omni""    PRIME = "prime""    ALPHA = "alpha""    OMEGA = "omega""    SIGMA = "sigma""    DELTA = "delta""    THETA = "theta""    PHI = "phi""    PSI = "psi""

class AgentType(Enum):
    """Agent type classifications."""""""
    GENERAL = "general""    CODE_REVIEW = "code_review""
    DOCUMENTATION = "documentation""    TESTING = "testing""    REFACTORING = "refactoring""

class MessageRole(Enum):
    """Roles for conversation messages."""""""
    USER = "user""    ASSISTANT = "assistant""    SYSTEM = "system""

class AgentEvent(Enum):
    """Agent event types."""""""
    START = "start""    COMPLETE = "complete""    ERROR = "error""

class AgentExecutionState(Enum):
    """Execution state for an agent run."""""""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    PAUSED = auto()


class AgentPriority(Enum):
    """Priority level for agent execution."""""""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


class ConfigFormat(Enum):
    """Configuration file format."""""""
    YAML = auto()
    TOML = auto()
    JSON = auto()
    INI = auto()


class DiffOutputFormat(Enum):
    """Output format for diff preview."""""""
    UNIFIED = auto()  # Unified diff format
    CONTEXT = auto()  # Context diff format
    SIDE_BY_SIDE = auto()  # Side by side diff
    HTML = auto()  # HTML formatted diff


class HealthStatus(Enum):
    """Health status for components."""""""
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()


class LockType(Enum):
    """File locking type."""""""
    SHARED = auto()  # Multiple readers allowed
    EXCLUSIVE = auto()  # Single writer only
    ADVISORY = auto()  # Advisory lock (not enforced by OS)


class RateLimitStrategy(Enum):
    """Rate limiting strategy for API calls."""""""
    FIXED_WINDOW = auto()  # Fixed time window rate limiting
    SLIDING_WINDOW = auto()  # Sliding window rate limiting
    TOKEN_BUCKET = auto()  # Token bucket algorithm
    LEAKY_BUCKET = auto()  # Leaky bucket algorithm


class EnvironmentStatus(Enum):
    """Environment instance status."""""""
    PENDING = "pending""    CREATING = "creating""    RUNNING = "running""    FAILED = "failed""    TERMINATED = "terminated""    EXPIRED = "expired""

class EnvironmentIsolation(Enum):
    """Environment isolation levels."""""""
    NONE = "none"  # No isolation"    PROCESS = "process"  # Separate process"    CONTAINER = "container"  # Docker container"    VM = "vm"  # Virtual machine"    NAMESPACE = "namespace"  # Linux namespace"