# Design: Desktop-Like Streaming Website (Web + Backend)

## Overview
This design document describes how to structure and implement a **desktop-like streaming website** for the PyAgent project, aligned with the existing repo layout and technology mix (Rust + Python + existing JS frontend). It includes where to place the code, what packages & frameworks to adopt, and a recommended architecture that balances performance, maintainability, and developer velocity.

---

## 1) Current baseline (existing code in `web/`)

The repo already contains a `web/` directory with:
- A React + Vite frontend (`App.tsx`, `index.tsx`, `vite.config.ts`)
- A Node.js backend stub under `web/backend/` (currently a Google Vertex AI proxy pattern)
- A `package.json` listing core frontend dependencies (React, Vite, Tailwind helpers, etc.)

That is already a working “desktop-like web app” scaffold.

---

## 2) Desired final structure (recommended)

### Top-level layout

```
./
├── web/                    # frontend + lightweight backend (Node/TS) or static UI
├── backend/                # production-grade backend (Rust + optional Python)
├── rust_core/              # performance-critical Rust core (existing)
├── src/                    # Python core agent runtime (existing)
├── docs/                   # documentation
├── .github/                # CI + design docs
└── ...
```

### Why this layout?
- **`web/`** keeps the UI fast to iterate on and able to run locally with `npm run dev`.
- **`backend/`** separates server concerns from the UI and allows swapping between 
  - a **Rust backend** (recommended for streaming & performance), and
  - a **Python shim** (for rapid integration with existing PyAgent logic).
- **`rust_core/`** stays focused on compute-heavy workloads (LLM inference, token math), and can be called by the backend via a Rust library API or via a local process boundary.

---

## 3) Proposed architecture (web + backend + core)

### 3.1 Frontend (UI) — `web/`
**Goal:** Desktop-like UI + streaming media display + realtime controls.

#### Tech stack
- **Framework:** React (existing) or Svelte (optional), using Vite.
- **UI:** Tailwind + `clsx` for styling, `lucide-react` icons, `recharts` for charts.
- **Media & streaming:**
  - WebRTC (preferred for low-latency audio/video streaming).
  - WebSocket for control signals (start/stop stream, agent input updates).

#### Packages (existing + recommended additions)
- `react`, `react-dom` (core UI)
- `vite`, `typescript`, `@vitejs/plugin-react` (build tooling)
- `lucide-react`, `clsx`, `tailwind-merge` (UI components)
- **Add (as needed):**
  - `@reduxjs/toolkit` / `zustand` (state management)
  - `@microsoft/signalr` or `socket.io-client` (websocket signal layer)
  - `simple-peer` or `webrtc-adapter` (WebRTC helper)

### 3.2 Backend (API + streaming orchestration) - `./backend/`
**Goal:** Host an API + WebRTC/WS streaming endpoint(s) that connect browser sessions to PyAgent and run as a worker within the core runtime.

#### Option A: Rust-first backend (recommended)
- **Framework:** `axum` or `actix-web` (async, fast, Rust-native)
- **Runtime:** `tokio`
- **Streaming/RTC:** `webrtc-rs` (Rust WebRTC), or integration with an external SFU (`mediasoup`, `janus`) via HTTP/WS.

**Core responsibilities:**
- Accept browser WebRTC offers and return answers.
- Relay agent events (text/audio) between browser and PyAgent runtime.
- Provide a REST API for configuration / auth / status.

#### Python backend (lighter integration path)
- **Framework:** FastAPI (async, websockets, simple)
- **Streaming-facing layer:** `aiortc` (WebRTC) + `uvicorn` (ASGI server)

This can be a thin wrapper that calls the Rust core via FFI or via an IPC socket.

##### Key Python packages (in `backend/requirements.txt`)
- `fastapi`, `uvicorn[standard]` (web server)
- `aiortc` (WebRTC)
- `httpx` (API requests)
- `pydantic` (schema validation)

---

