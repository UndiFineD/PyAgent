# PyAgent Improvement Research & Roadmap

## 🛡️ Core/Shell Architecture Design (Phase 114+)

To facilitate the migration of performance-critical logic to Rust, the codebase is being refactored into a **Core/Shell** pattern:

### 1. The Pure Logic Core (`*Core.py`)
- **Responsibility**: Pure computation, data transformation, regex parsing, score calculation.
- **Rules**:
  - No File I/O (cannot use `os`, `sqlite3`, `pathlib.read_text`, etc.).
  - No Network access.
  - No side effects.
  - Strictly typed.
- **Rust Readiness**: These files can be replaced by a compiled module without any changes to surrounding logic.

### 2. The I/O Shell (`Agent.py`, `Manager.py`, `Registry.py`, `Engine.py`)
- **Responsibility**: State management, File I/O, Database calls, Network requests.

## 🚀 Phase 115: Ecosystem Performance & Context Optimization

### 1. Native Acceleration Preparation
- **ContextCompressorCore (Target)**: Move AST parsing and regex summary logic to a pure core. This is a high-frequency operation during swarm cycles.
- **GlobalContextCore Audit**: Verify state-less logic for environment variable resolution and workspace scanning.

### 2. Strength in Typing
- **Refactoring Requirement**: All classes in `src/classes/context` and `src/classes/cognitive` must achieve 100% Type Hint coverage.
- **Null Safety**: Implementation of `Optional` guards for all dictionary lookups in core logic.

### 3. Memory Shard Efficiency
- **Shard Balancing**: Refine the Adler-32 sharding algorithm to ensure even distribution across 256 shards.
- **Fast Similarity Logic**: Extract similarity score calculation into `KnowledgeCore` for potential Rust `ndarray` acceleration.

## 🛡️ Security & Dependency Hardening (Patch 115.1)

### 1. urllib3 Vulnerability Mitigation
- **Upgrade**: Bumped `urllib3` to `2.6.3` to resolve high-severity vulnerabilities (#3, #4, #5, #6, #7).
- **Session Isolation**: Refactored all HTTP-capable agents (`WebAgent`, `SearchAgent`, `LLMClient`, `NotificationManager`, `RemoteAgentProxy`) to use `requests.Session` with strictly limited `max_redirects`.
- **Decompression Bomb Protection**: Implemented streaming size checks in `WebAgent` to abort downloads exceeding 10MB, preventing memory exhaustion from malicious compressed payloads.
- **Redirect Control**: Centralized redirect limits (max 2-10) to prevent unbounded decompression chains in web-crawling and remote proxy tasks.


### 🧠 AI Lessons Derived from Deep Shard Analysis (Phase 108)
- Intelligence Shard 27: 
- Intelligence Shard 29: 
- Intelligence Shard 102: 
- Intelligence Shard 114: Unknown failure
- Intelligence Shard 114: Unknown failure
- Intelligence Shard 146: 
- Intelligence Shard 199: 


## 🚀 Recent Autonomous Findings

### Latest Autonomous Scan (2026-01-09)
- **Files Scanned**: 840
- **Issues Identified**: 1
- **Autonomous Fixes**: 1
- **Stability Gate Status**: OPEN (Green)

#### Top Issues Discovered
- `src\classes\context\ContextCompressorCore.py`: 1 issues found.
