# Changelog

## [2025-12-18] - Static typing + optional dependency cleanup

### Changed (2025-12-18)

- Optional imports were made single-assignment and type-checker friendly:

  - `requests` guarded by `HAS_REQUESTS: Final[bool]`.
  - `tqdm` guarded by `HAS_TQDM: Final[bool]` with a typed fallback.

- Dataclass defaults were updated to use typed `default_factory` helpers to
  avoid `list[Unknown]` / `dict[Unknown, Unknown]` propagation.
- Dynamic markdown fixer loader `_load_fix_markdown_content()` was typed to

  return `Callable[[str], str]` and a typed no-op fallback is used when missing.

### Notes

- This update is focused on static analysis correctness and does not intend to
  change runtime behavior.

## [2025-01-16] - Session 9

### Added - Phase 9: Agent Chaining, Branch Processing, and Advanced Features

#### Agent Chaining

- `AgentChainStep`: Dataclass for chain steps with input/output transforms
- `AgentChain`: Chain multiple agents for sequential execution
- `add_step()`: Add step with transforms and conditions
- `execute()`: Execute chain with agent executor callback
- `get_results()`: Get results from last execution

#### Git Branch-Based Processing

- `GitBranchProcessor`: Process files changed in specific git branches
- `get_changed_files()`: Get files changed between branches
- `get_current_branch()`: Get current git branch name
- `list_branches()`: List branches with optional pattern filtering

#### Custom Validation Rules

- `ValidationRule`: Dataclass for custom validation rules
- `ValidationRuleManager`: Manage custom validation rules per file type
- `add_rule()`, `remove_rule()`: Rule management
- `validate()`: Validate content against applicable rules
- `get_rules_for_file()`: Get rules applicable to a file

#### Agent Priority Queue

- `AgentPriorityQueue`: Priority queue for ordered agent execution
- `add_agent()`: Add agent with priority and dependencies
- `remove_agent()`: Remove agent from queue
- `get_execution_order()`: Get agents in execution order with dependency resolution

#### Telemetry and Observability

- `TelemetrySpan`: Dataclass for tracing spans (OpenTelemetry-compatible)
- `TelemetryCollector`: Collect telemetry data for observability
- `span()`: Context manager for creating spans
- `SpanContext`: Context for managing span attributes and events
- `export_json()`: Export spans as JSON

#### Conditional Agent Execution

- `ExecutionCondition`: Dataclass for execution conditions
- `ConditionalExecutor`: Execute agents based on file content conditions
- `add_condition()`: Add condition with check function
- `set_agent_conditions()`: Set conditions for an agent
- `should_execute()`: Check if agent should execute for file

#### Agent Templates

- `AgentTemplate`: Dataclass for agent templates
- `TemplateManager`: Manage agent templates for common use cases
- Default templates: python_full, markdown_docs, quick_fix
- `add_template()`, `get_template()`: Template management
- `list_templates()`: List available templates

#### Agent Dependency Resolution

- `DependencyGraph`: Resolve agent dependencies for ordered execution
- `add_node()`, `add_dependency()`: Build dependency graph
- `resolve()`: Topological sort for execution order
- Circular dependency detection

#### Agent Execution Profiles

- `ExecutionProfile`: Dataclass for execution settings
- `ProfileManager`: Manage agent execution profiles
- Default profiles: default, fast, ci
- `activate()`, `get_active_config()`: Profile activation

#### Agent Result Caching

- `CachedResult`: Dataclass for cached agent results
- `ResultCache`: Cache agent results for reuse with TTL
- `get()`, `set()`: Cache operations
- `invalidate()`: Invalidate cache for file

#### Agent Execution Scheduling

- `ScheduledExecution`: Dataclass for scheduled executions
- `ExecutionScheduler`: Schedule agent executions
- `add_schedule()`: Add schedule (hourly, daily, weekly, HH:MM)
- `is_due()`, `mark_complete()`: Schedule checking and completion

## [2025-01-13] - Session 6

### Added - Phase 6: Plugin System, Rate Limiting, and Advanced Features

#### Enums for Type Safety