## 4) LLM-friendly interface features (AI control, typing, voice, webcam)

### 4.1 AI control & command model (autonomous operation)
The UI and backend should support **AI-driven actions** where the model can issue commands that affect the UI/workflow and run tasks without manual click-throughs.

#### 4.1.1 Action model
- The frontend exposes a small **action registry** of allowed actions (e.g., open window, run task, navigate, open file, capture screenshot).
- The backend (or agent runtime) can emit **`actionRequest`** messages to the frontend.
- The frontend validates action requests against the registry and executes them if allowed.

#### 4.1.2 Trust/consent
- For “trusted automation” mode, the UI can run actions immediately.
- For less-trusted flows, require user confirmation (modal prompt) before executing.
- Actions are logged so the user can audit what the AI did.

### 4.2 WebSocket message schema (control + streaming)
A single WebSocket connection carries both control messages and streaming results.

#### Client→Backend
- `init` — session negotiation
- `runTask` — start a new LLM task (text generation, code generation, etc.)
- `control` — pause/resume/cancel tasks
- `speechTranscript` — voice input text from Web Speech API

#### Backend→Client
- `taskStarted` — acknowledgment
- `taskDelta` — streaming partial output (token-level, incremental)
- `taskComplete` — final result
- `taskError` — error reporting
- `actionRequest` — ask the UI to execute a command (open window, click button, etc.)

> This model enables the UI to show **live typing** (each `taskDelta` can be rendered character-by-character) and to handle **autonomous AI actions** safely.

### 4.3 Typing indicator (user + AI)
- **AI typing**: display a “AI is typing…” indicator when `taskDelta` events arrive.
- **User typing**: UI can show local typing feedback (e.g., “You are typing…”) and send a `typing` signal over WebSocket for collaborative flows.

### 4.4 Voice input (Web Speech API)
- Use the **browser Web Speech API** for microphone capture and speech-to-text.
- Send transcripts to the backend via `speechTranscript` messages.
- Support a “push-to-talk” UI element and a mic mute/unmute state.

### 4.5 Webcam + video conferencing
- Use **WebRTC** for peer-to-peer (P2P) video conferencing between users.
- The backend acts as a **signaling server** (via WebSocket) to exchange SDP offers/answers and ICE candidates.
- The UI should include a “camera toggle” control, local preview, and remote video grid.

---

## 5) Dependency / package strategy (what to install and why)

### Frontend packages (JS/TS)
- **`react` / `react-dom`** — UI rendering
- **`vite` / `typescript`** — fast bundler + type safety
- **`tailwindcss` / `tailwind-merge`** — styling + class merging
- **`lucide-react`** — icon library
- **`recharts`** — charting for dashboard-style UI

### Backend packages (Rust)
- **`axum` / `actix-web`** — web server and routing.
- **`tokio`** — async runtime for web and streaming.
- **`webrtc-rs`** (or similar) — handle WebRTC signaling and media.
- **`serde`** — JSON (API payloads).
- **`anyhow`** / `thiserror` — ergonomic error handling.
- **`tracing`** — logging/observability.

### Backend packages (Python)**
- **`fastapi`** — API framework.
- **`uvicorn`** — ASGI server.
- **`aiortc`** — WebRTC.
- **`pydantic`** — request validation.
- **`httpx`** — HTTP client for internal calls.

---

## 5) Where to put the design document

Created here: `brainstorm.md

If you'd like, I can also add:
- a **scaffolded starter** in `web/` and `backend/` (with `package.json`, `Cargo.toml`, example entrypoints)
- updated CI/Dev scripts for `npm install`, `cargo build`, and `pytest` for the new web stack
- a small “integration glue” module showing how the frontend talks to the backend via WebRTC/WebSocket using the PyAgent runtime.

---

### Next question for you
Should the backend be: 
1) **Rust-first** (high performance, keeps repo aligned to existing Rust core), or 
2) **Python-first** (easier integration with existing PyAgent runtime and fewer new languages to maintain)?
