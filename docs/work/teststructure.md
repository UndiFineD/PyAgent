# PyAgent Testing Hierarchy (Jan 2026)

To ensure stability across the 5-tier architecture, tests are organized by scope and specialized persona.

## 1. Directory Structure
- tests/unit/:
  - Isolated tests for core primitives (src/core/).
  - Mocked dependencies using unittest.mock or pytest-mock.
- tests/integration/:
  - Validates cross-tier communication (e.g., Logic -> Infrastructure).
  - Tests plugin loading and fleet orchestration.
- tests/specialists/:
  - Deep validation for specific agents (CoderAgent, SecurityAgent, etc.).
  - Scenario-based testing (e.g., "Fix a bug in a legacy file").
- tests/phases/:
  - Milestone validation (e.g., test_phase130.py).
  - End-to-end flows for new feature rollouts.
- tests/ui/:
  - CLI and Dashboard integration tests.
  - Snapshot testing for report generation.

## 2. Testing Standards
- Pytest: Primary runner for all tests.
- Async Testing: pytest-asyncio for agent communication validation.
- Coverage: Minimum 80% coverage for src/core/.
- Performance: Benchmarking scripts in temp/ to monitor trillion-parameter lookups.

## 3. Toolchain
- pytest-cov: For coverage reporting.
- hypothesis: For property-based testing of MD5 sharding and data integrity.
- tox: For multi-environment (Python 3.12, 3.13) validation.
