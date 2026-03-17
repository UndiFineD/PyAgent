# PyAgent Project

## Overview
PyAgent is a comprehensive software development platform designed to streamline the development, testing, and deployment of secure and scalable applications.

## Getting Started (Run Locally)
This repo includes three runnable components:

1. **Core runtime (Python + Rust)** — the main logic and CI-tested code.
2. **Backend service** — a FastAPI/WebSocket worker in `backend/`.
3. **Frontend website** — a Vite/React app in `web/`.

### Run the core runtime & tests
```powershell
python -m pytest -q
```

### Run the backend
```powershell
python -m pip install -r backend/requirements.txt
uvicorn backend.app:app --reload
```

Health check:
```
curl http://localhost:8000/health
```

### Run the frontend
```powershell
cd web
npm install
npm run dev
```

Vite will print the URL it is serving on (usually `http://localhost:5173`, but it may pick a different port if 5173 is already in use).

> If you see a blank page, ensure the console has no errors and that the URL matches the port displayed by Vite.

## Asynchronous Runtime Helpers

A lightweight Tokio-backed runtime is available via the `runtime_py` wrapper. These helpers were added as part of the async runtime rollout and are intended to replace any remaining synchronous loops in the codebase.

Example usage:

```python
from runtime_py import spawn, on, emit, watch_file, run_http_server

# schedule a background task
spawn(async_work())

# simple in‑process event bus
on("data", lambda x: process(x))
emit("data", 42)

# watch a configuration file for changes
watch_file("/etc/myapp.conf", lambda path: reload_config(path))

# run a minimal HTTP service
async def handler(uri: str):
    return 200, "ok"
run_http_server("127.0.0.1:8000", handler)
```

These functions are thin wrappers; the implementation may migrate between Python and Rust without affecting callers.

### Performance Benchmarks

A simple benchmark script is available at `performance/metrics_bench.py`. It
compares the old synchronous loop against the new runtime-driven async loop:

```powershell
python performance/metrics_bench.py
```

On a typical development machine you should see a dramatic speedup, e.g.:

```
sync loop: 0.45s
async runtime: 0.02s
```

Feel free to modify the script to profile other subsystems as they are migrated.



## Core Components

### GitHub Import System
A robust system that processes lines from `user/import/github.md` to download repositories into `.external/github/<user>/<repository>/` and generate architecture documents with detailed file descriptions.

### Unified Transaction Manager
A centralized service that manages all transaction operations across the system, ensuring consistency, reliability, and security.

### Hybrid LLM Security Core
A security-first rewrite of the `rust_core` library, driven by Python integration tests. The new core provides inline encryption/decryption, transactional file operations, and monthly key rotation with full memory-safe Rust implementation.

## Workflow

### GitHub Import Process
1. **Configuration Loading** - The system loads the `user/import/github.md` file to get the list of repositories to import.
2. **Repository Parsing** - Each line in the file is parsed to extract the user and repository name in the format `user/repository`.
3. **Repository Download** - For each repository, the system downloads it to the directory structure: `.external/github/<user>/<repository>/`.
4. **File Description Generation** - The system creates a `*.desc.md` file for every file in every directory of the downloaded repository.
5. **Architecture Compilation** - All the content from the `*.desc.md` files is combined into a single `architecture.md` file in the repository's directory.

### Transaction Management Process
1. **Request Ingestion** - External clients send transaction requests to the transaction service.
2. **Validation** - The transaction validator checks the request against business rules and data integrity constraints.
3. **Processing** - The transaction service coordinates the execution of the transaction, potentially involving multiple services or data stores.
4. **Persistence** - The transaction repository stores the transaction data with ACID properties.
5. **Monitoring** - The transaction monitor tracks the transaction status and logs events for auditing and analysis.
6. **Completion** - Upon successful completion, the transaction is marked as complete and notifications are sent to relevant parties.

### Security Core Implementation Process
1. **Add Failing Test** - Write a failing Python encryption round-trip test that verifies the presence of `encrypt_data` and `decrypt_data` functions.
2. **Run Test** - Execute the test to verify it fails due to missing functions.
3. **Implement Rust Functions** - Develop the Rust functions in `security/crypto.rs` to provide encryption and decryption capabilities.
4. **Update Python Bindings** - Modify the Python bindings to expose the new Rust functions.
5. **Verify Functionality** - Run the test again to confirm it passes, demonstrating successful integration.

## Key Features

### Asynchronous Event Runtime ⚙️
- **Node.js‑style async infrastructure** powered by a global Rust/Tokio runtime and thin Python bindings (`runtime.spawn_task`, `runtime.set_timeout`, `runtime.create_queue`, etc.).
- **No synchronous loops allowed** – the `tests/test_async_loops.py` audit script runs in CI and fails whenever Python code contains blocking `for`/`while` constructs, ensuring all new development is async-first.
- Built‑in event bus, file watchers, HTTP server, and channels provide primitives for every subsystem.

### GitHub Import System
- Detailed file description format with structured content (path, size, content summary, purpose, dependencies, usage context, version information, notes)
- Comprehensive architecture document structure including repository overview, component breakdown, file system hierarchy, key files and functions, interactions and dependencies, design patterns and principles, and future enhancements
- Robust error handling for file not found, parsing errors, download failures, file generation failures, and compilation failures
- Security considerations including authentication, authorization, data privacy, and secure storage
- Performance optimization through batch processing, parallel downloads, caching, and efficient file reading

### Unified Transaction Manager
- Core components: Transaction Service, Repository, Validator, Monitor, and Security Layer
- Communication flow from request ingestion to completion
- Key design principles focusing on consistency, reliability, and security
- Failure handling mechanisms including rollback and retry strategies
- Integration points with various system components
- Future enhancement directions

### Hybrid LLM Security Core
- Rust FFI bridge (`rust_core/` crate) compiled as `cdylib` with `pyo3` bindings
- New `security/crypto.rs` module housing encryption, transaction and key-management routines
- Python test layer in `rust_core/tests/` exercising every security API, failing first then guiding the Rust implementation
- Existing dynamic test generator remains, but focused tests live alongside it

## Future Enhancements

### GitHub Import System
- Repository analysis to identify code quality issues, security vulnerabilities, and technical debt
- AI-powered suggestions for code improvements, refactoring, and optimization
- Version comparison to track changes over time
- Dependency graph showing how files and components relate to each other
- Multi-repository support for simultaneous import
- Blockchain integration for immutable repository records

### Unified Transaction Manager
- Real-time analytics for transaction pattern analysis
- Machine learning models for anomaly detection and fraud prevention
- Multi-region support for distributed transaction processing across multiple regions
- Blockchain integration for immutable transaction records

### Hybrid LLM Security Core
- Enhanced analysis of repository content to identify code quality issues, security vulnerabilities, and technical debt
- Integration of AI models to provide suggestions for code improvements, refactoring, and optimization
- Version comparison to track changes over time
- Dependency graph showing how files and components relate to each other
- Multi-repository support for simultaneous import
- Blockchain integration for immutable repository records

This platform provides a scalable, secure, and maintainable foundation for modern software development.