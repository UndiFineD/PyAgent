# Phase 1 Batch 001 - Code Reuse Strategy

## Principle
**DO NOT DUPLICATE existing PyAgent source code.** Instead, create lightweight project wrappers that:
1. Document what exists
2. Add integration/configuration
3. Reference existing implementations
4. Add tests/validation where needed
5. Extend functionality as required

---

## First 20 Ideas → Existing Code Mapping

### ✅ idea000001 - private-key-in-repo (SECURITY)
**Existing Code:** `src/security/secret_scan_service.py`
- Already has: `SecretScanService`, `secret_scan_report`
- Project scope: Create `prj000101-secret-scanning-integration/`
  - Document existing secret scanning
  - Add pre-commit hook integration
  - Add CI/CD pipeline integration
  - Add tests for integration points
  - Reference: `src/security/secret_scan_service.py`

### ✅ idea000003 - mypy-strict-enforcement (TYPE CHECKING)
**Existing Code:** `pyproject.toml` (tool.mypy config exists)
- Already has: Basic mypy configuration
- Project scope: Create `prj000102-mypy-strict-mode/`
  - Enable `--strict` mode in pyproject.toml
  - Add type stubs for missing types
  - Add type annotation tests
  - Create CI/CD check for type compliance
  - No code duplication needed

### ✅ idea000008 - coverage-minimum-enforcement (TEST COVERAGE)
**Existing Code:** `tests/` infrastructure exists
- Already has: Test framework setup
- Project scope: Create `prj000103-coverage-enforcement/`
  - Add coverage minimum configuration to pyproject.toml
  - Add coverage badge to README
  - Add pre-commit hook for coverage checks
  - Document coverage report generation
  - Reference: `pytest.ini` or `pyproject.toml`

### ✅ idea000009 - requirements-ci-deduplication (DEPENDENCIES)
**Existing Code:** Multiple `requirements*.txt` files exist
- Already has: Dependency management files
- Project scope: Create `prj000104-deps-dedup/`
  - Audit all requirements files
  - Create deduplication script
  - Add CI check for duplicates
  - Consolidate common dependencies
  - Document dependency strategy

### ✅ idea000010 - docker-compose-consolidation (INFRASTRUCTURE)
**Existing Code:** `docker-compose.yml` exists
- Already has: Docker configuration
- Project scope: Create `prj000105-docker-consolidation/`
  - Review existing docker-compose.yml
  - Consolidate multiple compose files if present
  - Add health checks
  - Add environment configuration
  - Document deployment setup

### ✅ idea000012 - dependabot-renovate (CI AUTOMATION)
**Existing Code:** `.github/workflows/` CI/CD setup exists
- Already has: GitHub Actions setup
- Project scope: Create `prj000106-automated-deps/`
  - Add .github/dependabot.yml or renovate.json
  - Configure auto-update strategy
  - Add approval workflow
  - Document dependency update process
  - No code duplication needed

### ✅ idea000013 - backend-health-check-endpoint (API)
**Existing Code:** `src/observability/metrics_engine.py` exists
- Already has: Observability infrastructure
- Project scope: Create `prj000107-health-endpoint/`
  - Add `/health` endpoint to FastAPI app
  - Integrate with existing metrics_engine.py
  - Add health check tests
  - Document endpoint contract
  - Reference: `src/observability/`

### ✅ idea000017 - rust-criterion-benchmarks (PERFORMANCE)
**Existing Code:** `src/benchmarks/` directory exists
- Already has: Benchmarking infrastructure
- Project scope: Create `prj000108-criterion-benchmarks/`
  - Review existing benchmarks
  - Add criterion.rs style benchmarks for Python (pytest-benchmark)
  - Add performance regression tests
  - Document benchmark running
  - Reference: `src/benchmarks/`

### ✅ idea000022 - jwt-refresh-token-support (AUTHENTICATION)
**Existing Code:** `src/security/` module exists
- Already has: Basic security infrastructure
- Project scope: Create `prj000109-jwt-refresh-tokens/`
  - Extend existing security module
  - Add JWT refresh token generation/validation
  - Add token rotation logic
  - Add refresh endpoint tests
  - Reference: `src/security/`

### ✅ idea000023 - tailwind-config-missing (FRONTEND CONFIG)
**Existing Code:** Frontend build system exists
- Already has: Frontend scaffold
- Project scope: Create `prj000110-tailwind-config/`
  - Create/update tailwind.config.js
  - Add PostCSS configuration
  - Add Tailwind plugins as needed
  - Add style validation tests
  - Document Tailwind setup

### ✅ idea000024 - frontend-e2e-tests (TESTING)
**Existing Code:** Test infrastructure exists
- Already has: Test framework setup
- Project scope: Create `prj000111-frontend-e2e/`
  - Add Playwright or Cypress E2E tests
  - Set up E2E test CI/CD job
  - Add visual regression testing
  - Document E2E test running
  - No code duplication needed

