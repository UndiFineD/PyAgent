# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# FLM (Fastflow Language Model) Architecture Design

## Overview
In this repository, **FLM means Fastflow Language Model**: a local, OpenAI-compatible model server optimized for **NPU-backed inference**, similar in usage pattern to Ollama.

The current integration pattern (see `flm-test-llama.py`) uses:
- OpenAI client SDK
- `base_url="http://127.0.0.1:52625/v1/"`
- local API key placeholder (`"dummy"`)
- chat-completions contract
- optional tool-calls loop

This design treats FLM as an infrastructure/runtime provider and PyAgent as the orchestration layer.

## Scope and Non-Goals

### In Scope
- FLM endpoint integration for chat completions
- model selection and request settings (example model: `llama3.2:1b`)
- tool-call handshake compatibility
- health and availability checks for local runtime
- NPU-oriented operational assumptions (low latency local serving)

### Out of Scope
- training or fine-tuning model weights
- custom tokenizer/model architecture design
- replacing OpenAI client SDK contract in application code

## Core Components

### 1. FLM Runtime (External Process)
Local Fastflow server responsible for hosting and serving models with NPU optimization. Exposes OpenAI-compatible HTTP API surface.

### 2. OpenAI-Compatible Client Adapter
PyAgent-side integration that uses `openai.OpenAI(...)` pointed to FLM base URL.

### 3. Conversation State Manager
Maintains `messages` list in OpenAI schema (`system`, `user`, `assistant`, `tool` roles), preserving turn history and tool-call continuity.

### 4. Tool-Call Bridge
Processes tool-calls returned by FLM, appends assistant/tool messages, and re-invokes completion until final assistant answer is produced.

### 5. Runtime Safety and Diagnostics
Handles endpoint unavailability, malformed payloads, model-not-found cases, and logs request/response metadata for troubleshooting.

## Request/Response Contract (Observed)

1. Client sends chat completion request with:
	- `model` (example: `llama3.2:1b`)
	- `messages`
	- `max_tokens`
2. If response contains `tool_calls`:
	- append assistant message including tool call payload
	- append tool result message(s)
	- repeat completion call
3. If no `tool_calls`:
	- treat assistant content as terminal answer
	- end loop

## Design Principles

- **OpenAI API compatibility first**: avoid custom protocol lock-in.
- **Local-first reliability**: FLM integration must work without cloud dependencies.
- **NPU-aware performance**: prefer low-overhead local serving and short request path.
- **Deterministic tool-call loop**: explicit, testable turn transitions.
- **Operational clarity**: clear endpoint, model, timeout, and failure logging.

## Failure Handling Strategy

- **Connection errors**: surface actionable message (endpoint + model + timeout).
- **Model missing**: return clear error with selected model name.
- **Invalid tool-call payload**: skip/guard malformed calls and log structured diagnostics.
- **Infinite loop prevention**: enforce max tool-call iterations per request.

## Security Considerations

- FLM is local-network by default; avoid exposing runtime without access controls.
- Keep API key handling compatible with OpenAI client; allow dummy/local key where runtime permits.
- Never persist sensitive prompt/response content without explicit retention policy.

## Integration Notes for PyAgent

- Treat FLM as another provider peer to Ollama-like local runtimes.
- Keep provider config centralized (base URL, model defaults, timeout, retries).
- Reuse existing transaction/logging patterns for auditability.

## Future Enhancements

- Dynamic model capability probe (`/models`) and auto-selection.
- Streaming support path for long outputs.
- Health-check gate before first inference.
- Provider fallback chain (FLM → Ollama → cloud provider) when configured.