# Backend Worker

The Python FastAPI backend worker for the PyAgent streaming UI. 
Manages WebSocket sessions between the NebulaOS browser frontend and the PyAgent runtime.

## Architecture

| File | Purpose |
|------|---------|
| `app.py` | FastAPI application — `/health` endpoint + `/ws` WebSocket endpoint |
| `session_manager.py` | Tracks active WebSocket connections keyed by UUID |
| `ws_handler.py` | Dispatches incoming messages to typed handlers; streams AI output |
| `models.py` | Pydantic schemas for all 10 client↔backend message types |
| `__main__.py` | Uvicorn entrypoint (`python -m backend`) |

## Endpoints

| Endpoint | Protocol | Description |
|----------|----------|-------------|
| `GET /health` | HTTP | Liveness probe — returns `{"status": "ok"}` |
| `ws://127.0.0.1:8000/ws` | WebSocket | Bidirectional streaming channel |

## Message Protocol

**Client → Backend**

| Type | Description |
|------|-------------|
| `init` | Register session UUID |
| `runTask` | Submit a task prompt for streaming execution |
| `control` | Send `cancel` to abort an in-progress task |
| `speechTranscript` | Push a voice transcript into the active task |
| `signal` | WebRTC signalling payload (offer/answer/candidate) |

**Backend → Client**

| Type | Description |
|------|-------------|
| `taskStarted` | Acknowledges `runTask`, echoes `taskId` |
| `taskDelta` | Streamed text chunk |
| `taskComplete` | Signals end of stream |
| `taskError` | Propagates runtime errors |
| `actionRequest` | Requests client-side action (e.g. open window) |

## Running

```powershell
# Install dependencies (first time)
pip install -r backend/requirements.txt

# Start the worker
python -m backend
# Listening on http://127.0.0.1:8000
```

The Vite dev server proxies `/ws` and `/api` to `http://127.0.0.1:8000` automatically 
— start both processes and open the NebulaOS frontend at `http://localhost:5173`.

## Tests

```powershell
python -m pytest tests/test_backend_worker.py tests/test_backend_models.py `
    tests/test_backend_session_manager.py tests/test_backend_ws_handler.py -v
```

