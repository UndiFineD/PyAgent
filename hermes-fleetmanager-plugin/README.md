# Hermes FleetManager Plugin

This plugin adds a PostgreSQL-backed task queue and orchestration layer to Hermes.

It installs three pieces:

- the Hermes plugin in `fleetmanager/`
- the runtime agent assets in `.github/agents/`
- the orchestration helpers in `.github/agents/orchestration/`

## What it does

The runtime chain is:

1. A client such as Telegram creates an intent and queues tasks.
2. FleetManager reads pending tasks from PostgreSQL.
3. FleetManager dispatches the matching agent from `.github/agents/code/`.
4. Orchestration helpers assemble redacted context before any LLM fallback path.
5. Hermes keeps provider selection in its normal config flow, including OpenRouter and user-defined providers.

The plugin now preserves `provider`, `model`, `base_url`, and `api_mode` metadata in queued task payloads so downstream agents can respect the caller's provider choice.

## Install

Run the installer from the plugin root:

```bash
bash install.sh
```

The installer does the following:

- symlinks `fleetmanager/` into `~/plugins/`
- symlinks `fleetmanager/` into `~/.hermes/plugins/`
- copies `.github/` into `~/.github/`
- installs Python dependencies from `requirements.txt`
- installs PostgreSQL on Debian/Ubuntu systems if `psql` is missing
- creates a default PostgreSQL database and user
- updates `~/.hermes/.env` with the required database settings
- updates `~/.hermes/config.yaml` to use OpenRouter with the default model `nvidia/nemotron-3-super-120b-a12b:free`

Default database values:

- `POSTGRES_DB=hermes_fleetmanager`
- `POSTGRES_USER=hermes_fleetmanager`
- `POSTGRES_PASSWORD=hermes_fleetmanager`

You can override them before install:

```bash
export HERMES_FLEETMANAGER_DB=my_db
export HERMES_FLEETMANAGER_USER=my_user
export HERMES_FLEETMANAGER_PASSWORD=my_password
bash install.sh
```

## Enable the plugin

Add this to your Hermes config:

```yaml
plugins:
   fleetmanager:
      enabled: true
```

## Provider routing

Hermes resolves providers through `hermes_cli/providers.py` and `resolve_provider_full()`.

That means:

- OpenRouter is a first-class provider in Hermes.
- user-defined providers from `config.yaml` are supported through `resolve_user_provider()`
- FleetManager should not hardcode a provider
- queued tasks can carry `provider`, `model`, `base_url`, and `api_mode`, and the plugin now preserves those fields

If you want to force OpenRouter for a caller, include it in the queued task payload:

```json
{
   "provider": "openrouter",
   "model": "nvidia/nemotron-3-super-120b-a12b:free"
}
```

## Tools exposed by the plugin

- `fleetmanager_status` returns pending task count, visible tasks, and available agents.
- `fleetmanager_run` runs the orchestration fleet manager once.
- `fleetmanager_agents` lists installed code agents.

## Tests

Run the plugin test suite with:

```bash
./tests.sh
```

This runs:

- **ruff** — linting and import sorting
- **autopep8** — code formatting
- **black** — strict code formatting
- **flake8** — style checking
- **mypy** — static type checking
- **pyright** — language server type checking
- **pytest** — unit and integration tests

### Type Annotation Status

All Python files in the orchestration layer and agent code have been hardened with comprehensive type annotations:

**Orchestration Layer** (`.github/agents/orchestration/`):

- ✅ `backend.py` — PostgreSQL backend with typed DB helpers and Protocols
- ✅ `fleetmanager.py` — Task queue worker with full type coverage
- ✅ `intent_decomposer.py` — Intent DAG builder with typed parameters
- ✅ `rules.py`, `swarm.py`, `workflow.py`, `fleet.py` — All agent classes with `execute(task: dict[str, Any]) -> dict[str, Any]`
- ✅ `context_manager.py` — Context assembly with type-safe redaction
- ✅ `daemon.py` — Worker daemon with relative imports and fallback patterns
- ✅ `loader.py` — Agent module loader with safe type signatures

**Agent Code Layer** (`.github/agents/code/`):

- ✅ **100 agent files** — All agents now have:
  - `__init__(self) -> None` with `self.name: str` attribute
  - `execute(self, task: dict[str, Any]) -> dict[str, Any]` standardized signature
  - `fast_execute()` and `llm_execute()` with full return type annotations
  - Proper `from typing import Any` imports

**Recent Results**:
✅ 129 tests passed
✅ ruff: All checks passed
✅ autopep8: Code formatted
✅ black: 125 files checked
✅ flake8: No issues
✅ mypy: Success - no issues in 10 source files
✅ pyright: 0 errors, 4 non-critical warnings (about __all__ exports)

**Type Checking Strategy**:

