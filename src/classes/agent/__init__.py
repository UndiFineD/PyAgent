"""Auto-generated module exports."""

from ._helpers import (
    _empty_dict_str_any,
    _empty_dict_str_float,
    _empty_dict_str_int,
    _empty_dict_str_str,
    _empty_list_str,
    _empty_list_dict_str_any,
    _empty_plugin_config_list,
    HAS_REQUESTS,
    requests,
    HAS_TQDM,
    tqdm,
)

from ..base_agent import (
    _empty_agent_event_handlers,
    _empty_dict_str_health_checks,
)

from .utils import (
    load_codeignore,
    setup_logging,
    _multiprocessing_worker,
    fix_markdown_content,
)


# Need to import AgentPluginConfig before defining _empty_plugin_config_list
# so we'll do this after the imports
from .Agent import Agent
from .AgentChain import AgentChain
from .AgentChainStep import AgentChainStep
from .AgentConfig import AgentConfig
from .AgentExecutionState import AgentExecutionState
from .AgentHealthCheck import AgentHealthCheck
from .AgentPluginBase import AgentPluginBase
from .AgentPluginConfig import AgentPluginConfig
from .AgentPriority import AgentPriority
from .AgentPriorityQueue import AgentPriorityQueue
from .AgentTemplate import AgentTemplate
from .CachedResult import CachedResult
from .CircuitBreaker import CircuitBreaker
from .ConditionalExecutor import ConditionalExecutor
from .ConfigFormat import ConfigFormat
from .ConfigLoader import ConfigLoader
from .DependencyGraph import DependencyGraph
from .DiffGenerator import DiffGenerator
from .DiffOutputFormat import DiffOutputFormat
from .DiffResult import DiffResult
from .ExecutionCondition import ExecutionCondition
from .ExecutionProfile import ExecutionProfile
from .ExecutionScheduler import ExecutionScheduler
from .FileLock import FileLock
from .FileLockManager import FileLockManager
from .GitBranchProcessor import GitBranchProcessor
from .GracefulShutdown import GracefulShutdown
from .HealthChecker import HealthChecker
from .HealthStatus import HealthStatus
from .IncrementalProcessor import IncrementalProcessor
from .IncrementalState import IncrementalState
from .LockType import LockType
from .ProfileManager import ProfileManager
from .RateLimitConfig import RateLimitConfig
from .RateLimitStrategy import RateLimitStrategy
from .RateLimiter import RateLimiter
from .ResultCache import ResultCache
from .ScheduledExecution import ScheduledExecution
from .ShutdownState import ShutdownState
from .SpanContext import SpanContext
from .TelemetryCollector import TelemetryCollector
from .TelemetrySpan import TelemetrySpan
from .TemplateManager import TemplateManager
from .ValidationRule import ValidationRule
from .ValidationRuleManager import ValidationRuleManager
from .cli import main
