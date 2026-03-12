# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Transport Layer Design

The `src/transport` package is intended to abstract communication channels
between agents, external services, and the outside world.  Although currently
empty in the `src` tree, the legacy code likely contained implementations for
HTTP, WebSocket, and CLI transports.

## Design Objectives

- **Unified interface** for sending and receiving messages regardless of
  protocol (HTTP, WebSocket, gRPC, local pipes).
- **Pluggable adapters** so new protocols can be added without touching core
  logic.
- **Security features** including authentication, encryption, rate limiting,
  and replay prevention.
- **Resilience** with automatic reconnection, heartbeat messages, and
  backoff strategies.

## Legacy Clues

The presence of `transport/__init__.py` in `src/transport` and earlier comments
in the todo list point to a planned skeletal implementation.  We should
consult `src-old` for any transport‑related modules (for example,
`agent_transport`, `MSGraphTransport`, etc.) and extract their docstrings when
refactoring.

## Brainstorm Ideas

- A `TransportManager` that selects the appropriate adapter based on
  configuration and destination URL.
- Support for local `multiprocessing.Queue` or `zmq` for intra-process
  communication within a swarm node.
- Metrics collection: bytes sent/received, errors, latency per transport.
- Simulation mode for offline testing where transport requests are recorded
  and replayed.

*Look for `Transport` classes in `src-old` to reuse descriptions.*