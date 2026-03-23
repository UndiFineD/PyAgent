# Prj0000031 Streaming Website

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-06-13_

## Goal

Deliver a desktop-like streaming website for PyAgent: a React+Vite frontend
connected to a Rust/Python backend via WebSocket and optional WebRTC.
The result is a browser-based UI that streams agent output token-by-token and
supports voice input, webcam, and AI-driven UI actions.

## Architecture

- **`web/`** — React+Vite frontend (existing scaffold), extended with streaming
  and media controls.
- **`backend/`** — Rust-first (axum/tokio) or Python (FastAPI+aiortc) backend
  that relays agent events and handles WebRTC signalling.
- **`rust_core/`** — remains the performance-critical layer; called by the
  backend for token math and LLM inference.

## Tasks

- [ ] Define WebSocket message schema (`init`, `runTask`, `taskDelta`, `taskComplete`, `actionRequest`)
- [ ] Implement backend WebSocket endpoint (Rust axum or Python FastAPI)
- [ ] Implement frontend streaming renderer (token-by-token `taskDelta` display)
- [ ] Add voice input via Web Speech API → `speechTranscript` message
- [ ] Add WebRTC signalling endpoint and browser peer connection
- [ ] Add AI action registry on the frontend (trusted automation mode)
- [ ] Wire webcam capture and remote video grid
- [ ] Add CI smoke test for the backend WebSocket endpoint
- [ ] Document setup in `docs/setup.md` (npm install, cargo build, run locally)

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Message schema defined | T1 | NOT_STARTED |
| M2 | Backend endpoint live | T2 | NOT_STARTED |
| M3 | Streaming UI rendering | T3 | NOT_STARTED |
| M4 | Voice + WebRTC enabled | T4, T5, T7 | NOT_STARTED |
| M5 | AI action model ready | T6 | NOT_STARTED |
| M6 | CI + docs complete | T8, T9 | NOT_STARTED |
