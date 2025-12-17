# Changelog

- 2025-12-15: Added utilities for legacy agent tests (safe path-loading of agent modules, including hyphenated filenames).

## Session 9 [2025-01-16]

### Added - ParameterizedTestGenerator Class
- `ParameterizedTestCase` dataclass: name, params, expected, tags
- `ParameterizedTestGenerator`: Generates test cases from parameter combinations
- `add_parameter()`: Add parameter with possible values
- `set_expected_fn()`: Set function to compute expected result
- `generate_cases()`: Generate all test case combinations

### Added - DependencyContainer Class (Test Dependency Injection)
- `DependencyContainer`: Container for test dependency injection
- `register()`: Register a dependency instance
- `register_factory()`: Register a dependency factory
- `resolve()`: Resolve a dependency
- `inject()`: Decorator to inject dependencies into function

### Added - FlakinessDetector Class
- `FlakinessReport` dataclass: test_name, runs, passes, failures, flakiness_score
- `FlakinessDetector`: Detects flaky tests through repeated execution
- `analyze()`: Analyze test for flakiness
- `get_history()`: Get flakiness history for a test
- `get_flaky_tests()`: Get tests that exceed flakiness threshold

### Added - TestDataCleaner Class
- `TestDataCleaner`: Utilities for cleaning up test data
- `register_path()`: Register directory for cleanup
- `register_file()`: Register file for cleanup
- `register_callback()`: Register cleanup callback
- `cleanup_all()`: Clean up all registered resources

### Added - CrossPlatformHelper Class
- `CrossPlatformHelper`: Helpers for cross-platform testing
- `is_windows()`, `is_linux()`, `is_macos()`: Platform checks
- `normalize_path()`: Normalize path for current platform
- `normalize_line_endings()`: Normalize line endings
- `skip_on_platform()`: Check if test should be skipped

### Added - TestLogger Class
- `TestLogEntry` dataclass: level, message, timestamp, test_name, extra
- `TestLogger`: Logger for test debugging
- `debug()`, `info()`, `warning()`, `error()`: Log methods
- `capture()`: Context manager to capture logs for a test
- `get_logs()`, `get_errors()`: Retrieve logs

### Added - ParallelTestRunner Class
- `ParallelTestResult` dataclass: test_name, passed, duration_ms, error, worker_id
- `ParallelTestRunner`: Helper for parallel test execution
- `add_test()`: Add test to run
- `run_all()`: Run all tests in parallel using ThreadPoolExecutor
- `get_summary()`: Get summary of parallel test execution

### Added - TestRecorder Class
- `RecordedInteraction` dataclass: call_type, call_name, args, kwargs, result
- `TestRecorder`: Records and replays test interactions
- `record_interaction()`: Record an interaction
- `get_replay_result()`: Get replayed result for a call
- `record()`, `replay()`: Context managers for modes
- `save()`, `load()`: Persist recordings to JSON

### Added - BaselineManager Class
- `TestBaseline` dataclass: name, values, created_at, version
- `BaselineManager`: Manages test baselines for comparison
- `save_baseline()`: Save a baseline
- `load_baseline()`: Load a baseline
- `compare()`: Compare current values against baseline

### Added - TestProfileManager Class
- `TestProfile` dataclass: name, settings, env_vars, enabled
- `TestProfileManager`: Manages test configuration profiles
- `add_profile()`, `get_profile()`: Profile management
- `activate()`, `deactivate()`: Profile activation
- `get_setting()`: Get setting from active profile
- `get_active_profile()`: Get currently active profile

## Session 6 [2025-01-13]

### Added - Type-Safe Enums
- `TestStatus` enum: PASSED, FAILED, SKIPPED, ERROR, PENDING
- `MockResponseType` enum: SUCCESS, ERROR, TIMEOUT, RATE_LIMITED, EMPTY
- `IsolationLevel` enum: NONE, TEMP_DIR, COPY_ON_WRITE, SANDBOX
- `TestDataType` enum: PYTHON_CODE, MARKDOWN, JSON, YAML, TEXT
- `PerformanceMetricType` enum: EXECUTION_TIME, MEMORY_USAGE, FILE_IO, CPU_TIME
- `CleanupStrategy` enum: IMMEDIATE, DEFERRED, ON_SUCCESS, NEVER

### Added - Dataclasses for Structured Data
- `TestFixture` dataclass: name, setup_fn, teardown_fn, scope, data
- `MockResponse` dataclass: content, response_type, latency_ms, tokens_used, error_message
- `TestDataFactory` dataclass: data_type, template, variations, seed
- `TestResult` dataclass: test_name, status, duration_ms, error_message, assertions_count
- `PerformanceMetric` dataclass: metric_type, value, unit, test_name, timestamp
- `TestEnvironment` dataclass: name, env_vars, temp_dir, isolation_level, cleanup
- `TestSnapshot` dataclass: name, content, content_hash, created_at, updated_at
- `TestAssertion` dataclass: name, expected, actual, passed, message

### Added - MockAIBackend Class
- `add_response()`: Add mock response for prompt pattern
- `set_default_response()`: Set default response
- `call()`: Call mock backend with simulated latency
- `get_call_history()`: Get history of calls
- `clear()`: Clear responses and history

### Added - FixtureGenerator Class
- `create_python_file_fixture()`: Create Python file fixture
- `create_directory_fixture()`: Create directory with files
- `cleanup_all()`: Clean up all created fixtures

### Added - TestDataGenerator Class
- `generate_python_code()`: Generate sample Python code
- `generate_markdown()`: Generate sample markdown content
- `generate_json()`: Generate sample JSON content

### Added - FileSystemIsolator Class
- Context manager for file system isolation
- `write_file()`: Write file in isolated environment
- `read_file()`: Read file from isolated environment
- `get_temp_dir()`: Get temporary directory

### Added - PerformanceTracker Class
- `track()`: Context manager to track execution time
- `record_metric()`: Record performance metric
- `get_metrics()`: Get all recorded metrics
- `get_summary()`: Get performance summary

### Added - SnapshotManager Class
- `save_snapshot()`: Save new snapshot
- `load_snapshot()`: Load existing snapshot
- `assert_match()`: Assert actual matches snapshot
- `get_diff()`: Get diff between snapshot and actual

### Added - TestResultAggregator Class
- `add_result()`: Add test result
- `get_results()`: Get all results
- `get_report()`: Get aggregated report with statistics
- `get_failures()`: Get failed tests

### Added - AgentAssertions Class
- `assert_valid_python()`: Assert code is valid Python
- `assert_contains_docstring()`: Assert code has docstrings
- `assert_markdown_structure()`: Assert markdown structure
- `assert_json_valid()`: Assert valid JSON

## [2025-12-16]
- Add type hints for all methods. (Fixed)
- Add docstrings for all methods. (Fixed)

## [2025-12-15]
- Added detailed logging for module loading.
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Fixed)
