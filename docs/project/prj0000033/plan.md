# Prj0000033 Chat Subsystem

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-06-13_

## Goal

Build the `src/chat` package that encapsulates all conversational interfaces
and utilities: a unified message schema, session management, plugin hooks for
preprocessing, and gateway adapters for multiple LLM backends.

## Design Pillars

- **Message abstraction** — standardized schema for prompts, responses,
  function calls, and tool invocations across backends.
- **Session management** — track user-agent conversations, context windows,
  and memory integration.
- **Plugin hooks** — custom message pre/post-processing (e.g., profanity
  filters, translation) before dispatch to an LLM.
- **Backend adapters** — OpenAI, Anthropic, Gemini, Ollama (local LLM), and
  others via a common `ChatAdapter` interface.

## Tasks

- [ ] Define unified message schema (`role`, `content`, `metadata`, `tool_calls`)
- [ ] Implement `ChatSession` with context window tracking and memory integration
- [ ] Implement `ChatAdapter` ABC and adapters for OpenAI, Anthropic, Ollama
- [ ] Implement plugin hook pipeline (pre-dispatch, post-response)
- [ ] Add rate-limiting and exponential backoff for high-volume workloads
- [ ] Support rich media in messages (images, audio content blobs)
- [ ] Add conversation storage and retrieval (in-memory + optional persistent)
- [ ] Write tests: `tests/test_chat_session.py`, `tests/test_chat_adapters.py`
- [ ] Document `src/chat` design in `docs/architecture/`

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Message schema defined | T1 | NOT_STARTED |
| M2 | Session management live | T2, T7 | NOT_STARTED |
| M3 | Backend adapters working | T3 | NOT_STARTED |
| M4 | Plugin hooks and rate-limiting | T4, T5 | NOT_STARTED |
| M5 | Rich media + tests + docs | T6, T8, T9 | NOT_STARTED |