- `AgentExecutionState`: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED, PAUSED
- `RateLimitStrategy`: FIXED_WINDOW, SLIDING_WINDOW, TOKEN_BUCKET, LEAKY_BUCKET
- `ConfigFormat`: YAML, TOML, JSON, INI
- `LockType`: SHARED, EXCLUSIVE, ADVISORY
- `DiffOutputFormat`: UNIFIED, CONTEXT, SIDE_BY_SIDE, HTML
- `AgentPriority`: CRITICAL, HIGH, NORMAL, LOW, BACKGROUND
- `HealthStatus`: HEALTHY, DEGRADED, UNHEALTHY, UNKNOWN

#### Dataclasses for Data Structures

- `RateLimitConfig`: Rate limiting configuration with requests_per_second, burst_size
- `AgentPluginConfig`: Plugin configuration with name, module_path, entry_point
- `FileLock`: File lock information with path, type, owner, timestamps
- `DiffResult`: Diff result with original/modified content, additions/deletions
- `IncrementalState`: State tracking for processed files and content hashes
- `AgentHealthCheck`: Health check result with status, response_time, error details
- `ShutdownState`: Graceful shutdown state with current/pending/completed files
- `AgentConfig`: Full agent configuration loaded from config files

#### Plugin System

- `AgentPluginBase`: Abstract base class for custom agent plugins
- `register_plugin()`: Register third-party agent plugins
- `unregister_plugin()`: Remove plugins by name
- `get_plugin()`: Retrieve registered plugins
- `run_plugins()`: Execute all plugins on a file with priority ordering
- `load_plugins_from_config()`: Load plugins from YAML/TOML config

#### Rate Limiting

- `RateLimiter`: Token bucket implementation with thread-safe token acquisition
- `enable_rate_limiting()`: Enable rate limiting on agent
- `get_rate_limit_stats()`: Get current rate limiter statistics
- `--rate-limit` CLI argument for configuring requests per second

#### Configuration File Support

- `ConfigLoader`: Load and parse YAML/TOML/JSON config files
- `Agent.from_config_file()`: Create agent from configuration file
- `Agent.auto_configure()`: Auto-detect and load config from repository
- `--config` CLI argument for specifying config file path
- Support for agent.yaml, agent.toml, agent.json naming conventions

#### File Locking

- `FileLockManager`: Thread-safe file lock management with timeouts
- `acquire_lock()`: Acquire exclusive or shared file locks
- `release_lock()`: Release held locks
- `enable_file_locking()`: Enable file locking on agent
- `--enable-file-locking` CLI argument
- Automatic cleanup of expired locks

#### Diff Preview Mode

- `DiffGenerator`: Generate and format diffs in multiple formats
- `preview_changes()`: Preview file changes without applying
- `show_pending_diffs()`: Show all pending diffs in dry-run mode
- `enable_diff_preview()`: Enable diff preview mode
- `--diff-preview` CLI argument
- Colorized console output with ANSI escape codes

#### Graceful Shutdown

- `GracefulShutdown`: Signal handler with state persistence
- `install_handlers()`: Install SIGINT/SIGTERM handlers
- `should_continue()`: Check if processing should continue
- `set_current_file()`: Track currently processing file
- `load_resume_state()`: Load state for resuming interrupted runs
- `enable_graceful_shutdown()`: Enable graceful shutdown
- `resume_from_shutdown()`: Resume from previous interrupted run
- `--graceful-shutdown` and `--resume` CLI arguments

#### Incremental Processing

- `IncrementalProcessor`: Track file modification times and content hashes
- `get_changed_files()`: Get files changed since last run
- `mark_processed()`: Mark file as processed with hash
- `complete_run()`: Save state after successful run
- `reset_state()`: Force full reprocessing
- `enable_incremental_processing()`: Enable incremental processing
- `reset_incremental_state()`: Reset state on agent
- `--incremental` CLI argument

#### Health Checks

- `HealthChecker`: Run health checks on all agent components
- `check_python()`: Check Python environment
- `check_git()`: Check git availability
- `check_agent_script()`: Check agent script validity
- `run_all_checks()`: Run all health checks
- `is_healthy()`: Quick health status check
- `print_report()`: Print formatted health report
- `run_health_checks()`: Agent method for health checks
- `print_health_report()`: Print health check report
- `--health-check` CLI argument

#### Test Coverage

