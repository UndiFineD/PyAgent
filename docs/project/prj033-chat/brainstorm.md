# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Chat Subsystem Design

The `src/chat` package will encapsulate the conversational interfaces and
chat-related utilities used by the project.  Although the current `src`
directory contains only the placeholder `chat` package, the legacy code set
included tests such as `tests/test_chat_*`, indicating an existing chat
architecture.

## High-level Goals

- **Message abstraction** that standardizes prompts, responses, function calls,
  and tool invocations across different LLM backends.
- **Session management** to track user-agent conversations, context windows,
  and memory integration.
- **Plugin hooks** for custom message preprocessing (e.g. profanity filters,
  translation services) before dispatch to an LLM.
- **Gateway adapters** for multiple chat APIs (OpenAI, Anthropic, Gemini,
  local LLMs via Ollama, etc.).

## Legacy Clues

- The repository contains a sample script `flm-test-llama.py` demonstrating
  chat completion usage with an LLM client, suggesting the design supports
  pluggable backends.
- The CI workflow file runs `pytest tests/test_chat_*`, confirming the
  presence of chat-specific tests in earlier versions.

## Brainstorm Topics

- Unified schema for chat messages (role, content, metadata, tool calls).
- Conversation storage and retrieval across sessions.
- Support for rich media (images, audio) in chat.
- Rate‑limiting and backoff for high-volume chat workloads.
- UI considerations for multi-turn chat when integrated with the Web GUI.

*Example content re‑used from `flm-test-llama.py` and test files.*