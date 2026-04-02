# standards-commit-style

**Project ID:** `prj0000031`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

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

## Status

0 of 9 tasks completed

## Code detection

- Code detected in:
  - `tests\security\test_pre_commit_secret_hook.py`
  - `tests\test_precommit.py`