# Setup & Installation

This guide explains how to prepare a development environment for PyAgent.

## Requirements

- Python 3.11+
- Git
- Docker (optional, used by some integration tests)

## Steps

1. Clone the repository:
   ```powershell
   git clone https://github.com/UndiFineD/PyAgent.git
   cd PyAgent
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Run the setup script to create required directories:
   ```powershell
   python scripts/setup_structure.py
   ```
5. Verify everything is working by running the test suite:
   ```powershell
   pytest
   ```

You can also build the documentation locally using MkDocs:
```powershell
pip install mkdocs mkdocstrings
mkdocs build
```

---

## Local Testing

PyAgent uses a **local-first** testing philosophy. All checks that can run locally should
run locally before pushing. CI (`ci.yml`) is the cloud gate; `pre-commit` + `pytest` are
the local gate.

### 1. Pre-commit hooks (run on every commit automatically)

Install once:
```powershell
pip install pre-commit
pre-commit install
```

Run manually against all files:
```powershell
pre-commit run --all-files
```

This runs:
- **ruff** — lint + auto-fix (`src/`, `tests/`, `scripts/`, `docs/**/*.py`)
- **mypy** — type checking (same scope)
- **enforce-branch** — validates that the current branch matches the project naming convention
- **run-precommit-checks** — `scripts/ci/run_checks.py --profile precommit` (curated smoke tests without Rust)

### 2. Full test suite

```powershell
pytest
```

To mirror the CI shards exactly:
```powershell
# Shard 1 — CI/structure/docs tests
pytest tests/ci/ tests/structure/ tests/docs/ -n 2

# Shard 2 — General tests (excludes long-running suites)
pytest tests/ --ignore=tests/core --ignore=tests/security --ignore=tests/integration `
              --ignore=tests/agents --ignore=tests/observability `
              --ignore=tests/runtime --ignore=tests/tools -n 2

# Shard 3 — Core, security, integration, agents, tools
pytest tests/core/ tests/security/ tests/integration/ `
       tests/agents/ tests/observability/ tests/runtime/ tests/tools/ -n 2
```

### 3. Local CodeQL (optional, for security analysis)

The CodeQL CLI is available at `C:\Dev\CodeQL`. To run the Python queries locally:

```powershell
# Create a database from the Python sources
C:\Dev\CodeQL\codeql database create codeql-db-python `
    --language=python `
    --source-root=src

# Analyse with the built-in security-and-quality suite
C:\Dev\CodeQL\codeql database analyze codeql-db-python `
    --format=sarif-latest `
    --output=codeql-results-python.sarif `
    python-security-and-quality.qls
```

The same scan runs automatically in GitHub Actions via `security.yml` on every push to
`main`, every PR, and once per week. Results appear in the **Security → Code scanning**
tab of the repository.

### 4. CI workflows

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Functional correctness: full test suite (3-shard matrix), Rust build gate |
| `.github/workflows/security.yml` | Security scanning: CodeQL for Python + JavaScript |

No other workflow files should exist. If you see others, they are stale and should be removed.


That's it!  You now have a fully functioning development workspace.