- Module-level `TypeVar` and `Protocol` definitions for generic DB callbacks
- Explicit casting with `cast(dict[str, Any], ...)` at JSON/DB read boundaries
- Typed loops and local variables throughout
- Consistent agent class structure: `execute()` always takes `task: dict[str, Any]` and returns `dict[str, Any]`

Current tests cover:

- safe module loading
- database queue behavior
- task metadata preservation for `agent` and `provider`
- context redaction
- installer shell syntax

## Development notes

- `.github/agents/code/` contains the executable agent modules.
- `.github/agents/orchestration/` contains queue, daemon, context, and rules helpers.
- `fleetmanager/__init__.py` is the Hermes plugin entrypoint.
- `install.sh` is the supported install path for local setup.

## Detailed Orchestration Workflow

This describes the end-to-end flow from an external client (for example, Telegram) down to the LLM provider.
Each step includes the component(s) that participate and where the router/provider metadata is preserved.

- **Client / Gateway (Telegram)**:
    an incoming message or slash command is handled by your messaging gateway (e.g., the Telegram adapter).
    The gateway converts the message into an intent and calls the Hermes intent decomposer or queues a task directly.
  - Relevant code: your gateway adapter and the Hermes CLI/gateway layer in the main Hermes repo.

- **Intent Decomposer**:
    receives the intent and splits it into one or more atomic tasks.
    The decomposer normalizes the task payload and merges caller-supplied routing metadata (`provider`, `model`, `base_url`, `api_mode`) into the payload JSON before persisting.
  - Relevant file: [.github/agents/orchestration/intent_decomposer.py](.github/agents/orchestration/intent_decomposer.py)

- **Task Queue (DB / File fallback)**:
    tasks are persisted to PostgreSQL (preferred) or into a file-backed queue.
    The queued payload carries the merged routing metadata.
    Claiming is done with `SELECT ... FOR UPDATE SKIP LOCKED` to avoid races.
  - Relevant file: [.github/agents/orchestration/backend.py](.github/agents/orchestration/backend.py)

- **FleetManager Dispatcher**:
    FleetManager polls the queue (or is triggered) and resolves the agent to run.
    It preserves the `provider` metadata from the task payload and includes it when invoking the agent runtime.
    If an agent is matched, FleetManager dispatches to a Fleet or directly to a Worker/Swarm node depending on configuration.
  - Relevant file: [fleetmanager/__init__.py](fleetmanager/__init__.py)

- **Fleet & Swarm**:
    A Fleet is a logical grouping of worker processes;
    a Swarm is the execution surface (local threads/processes or remote workers).
    The dispatcher allocates the task to a Swarm worker which loads the agent module and executes it.
  - Relevant files: [.github/agents/orchestration/daemon.py](.github/agents/orchestration/daemon.py) and the worker launcher in `.github/agents/code/`.

- **Workflow & Agents**:
    The agent code (in `.github/agents/code/` or registered plugins) receives the task payload (with preserved provider routing).
    Agents implement domain logic and may either call an LLM provider directly or use Hermes' provider
    resolution helpers to call the chosen provider.
  - Agent loader: [.github/agents/orchestration/loader.py](.github/agents/orchestration/loader.py)

- **Rules & Decision Layer**:
    Some agents consult local rule sets or a rules engine (policy checks, rate limits, safety) before calling external models.
    The rules layer can also modify which provider/model to pick (if permitted by policy).
  - Rule helpers: `.github/agents/orchestration/rules.py` (if present) and inline rule checks in agent code.

- **Context Assembly**:
    Before any LLM call, orchestration helpers assemble the conversation context and run redaction to strip secrets or sensitive tokens.
    The context manager ensures the payload is safe to send to third-party models.
  - Relevant file: [.github/agents/orchestration/context_manager.py](.github/agents/orchestration/context_manager.py)

- **Provider Call (Pipelines: Hermes provider abstraction)**:
    The agent either calls the provider directly using the preserved `provider`/`model`/`base_url`/`api_mode`
    in the task payload, or it calls Hermes' provider resolution helpers which merge task-level overrides with system/user defaults.
  - Provider resolution: Hermes core (resolve_provider_full / hermes_cli providers)
  - The plugin preserves routing metadata in queued tasks so downstream calls always see the caller's intent.

Important notes:

- Provider metadata is intentionally kept inside the task payload JSON so it travels with the task across the DB boundary.
  This avoids losing caller intent when agent selection is performed separately from the payload content.
- The context manager performs defensive redaction; do not rely on it as the only secret-control mechanism
  — sensitive data should be filtered before queueing when possible.
- If you want gateway-level defaults (for example, always prefer a particular provider for Telegram callers),
  add a small wrapper in the gateway that injects `provider`/`model` into the task payload before calling the decomposer.

If you want, I can also add a diagram (Mermaid) showing this flow and add integration test suggestions for end-to-end DB-backed runs.
