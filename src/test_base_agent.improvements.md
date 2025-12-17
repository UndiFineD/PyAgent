# Improvements: `test_base_agent.py`

## Fixed
- Security: Use `check=True` or `check=False` explicitly in `subprocess.run`. (Fixed - verified in agent_backend.py)

## Suggested improvements
- [x] FIXED: [2025-06-14] Add tests for prompt templating system.
- [x] FIXED: [2025-06-14] Test conversation history management.
- [x] FIXED: [2025-06-14] Add tests for response post-processing hooks.
- [x] FIXED: [2025-06-14] Test model selection per agent type.
- [x] FIXED: [2025-06-14] Add tests for request batching performance.
- [x] FIXED: [2025-06-14] Test custom authentication methods.
- [x] FIXED: [2025-06-14] Add tests for response quality scoring.
- [x] FIXED: [2025-06-14] Test prompt versioning and A/B testing.
- [x] FIXED: [2025-06-14] Add tests for context window management.
- [x] FIXED: [2025-06-14] Test multimodal input handling.
- [x] FIXED: [2025-06-14] Add tests for content-based response caching.
- [x] FIXED: [2025-06-14] Test agent composition patterns.
- [x] FIXED: [2025-06-14] Add tests for token budget management.
- [x] FIXED: [2025-06-14] Test custom serialization formats.
- [x] FIXED: [2025-06-14] Add tests for request prioritization logic.
- [x] FIXED: [2025-06-14] Test agent state persistence.
- [x] FIXED: [2025-06-14] Add tests for agent event hooks.
- [x] FIXED: [2025-06-14] Test agent plugin loading.
- [x] FIXED: [2025-06-14] Add tests for agent health diagnostics.
- [x] FIXED: [2025-06-14] Test agent configuration profiles.

## Fixed (Moved to test_base_agent.changes.md)
- Add tests for file encoding edge cases. (Fixed)
- Test all backend selection scenarios. (Fixed)
- Add tests for timeout handling. (Fixed)
- Test markdown content fixing edge cases. (Fixed)
- Add parametrized tests for file extensions. (Fixed)
- Test error recovery and retry mechanisms. (Fixed)
- Add tests for diff generation. (Fixed)
- Test missing backend scenarios. (Fixed)
- Add tests for concurrent operations. (Fixed)
- Test markdown preservation. (Fixed)
- Add tests for large file handling. (Fixed)
- Test import fallback chains. (Fixed)
- Add tests for setup_logging. (Fixed)
- Test create_main_function. (Fixed)
- Add integration tests with real I/O. (Fixed)

## Notes
- These are suggestions based on static inspection; validate behavior with tests/runs.
- File: `scripts/agent/test_base_agent.py`
