# Observability & Data Stack

The Observability layer (`src/observability/`) acts as the "Nervous System" of the PyAgent swarm, providing real-time telemetry, audit logs, and performance metrics.

## 📡 Live Telemetry
- **Prometheus/Grafana Integration**: Exporting fine-grained metrics including:
  - Tokens-per-second (TPS) per agent/node.
  - P2P message latency (mDNS vs. Static).
  - Memory pressure and cache hit rates.
- **Node Health**: Heartbeat monitoring across the Voyager P2P network.

## 🪵 Audit & Traceability
- **CascadeContext Tracking**: Every task carries a unique ID and parent ID, allowing for full recursion depth visualization and "attribution analysis" in multi-agent loops.
- **Log Sharding**: Active logs are sharded by Agent Session to ensure high-speed writing without I/O contention.

## 🧪 Simulation & Benchmarking
- **Shadow Mode**: Agents can run in "Shadow Mode," performing actions alongside production agents without executing side effects, providing a safe playground for testing new logic cores.
- **Deterministic Replay**: Ability to replay a session from log files to debug exact failure points in complex swarm behavior.

## 💾 Agent Memory & Persistence
- **Redis Cache**: High-speed ephemeral storage for cross-agent signaling (Wait/Stop/Pause).
- **Relational Backend (SQLAlchemy)**: Structured storage for:
  - `weights_registry`: Performance history of logic cores and agents.
  - `agent_knowledge_index`: Vector-search based retrieval for long-term agent memory.
- **S3/Local Artifacts**: Storage for large files generated during tasks (Logs, Benchmarks, Snapshots).

## 🛡️ Governance & Quality
- **Automated Red-Teaming**: Periodic scheduling of stress tests via `RedTeamCore`.
- **Linter Service**: Automated code quality checks on generated artifacts using Pylint and Flake8 within the sandbox.

---
*If you can't measure it, you can't evolve it.*
