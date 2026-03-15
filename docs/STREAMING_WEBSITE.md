# Desktop-like Streaming Website (Frontend + Backend)

This document describes where to place and how to organize the **user-facing streaming website** for the PyAgent project, along with recommended technologies and architecture patterns.

---

## 📍 Where to keep it in this repo

### Recommended location
- **Frontend (UI)**: `web/` or `frontend/` at the repository root
- **Backend (API / streaming orchestration)**: `backend/` at the root

This keeps the website code separate from `src/` (PyAgent core) and `rust_core/` (performance-critical Rust core), while still enabling a monorepo workflow.

Example structure:

```
./
├── backend/              # API + streaming worker (Rust/Python)
├── web/                  # Desktop-like web UI (React/Vite)
├── rust_core/            # Rust performance core (existing)
├── src/                  # PyAgent Python core (existing)
├── docs/                 # Documentation (this file lives here)
└── ...
```

---

## 🧩 Recommended tech stack

### 1) Frontend (user-facing UI) — **JavaScript / TypeScript**
**Why**: Browsers run JS/TS natively, and modern frameworks make desktop-like UX easy.

- **Framework**: React / Next.js, Vue, or Svelte (React is most common for desktop-style apps)
- **UI**: Component library (Tailwind + shadcn, Radix, MUI, or Chakra)
- **Streaming**: Use **WebRTC** (for real-time low-latency streaming) and/or **WebSockets** (for control + events)
- **Build tooling**: Vite, Next.js, or webpack (Vite is fast and recommended)

📦 Example folder: `web/`

---

### 2) Backend (streaming orchestration + API)

#### Option A — Python backend (fast iteration)
- **Framework**: FastAPI (async, websockets, simple routing)
- **Streaming layer**: aiortc / WebRTC server, or a dedicated media server (e.g., Janus, mediasoup) behind the API
- **Why**: Fast to build, lots of ecosystem libraries, integrates with existing PyAgent Python code.

📦 Example folder: `backend/` or `api/`

#### Option B — Rust backend (highest performance)
- **Framework**: Axum, Actix Web, or Warp
- **Streaming**: `webrtc-rs`, `libwebrtc`, or Rust bindings to media servers
- **Why**: Best for CPU-heavy streaming, low-latency media pipelines, and safe concurrent handling.

📦 Example folder: `backend/` or `api/`

---

## 🧠 How it ties into PyAgent

- **`rust_core/`** stays focused on compute-heavy/algorithmic code (inference, tokenization, performance kernels).
- **`src/`** stays focused on the PyAgent runtime, orchestration, and agent logic.
- **`web/`** becomes the user-facing UI layer that talks to PyAgent via **HTTP/WebSocket/WebRTC**.
- **`backend/`** (if used) can either be a thin proxy that forwards streaming events to the PyAgent runtime or a full streaming orchestrator.

---

## ✅ Quick-start directory blueprint

Create the following folders (example):

- `web/` (frontend)
  - `web/src/`
  - `web/public/`
  - `web/package.json`

- `backend/` (API, optional)
  - `backend/app.py` (FastAPI) or `backend/src/main.rs` (Rust)
  - `backend/requirements.txt` or `backend/Cargo.toml`

- `docs/STREAMING_WEBSITE.md` (this file)

---

## 🎯 Goals for the streaming website

1. **Desktop-like UI**: smooth navigation, responsive layout, keyboard shortcuts, true app feel.
2. **Low-latency streaming**: use WebRTC or well-optimized websocket pipelines.
3. **Scalable backend**: separate streaming logic from core agent logic; keep PyAgent as the “brain”.
4. **Maintainable architecture**: keep UI, API, and core separate so each can evolve independently.

---

If you want, I can also propose a concrete minimal scaffold (folder + config + example code) for `web/` + `backend/` in this repo.