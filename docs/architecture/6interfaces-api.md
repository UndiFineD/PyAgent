# 6 - Interface and API Architecture

This document describes stable integration surfaces between agents, backend APIs, and UI layers.

## Interface layers

- Agent interface: task contracts and handoff artifacts.
- Backend interface: FastAPI REST and WebSocket endpoints.
- Frontend interface: Vite/React presentation and operator workflows.
- Tool interface: controlled command and file operations.

## Agent handoff contract

Each lifecycle phase produces a concrete artifact that becomes the input to the next phase.

- think -> design -> plan -> test -> code -> exec -> ql -> git

Artifacts must be:

- deterministic enough for downstream validation
- scope-bounded to a project ID
- linked to acceptance criteria

## Backend API expectations

- API responses should be machine-parseable and stable.
- Errors must include enough context for retries and triage.
- Long-running operations should provide progress visibility.

## WebSocket expectations

- Reconnect logic must be resilient to transient network failures.
- Event payloads should be version-tolerant.
- Critical status changes must be durable and replayable.

## Versioning and compatibility

- Prefer additive changes for public API surfaces.
- Document breaking changes in release notes and migration docs.
- Keep endpoint and schema evolution explicit and reviewable.

## Validation

- API changes require contract-level tests.
- Integration tests must cover success, timeout, and failure paths.