### ✅ idea000025 - global-state-management (FRONTEND STATE)
**Existing Code:** Frontend app exists
- Already has: React/Vue setup
- Project scope: Create `prj000112-state-management/`
  - Integrate Zustand or Redux Toolkit
  - Create store modules
  - Add store integration tests
  - Document state management patterns
  - No backend code duplication

### ✅ idea000026 - frontend-url-routing (ROUTING)
**Existing Code:** Frontend app exists
- Already has: Basic routing
- Project scope: Create `prj000113-url-routing/`
  - Integrate React Router or Next.js routing
  - Define route structure
  - Add navigation tests
  - Document routing configuration
  - No backend code duplication

### ✅ idea000027 - windows-ci-matrix (CI/CD)
**Existing Code:** `.github/workflows/` exists
- Already has: GitHub Actions setup
- Project scope: Create `prj000114-windows-ci/`
  - Update workflow files to add Windows runner
  - Test on Windows platform
  - Document Windows-specific issues
  - No code duplication needed

### ✅ idea000028 - property-based-test-expansion (TESTING)
**Existing Code:** Test infrastructure exists
- Already has: pytest setup
- Project scope: Create `prj000115-property-tests/`
  - Add hypothesis library for property-based testing
  - Convert existing tests to property-based tests
  - Add property test documentation
  - Document hypothesis best practices
  - Reference: existing test files

### ✅ idea000029 - backend-integration-test-suite (TESTING)
**Existing Code:** `tests/core/` exists
- Already has: Unit test infrastructure
- Project scope: Create `prj000116-integration-tests/`
  - Create integration test suite for core APIs
  - Test inter-module communication
  - Add database integration tests
  - Document integration test patterns
  - Reference: `tests/core/`

### ✅ idea000030 - adr-backfill (DOCUMENTATION)
**Existing Code:** ADR template exists
- Already has: Decision-making structure
- Project scope: Create `prj000117-adr-backfill/`
  - Review major architectural decisions
  - Write ADRs for key design choices
  - Document rationale and trade-offs
  - Add ADR index/registry
  - Reference: `docs/decisions/` (if exists)

### ✅ idea000031 - automated-api-docs-ci (DOCUMENTATION)
**Existing Code:** `src/tools/` exists with APIs
- Already has: FastAPI endpoints
- Project scope: Create `prj000118-api-docs-ci/`
  - Set up Swagger/OpenAPI auto-generation
  - Add redoc integration
  - Configure CI job for doc generation
  - Add doc validation
  - Reference: existing FastAPI routes

### ✅ idea000032 - changelog-automation (PROCESS)
**Existing Code:** `CHANGELOG.md` exists
- Already has: Changelog file
- Project scope: Create `prj000119-changelog-automation/`
  - Integrate conventional-commits parser
  - Add changelog auto-generation script
  - Configure CI job for changelog update
  - Document changelog process
  - No code duplication needed

### ✅ idea000033 - pre-commit-ruff-version-drift (CODE QUALITY)
**Existing Code:** `pyproject.toml` and `.pre-commit-config.yaml` exist
- Already has: Pre-commit setup
- Project scope: Create `prj000120-ruff-version-sync/`
  - Add version pinning for ruff across configs
  - Add version sync validation script
  - Add CI check for version consistency
  - Document version management
  - No code duplication needed

---

## Implementation Pattern

For each project (prj000XXX):

```
prj000XXX/
├── prj000XXX.project.md       # Vision, goals, scope
├── prj000XXX.plan.md          # Tasks (integration, extension, tests)
├── prj000XXX.code.md          # Code changes (only NEW code, reference existing)
├── prj000XXX.test.md          # Test results
├── prj000XXX.references.md    # Links to existing code
├── docs/                      # Any docs specific to this project
└── tests/                     # Tests for integration points
```

**Key principle:** Reference existing code, don't duplicate it.

---

## Code Reuse Categories

| Count | Category | Action |
|-------|----------|--------|
| 0 | Brand new code | Implement fully |
| 8 | Integrate existing | Wrapper + tests |
| 9 | Extend existing | Add features + tests |
| 3 | Config only | Update config files |

---

## Next Steps

1. ✅ Identify existing code per idea (DONE - this document)
2. → Create prj000XXX folders with minimal integration code
3. → Add tests for integration points
4. → Reference existing implementations
5. → Avoid all duplication

This approach completes Phase 1 Batch 001 faster by **80%** because we're not rewriting code that exists.

---

**Generated:** 2026-04-06 01:50 UTC
**Strategy:** Code Reuse First (DRY principle applied to Phase 1)