- 60+ new tests for Phase 6 features
- TestAgentExecutionStateEnum, TestRateLimitStrategyEnum, TestConfigFormatEnum
- TestLockTypeEnum, TestDiffOutputFormatEnum, TestAgentPriorityEnum, TestHealthStatusEnum
- TestRateLimitConfigDataclass, TestAgentPluginConfigDataclass
- TestFileLockDataclass, TestDiffResultDataclass, TestIncrementalStateDataclass
- TestAgentHealthCheckDataclass, TestShutdownStateDataclass
- TestRateLimiter, TestFileLockManager, TestDiffGenerator
- TestIncrementalProcessor, TestGracefulShutdown, TestConfigLoader, TestHealthChecker
- TestAgentPluginSystem, TestAgentRateLimiting, TestAgentFileLocking
- TestAgentDiffPreview, TestAgentIncrementalProcessing
- TestAgentGracefulShutdown, TestAgentHealthChecks, TestAgentConfigFile
- TestPhase6Integration

## [2025-12-16]

### Added (2025-12-16)

- Refactor: File split into `agent_orchestrator.py`, `agent_processor.py`, `agent_reporter.py`. (Fixed)
- Configurable timeout values per agent type. (Fixed)
- Progress tracking with timestamps for performance monitoring. (Fixed)
- Integration tests with real repositories for end-to-end validation. (Fixed)
- Dry-run mode with `--dry-run` flag. (Fixed)
- Summary statistics with `--summary` flag. (Fixed)
- Selective agent execution with `--only-agents` flag. (Fixed)
- Rollback functionality with file snapshots. (Fixed)
- Cascading `.agentignore` support. (Fixed)
- Async file processing with `--async` flag. (Fixed)
- Parallel processing with `--multiprocessing` and `--workers` flags. (Fixed)
- Webhook/callback support with `--webhook` flag. (Fixed)
- Detailed improvement reports. (Fixed)
- Performance benchmarking and metrics collection. (Fixed)
- Cost analysis for different API backends. (Fixed)
- Circuit breaker pattern for failing backends. (Fixed)
- Automated snapshot cleanup with retention policies. (Fixed)

## [1.0.2] - 2025-12-16

### Fixed

- Improved exception handling in `_run_command` to be more specific (`OSError`) and robust (`errors='replace'`). (Fixed)
- Added type hint and docstring to `_load_fix_markdown_content`. (Fixed)
- Added type hints for all methods. (Fixed)
- Add logging for all major actions. (Fixed)

## [1.0.1] - 2025-12-15

### Changed (1.0.1)

- Improved Windows robustness for subprocess output decoding in `BaseAgent`.
- Expanded agent test coverage (unit tests under `tests/` plus legacy `scripts/agent/test_*.py`).
- Added VS Code tasks to run both agent test suites.
- Improved exception handling in `_run_command` to be more specific (`OSError`) and robust (`errors='replace'`).
- Added type hints to all methods in `agent.py`.

## [1.0.0] - 2025-12-14

### Added (1.0.0)

- Initial implementation of the Agent orchestrator
- Support for multiple specialized sub-agents
- Iterative improvement loop with change detection
- Git integration for automatic commits and pushes
- Configurable file processing limits
- Comprehensive progress reporting

### Features

- Recursive code file discovery
- Automatic creation of supporting documentation files
- Error handling and recovery
- Stats reporting for processed files
- Command-line interface with multiple options

## [0.1.0] - 2025-12-13

### Initial

- Basic agent framework
- Sub-agent coordination system
- File processing pipeline
- Initial git operations support

## [2025-12-15]

- Add `--help` examples and validate CLI args (paths, required files). (Fixed)
- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting). (Fixed)
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Fixed)
- Function `__init__` is missing type annotations. (Fixed)
- Function `_commit_and_push` is missing type annotations. (Fixed)
- Function `_log_changes` is missing type annotations. (Fixed)
- Function `_mark_improvements_fixed` is missing type annotations. (Fixed)
- Function `main` is missing type annotations. (Fixed)
- Function `process_file` is missing type annotations. (Fixed)
- Function `run_stats_update` is missing type annotations. (Fixed)
- Function `run_tests` is missing type annotations. (Fixed)
- Function `run` is missing type annotations. (Fixed)
- Function `setup_logging` is missing type annotations. (Fixed)
