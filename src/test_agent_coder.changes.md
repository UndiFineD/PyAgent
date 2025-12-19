# Changelog

## [2025-12-19] - Documentation refresh

- Refreshed companion docs to match `src/test_agent_coder.py` and updated SHA256 fingerprint.

## Session 9 - 2025-01-16

### Added - Coder Tests (20 test classes)
- `TestCodeRefactoring` - Tests for code refactoring suggestions and application
- `TestMultiLanguageCodeGeneration` - Tests for code generation for multiple programming languages
- `TestCodeDocumentationGeneration` - Tests for code comment and documentation generation
- `TestCodeOptimizationPatterns` - Tests for code optimization pattern application
- `TestDeadCodeDetection` - Tests for dead code detection and removal
- `TestDependencyInjectionPatterns` - Tests for code dependency injection patterns
- `TestCodeSplitting` - Tests for code splitting and module extraction
- `TestCodeConsistency` - Tests for code consistency enforcement across files
- `TestCodeTemplates` - Tests for code template instantiation
- `TestTypeAnnotationInference` - Tests for code type annotation inference
- `TestStyleUnification` - Tests for code style unification
- `TestMergeConflictResolution` - Tests for code merge conflict resolution
- `TestAPICompatibility` - Tests for code API compatibility checking
- `TestIncrementalImprovement` - Tests for incremental code improvement strategies
- `TestQualityGates` - Tests for code quality gates and thresholds
- `TestSecurityScanning` - Tests for code security scanning integration
- `TestComplexityAnalysis` - Tests for code complexity analysis
- `TestCoverageGapDetection` - Tests for code coverage gap detection
- `TestPerformanceProfiling` - Tests for code performance profiling
- `TestMigrationAutomation` - Tests for code migration automation

---

- Initial version of test_agent-coder.py
- 2025-12-15: Replaced placeholder-only tests with real coverage for keyword fallback vs `BaseAgent` delegation.

## [2025-12-15]
- Rename the file to be pytest-importable (avoid '-' and extra '.'), then update references. (Fixed)
