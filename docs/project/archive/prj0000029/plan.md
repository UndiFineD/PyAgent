# PyAgent LLM UI + Backend Worker — Implementation Plan

**Goal:** Build a Python FastAPI backend worker (embedded in the PyAgent runtime) 
that communicates with the existing React/Vite frontend over WebSocket, 
supporting real-time streaming, autonomous AI control, voice input, 
and WebRTC video conferencing signaling. 
The existing Node.js `web/backend/` proxy is retired and replaced.

**Architecture:**
- `backend/` — Python FastAPI + uvicorn + aiortc worker, embedded in PyAgent process
- `web/` — React + Vite frontend (existing NebulaOS UI) extended with WebSocket client, voice input, webcam/WebRTC UI
- `web/backend/` — retired (Node.js proxy removed; no longer used)
- WebSocket messages carry AI streaming deltas, control commands, and WebRTC signaling
- Action registry in the frontend validates and executes AI-driven UI commands

**Tech Stack:**
- Python: `fastapi`, `uvicorn[standard]`, `aiortc`, `pydantic`, `websockets`
- TypeScript/React: `socket.io-client` (or native WebSocket), `simple-peer` (WebRTC), `zustand` (state)
- Vite proxy: `/ws` → Python backend, `/api` → Python backend

---

## Task 1 — Set up `backend/` Python package

### Step 1: Create `backend/requirements.txt`
- File: `backend/requirements.txt`
- Content:
  ```
  fastapi>=0.115.0
  uvicorn[standard]>=0.34.0
  aiortc>=1.10.0
  pydantic>=2.10.0
  websockets>=14.0
  httpx>=0.28.0
  ```

### Step 2: Create `backend/__init__.py`
- File: `backend/__init__.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """PyAgent backend worker package."""
  ```

### Step 3: Verify package structure
- Command:
  ```powershell
  Get-ChildItem backend\ -Recurse | Select-Object FullName
  ```
- Expected output: `backend\__init__.py`, `backend\requirements.txt`

---

## Task 2 — Write failing test: backend package importable

### Step 1: Write the failing test
- File: `tests/test_backend_worker.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Tests for the backend worker package."""
  import importlib
  import pytest


  def test_backend_package_importable():
      mod = importlib.import_module("backend")
      assert mod is not None


  def test_backend_app_importable():
      mod = importlib.import_module("backend.app")
      assert hasattr(mod, "app")
  ```

### Step 2: Run test and verify failure
- Command:
  ```powershell
  pytest tests/test_backend_worker.py -v 2>&1
  ```
- Expected (before implementation):
  ```
  FAILED tests/test_backend_worker.py::test_backend_app_importable - ModuleNotFoundError
  ```

---

## Task 3 — Implement `backend/models.py` — WebSocket message schemas

### Step 1: Create `backend/models.py`
- File: `backend/models.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Pydantic models for WebSocket message schema."""
  from __future__ import annotations
  from typing import Any, Literal, Optional
  from pydantic import BaseModel


  # ── Client → Backend ────────────────────────────────────────────────────────

  class InitMessage(BaseModel):
      type: Literal["init"]
      session_id: str
      client_info: dict[str, Any] = {}


  class RunTaskMessage(BaseModel):
      type: Literal["runTask"]
      task_id: str
      task: str
      payload: dict[str, Any] = {}


  class ControlMessage(BaseModel):
      type: Literal["control"]
      task_id: str
      action: Literal["cancel", "pause", "resume"]


  class SpeechTranscriptMessage(BaseModel):
      type: Literal["speechTranscript"]
      task_id: Optional[str] = None
      transcript: str
      is_final: bool = True


  # WebRTC signaling (client→backend)
  class SignalMessage(BaseModel):
      type: Literal["signal"]
      session_id: str
      peer_id: str
      signal_type: Literal["offer", "answer", "ice"]
      payload: dict[str, Any]


  # ── Backend → Client ────────────────────────────────────────────────────────

  class TaskStartedMessage(BaseModel):
      type: Literal["taskStarted"] = "taskStarted"
      task_id: str
      started_at: str


  class TaskDeltaMessage(BaseModel):
      type: Literal["taskDelta"] = "taskDelta"
      task_id: str
      delta: str
      meta: dict[str, Any] = {}


  class TaskCompleteMessage(BaseModel):
      type: Literal["taskComplete"] = "taskComplete"
      task_id: str
      result: dict[str, Any]
      status: Literal["success", "error"] = "success"


  class TaskErrorMessage(BaseModel):
      type: Literal["taskError"] = "taskError"
      task_id: str
      error: str
      code: str = "UNKNOWN"


  class ActionRequestMessage(BaseModel):
      """AI-driven command: backend asks the UI to perform an action."""
      type: Literal["actionRequest"] = "actionRequest"
      action: str
      params: dict[str, Any] = {}
      task_id: Optional[str] = None
  ```

### Step 2: Write test for models
- File: `tests/test_backend_models.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Tests for WebSocket message schema models."""
  import pytest
  from backend.models import (
      InitMessage, RunTaskMessage, TaskDeltaMessage,
      ActionRequestMessage, SignalMessage,
  )


  def test_init_message_valid():
      msg = InitMessage(type="init", session_id="abc-123")
      assert msg.session_id == "abc-123"


  def test_run_task_message_valid():
      msg = RunTaskMessage(type="runTask", task_id="t1", task="generateText",
                          payload={"prompt": "hello"})
      assert msg.task == "generateText"


  def test_task_delta_message_valid():
      msg = TaskDeltaMessage(task_id="t1", delta="hello ")
      assert msg.type == "taskDelta"


  def test_action_request_message_valid():
      msg = ActionRequestMessage(action="openWindow", params={"appId": "editor"})
      assert msg.action == "openWindow"


  def test_signal_message_valid():
      msg = SignalMessage(
          type="signal", session_id="s1", peer_id="p1",
          signal_type="offer", payload={"sdp": "..."}
      )
      assert msg.signal_type == "offer"
  ```

### Step 3: Run model tests (verify they fail before implementation, pass after)
- Command:
  ```powershell
  pytest tests/test_backend_models.py -v 2>&1
  ```
- Expected after implementation:
  ```
  PASSED tests/test_backend_models.py::test_init_message_valid
  PASSED tests/test_backend_models.py::test_run_task_message_valid
  PASSED tests/test_backend_models.py::test_task_delta_message_valid
  PASSED tests/test_backend_models.py::test_action_request_message_valid
  PASSED tests/test_backend_models.py::test_signal_message_valid
  ```

---

## Task 4 — Implement `backend/app.py` — FastAPI app + WebSocket endpoint

### Step 1: Create `backend/app.py`
- File: `backend/app.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """FastAPI backend worker — WebSocket + signaling endpoints."""
  from __future__ import annotations
  import asyncio
  import json
  import logging
  from typing import Any
  from fastapi import FastAPI, WebSocket, WebSocketDisconnect
  from fastapi.middleware.cors import CORSMiddleware
  from .session_manager import SessionManager
  from .ws_handler import handle_message

  logger = logging.getLogger(__name__)

  app = FastAPI(title="PyAgent Backend Worker", version="0.1.0")

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:5173", "http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

  sessions = SessionManager()


  @app.get("/health")
  async def health() -> dict[str, str]:
      return {"status": "ok"}


  @app.websocket("/ws")
  async def websocket_endpoint(websocket: WebSocket) -> None:
      session_id = await sessions.connect(websocket)
      logger.info("WebSocket connected: %s", session_id)
      try:
          while True:
              raw = await websocket.receive_text()
              try:
                  data = json.loads(raw)
              except json.JSONDecodeError:
                  await websocket.send_text(
                      json.dumps({"type": "error", "error": "Invalid JSON"})
                  )
                  continue
              await handle_message(sessions, session_id, websocket, data)
      except WebSocketDisconnect:
          logger.info("WebSocket disconnected: %s", session_id)
          sessions.disconnect(session_id)
  ```

### Step 2: Run test to verify app is importable
- Command:
  ```powershell
  pytest tests/test_backend_worker.py::test_backend_app_importable -v 2>&1
  ```
- Expected after all task 4 files are written:
  ```
  PASSED tests/test_backend_worker.py::test_backend_app_importable
  ```

---

## Task 5 — Implement `backend/session_manager.py`

### Step 1: Create `backend/session_manager.py`
- File: `backend/session_manager.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Manages active WebSocket sessions."""
  from __future__ import annotations
  import uuid
  from fastapi import WebSocket


  class SessionManager:
      def __init__(self) -> None:
          self._sessions: dict[str, WebSocket] = {}

      async def connect(self, websocket: WebSocket) -> str:
          await websocket.accept()
          session_id = str(uuid.uuid4())
          self._sessions[session_id] = websocket
          return session_id

      def disconnect(self, session_id: str) -> None:
          self._sessions.pop(session_id, None)

      def get(self, session_id: str) -> WebSocket | None:
          return self._sessions.get(session_id)

      def all_sessions(self) -> dict[str, WebSocket]:
          return dict(self._sessions)
  ```

### Step 2: Write test for session manager
- File: `tests/test_backend_session_manager.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Tests for SessionManager."""
  import pytest
  from unittest.mock import AsyncMock
  from backend.session_manager import SessionManager


  @pytest.mark.asyncio
  async def test_connect_returns_session_id():
      manager = SessionManager()
      ws = AsyncMock()
      session_id = await manager.connect(ws)
      assert isinstance(session_id, str)
      assert len(session_id) > 0
      ws.accept.assert_awaited_once()


  @pytest.mark.asyncio
  async def test_disconnect_removes_session():
      manager = SessionManager()
      ws = AsyncMock()
      session_id = await manager.connect(ws)
      manager.disconnect(session_id)
      assert manager.get(session_id) is None


  def test_disconnect_nonexistent_session_is_safe():
      manager = SessionManager()
      manager.disconnect("does-not-exist")  # should not raise
  ```

### Step 3: Run test
- Command:
  ```powershell
  pytest tests/test_backend_session_manager.py -v 2>&1
  ```
- Expected:
  ```
  PASSED tests/test_backend_session_manager.py::test_connect_returns_session_id
  PASSED tests/test_backend_session_manager.py::test_disconnect_removes_session
  PASSED tests/test_backend_session_manager.py::test_disconnect_nonexistent_session_is_safe
  ```

---

## Task 6 — Implement `backend/ws_handler.py` — message dispatch + AI streaming

### Step 1: Create `backend/ws_handler.py`
- File: `backend/ws_handler.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Dispatches WebSocket messages to the appropriate handler."""
  from __future__ import annotations
  import asyncio
  import json
  import logging
  from datetime import datetime, timezone
  from typing import Any
  from fastapi import WebSocket
  from .session_manager import SessionManager
  from .models import (
      TaskStartedMessage, TaskDeltaMessage,
      TaskCompleteMessage, TaskErrorMessage,
  )

  logger = logging.getLogger(__name__)


  async def handle_message(
      sessions: SessionManager,
      session_id: str,
      websocket: WebSocket,
      data: dict[str, Any],
  ) -> None:
      msg_type = data.get("type")
      if msg_type == "init":
          await websocket.send_text(json.dumps({
              "type": "initAck",
              "session_id": session_id,
              "server_version": "0.1.0",
          }))
      elif msg_type == "runTask":
          await _handle_run_task(websocket, data)
      elif msg_type == "control":
          await _handle_control(websocket, data)
      elif msg_type == "speechTranscript":
          await _handle_speech(websocket, data)
      elif msg_type == "signal":
          await _handle_signal(sessions, session_id, data)
      else:
          await websocket.send_text(json.dumps({
              "type": "error",
              "error": f"Unknown message type: {msg_type}",
          }))


  async def _handle_run_task(websocket: WebSocket, data: dict[str, Any]) -> None:
      task_id = data.get("task_id", "unknown")
      now = datetime.now(timezone.utc).isoformat()

      # Acknowledge start
      await websocket.send_text(TaskStartedMessage(
          task_id=task_id, started_at=now
      ).model_dump_json())

      # Stream partial results (placeholder — wire to PyAgent core in later tasks)
      sample_tokens = ["Hello", " from", " PyAgent", " backend", "!"]
      for token in sample_tokens:
          await asyncio.sleep(0.05)
          await websocket.send_text(TaskDeltaMessage(
              task_id=task_id, delta=token
          ).model_dump_json())

      # Complete
      await websocket.send_text(TaskCompleteMessage(
          task_id=task_id,
          result={"text": "".join(sample_tokens)},
          status="success",
      ).model_dump_json())


  async def _handle_control(websocket: WebSocket, data: dict[str, Any]) -> None:
      task_id = data.get("task_id", "unknown")
      action = data.get("action", "cancel")
      logger.info("Control action '%s' for task %s", action, task_id)
      await websocket.send_text(json.dumps({
          "type": "controlAck", "task_id": task_id, "action": action,
      }))


  async def _handle_speech(websocket: WebSocket, data: dict[str, Any]) -> None:
      transcript = data.get("transcript", "")
      logger.info("Speech transcript received: %s", transcript[:80])
      # Forward to AI as a runTask (route transcript as a prompt)
      await _handle_run_task(websocket, {
          "task_id": data.get("task_id", "speech"),
          "task": "generateText",
          "payload": {"prompt": transcript},
      })


  async def _handle_signal(
      sessions: SessionManager,
      sender_id: str,
      data: dict[str, Any],
  ) -> None:
      """Relay WebRTC signaling messages between peers."""
      peer_id = data.get("peer_id")
      peer_ws = sessions.get(peer_id) if peer_id else None
      if peer_ws:
          relay = {**data, "from_peer_id": sender_id}
          await peer_ws.send_text(json.dumps(relay))
      else:
          logger.warning("Signal relay: peer %s not found", peer_id)
  ```

### Step 2: Write test for ws_handler dispatch
- File: `tests/test_backend_ws_handler.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Tests for WebSocket message handler dispatch."""
  import json
  import pytest
  from unittest.mock import AsyncMock, MagicMock
  from backend.session_manager import SessionManager
  from backend.ws_handler import handle_message


  @pytest.fixture
  def ws():
      mock = AsyncMock()
      mock.send_text = AsyncMock()
      return mock


  @pytest.fixture
  def sessions():
      return SessionManager()


  @pytest.mark.asyncio
  async def test_init_message_sends_ack(ws, sessions):
      await handle_message(sessions, "s1", ws, {"type": "init", "session_id": "s1"})
      ws.send_text.assert_awaited_once()
      sent = json.loads(ws.send_text.call_args[0][0])
      assert sent["type"] == "initAck"


  @pytest.mark.asyncio
  async def test_unknown_message_sends_error(ws, sessions):
      await handle_message(sessions, "s1", ws, {"type": "unknownXYZ"})
      ws.send_text.assert_awaited_once()
      sent = json.loads(ws.send_text.call_args[0][0])
      assert sent["type"] == "error"


  @pytest.mark.asyncio
  async def test_run_task_streams_deltas(ws, sessions):
      await handle_message(sessions, "s1", ws, {
          "type": "runTask", "task_id": "t1",
          "task": "generateText", "payload": {"prompt": "hi"},
      })
      calls = [json.loads(c[0][0]) for c in ws.send_text.await_args_list]
      types = [c["type"] for c in calls]
      assert "taskStarted" in types
      assert "taskDelta" in types
      assert "taskComplete" in types
  ```

### Step 3: Run test
- Command:
  ```powershell
  pytest tests/test_backend_ws_handler.py -v 2>&1
  ```
- Expected:
  ```
  PASSED tests/test_backend_ws_handler.py::test_init_message_sends_ack
  PASSED tests/test_backend_ws_handler.py::test_unknown_message_sends_error
  PASSED tests/test_backend_ws_handler.py::test_run_task_streams_deltas
  ```

---

## Task 7 — Implement `backend/__main__.py` — runnable entrypoint

### Step 1: Create `backend/__main__.py`
- File: `backend/__main__.py`
- Content:
  ```python
  #!/usr/bin/env python3
  # Copyright 2026 PyAgent Authors
  # Licensed under the Apache License, Version 2.0 (the "License");
  # you may not use this file except in compliance with the License.
  # You may obtain a copy of the License at
  #
  #     http://www.apache.org/licenses/LICENSE-2.0
  #
  # Unless required by applicable law or agreed to in writing, software
  # distributed under the License is distributed on an "AS IS" BASIS,
  # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  # See the License for the specific language governing permissions and
  # limitations under the License.
  """Run the PyAgent backend worker with: python -m backend"""
  import uvicorn
  from .app import app

  if __name__ == "__main__":
      uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
  ```

### Step 2: Verify entrypoint is runnable (dry check — not a full server start during CI)
- Command:
  ```powershell
  python -c "from backend.__main__ import app; print('OK')" 2>&1
  ```
- Expected:
  ```
  OK
  ```

---

## Task 8 — Update Vite proxy to forward `/ws` and `/api` to Python backend

### Step 1: Edit `web/vite.config.ts`
- File: `web/vite.config.ts`
- Replace the existing `server.proxy` block:
  ```typescript
  server: {
    proxy: {
      '/api-proxy': 'http://localhost:5000',  // OLD — remove this
    },
  },
  ```
  With:
  ```typescript
  server: {
    proxy: {
      '/ws': {
        target: 'http://127.0.0.1:8000',
        ws: true,
        changeOrigin: true,
      },
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  ```

### Step 2: Verify Vite config has no TypeScript errors
- Command:
  ```powershell
  cd web; npx tsc --noEmit 2>&1
  ```
- Expected: no errors

---

## Task 9 — Add frontend WebSocket hook (`useWebSocket.ts`)

### Step 1: Write failing test for hook module existence
- File: `web/hooks/useWebSocket.test.ts` (Vitest)
- Content:
  ```typescript
  import { describe, it, expect, vi } from 'vitest';
  import { renderHook } from '@testing-library/react';
  import { useWebSocket } from './useWebSocket';

  describe('useWebSocket', () => {
    it('exports useWebSocket function', () => {
      expect(typeof useWebSocket).toBe('function');
    });
  });
  ```

### Step 2: Run test and observe failure
- Command:
  ```powershell
  cd web; npx vitest run hooks/useWebSocket.test.ts 2>&1
  ```
- Expected: `FAIL` — file does not exist yet

### Step 3: Create `web/hooks/useWebSocket.ts`
- File: `web/hooks/useWebSocket.ts`
- Content:
  ```typescript
  import { useEffect, useRef, useCallback, useState } from 'react';

  export interface WsMessage {
    type: string;
    [key: string]: unknown;
  }

  export interface UseWebSocketOptions {
    onMessage?: (msg: WsMessage) => void;
    reconnectDelay?: number;
  }

  export function useWebSocket(url: string, options: UseWebSocketOptions = {}) {
    const wsRef = useRef<WebSocket | null>(null);
    const [connected, setConnected] = useState(false);
    const { onMessage, reconnectDelay = 2000 } = options;

    useEffect(() => {
      let active = true;
      function connect() {
        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => { if (active) setConnected(true); };
        ws.onclose = () => {
          if (active) {
            setConnected(false);
            setTimeout(connect, reconnectDelay);
          }
        };
        ws.onmessage = (event) => {
          try {
            const msg = JSON.parse(event.data) as WsMessage;
            onMessage?.(msg);
          } catch { /* ignore malformed messages */ }
        };
      }
      connect();
      return () => {
        active = false;
        wsRef.current?.close();
      };
    }, [url]);

    const send = useCallback((msg: WsMessage) => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify(msg));
      }
    }, []);

    return { send, connected };
  }
  ```

### Step 4: Run test and verify pass
- Command:
  ```powershell
  cd web; npx vitest run hooks/useWebSocket.test.ts 2>&1
  ```
- Expected:
  ```
  PASS hooks/useWebSocket.test.ts
  ✓ exports useWebSocket function
  ```

---

## Task 10 — Add frontend Action Registry (`actionRegistry.ts`)

### Step 1: Write failing test for action registry
- File: `web/hooks/actionRegistry.test.ts`
- Content:
  ```typescript
  import { describe, it, expect, vi } from 'vitest';
  import { ActionRegistry, createDefaultRegistry } from './actionRegistry';

  describe('ActionRegistry', () => {
    it('executes a registered action', async () => {
      const registry = new ActionRegistry();
      const handler = vi.fn();
      registry.register('test', handler);
      await registry.execute('test', { x: 1 });
      expect(handler).toHaveBeenCalledWith({ x: 1 });
    });

    it('throws for unknown action', async () => {
      const registry = new ActionRegistry();
      await expect(registry.execute('unknown', {})).rejects.toThrow();
    });

    it('createDefaultRegistry includes openWindow action', () => {
      const registry = createDefaultRegistry(() => {});
      expect(registry.has('openWindow')).toBe(true);
    });
  });
  ```

### Step 2: Run test and observe failure
- Command:
  ```powershell
  cd web; npx vitest run hooks/actionRegistry.test.ts 2>&1
  ```
- Expected: `FAIL` — file does not exist yet

### Step 3: Create `web/hooks/actionRegistry.ts`
- File: `web/hooks/actionRegistry.ts`
- Content:
  ```typescript
  export type ActionHandler = (params: Record<string, unknown>) => Promise<void> | void;

  export class ActionRegistry {
    private _handlers = new Map<string, ActionHandler>();

    register(action: string, handler: ActionHandler): void {
      this._handlers.set(action, handler);
    }

    has(action: string): boolean {
      return this._handlers.has(action);
    }

    async execute(action: string, params: Record<string, unknown>): Promise<void> {
      const handler = this._handlers.get(action);
      if (!handler) {
        throw new Error(`Unknown action: "${action}". Not registered in ActionRegistry.`);
      }
      await handler(params);
    }
  }

  /** Build a default registry wired to the NebulaOS app state. */
  export function createDefaultRegistry(openApp: (appId: string) => void): ActionRegistry {
    const registry = new ActionRegistry();

    registry.register('openWindow', async (params) => {
      const appId = params['appId'] as string;
      if (!appId) throw new Error('openWindow requires appId param');
      openApp(appId);
    });

    registry.register('log', async (params) => {
      console.log('[ActionRegistry:log]', params);
    });

    return registry;
  }
  ```

### Step 4: Run test
- Command:
  ```powershell
  cd web; npx vitest run hooks/actionRegistry.test.ts 2>&1
  ```
- Expected:
  ```
  PASS hooks/actionRegistry.test.ts
  ✓ executes a registered action
  ✓ throws for unknown action
  ✓ createDefaultRegistry includes openWindow action
  ```

---

## Task 11 — Add voice input component (`VoiceInput.tsx`)

### Step 1: Create `web/components/VoiceInput.tsx`
- File: `web/components/VoiceInput.tsx`
- Content:
  ```typescript
  import React, { useCallback, useRef, useState } from 'react';
  import { Mic, MicOff } from 'lucide-react';
  import { cn } from '../utils';

  interface VoiceInputProps {
    onTranscript: (transcript: string, isFinal: boolean) => void;
  }

  export const VoiceInput: React.FC<VoiceInputProps> = ({ onTranscript }) => {
    const [isListening, setIsListening] = useState(false);
    const recognitionRef = useRef<SpeechRecognition | null>(null);

    const startListening = useCallback(() => {
      const SpeechRecognitionAPI =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (!SpeechRecognitionAPI) {
        console.warn('Web Speech API not supported in this browser');
        return;
      }
      const recognition: SpeechRecognition = new SpeechRecognitionAPI();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i];
          if (result.isFinal) {
            onTranscript(result[0].transcript, true);
          } else {
            interim += result[0].transcript;
          }
        }
        if (interim) onTranscript(interim, false);
      };

      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);

      recognition.start();
      recognitionRef.current = recognition;
      setIsListening(true);
    }, [onTranscript]);

    const stopListening = useCallback(() => {
      recognitionRef.current?.stop();
      setIsListening(false);
    }, []);

    return (
      <button
        onMouseDown={startListening}
        onMouseUp={stopListening}
        onTouchStart={startListening}
        onTouchEnd={stopListening}
        className={cn(
          'p-2 rounded-lg transition-all duration-200 border',
          isListening
            ? 'bg-red-500 text-white border-red-600 animate-pulse'
            : 'bg-os-window text-os-text border-os-border hover:bg-os-border'
        )}
        title="Hold to speak"
        aria-label={isListening ? 'Listening…' : 'Push to talk'}
      >
        {isListening ? <Mic size={18} /> : <MicOff size={18} />}
      </button>
    );
  };
  ```

### Step 2: Verify no TypeScript errors
- Command:
  ```powershell
  cd web; npx tsc --noEmit 2>&1
  ```
- Expected: no errors involving `VoiceInput.tsx`

---

## Task 12 — Add webcam/video conferencing panel (`VideoPanel.tsx`)

### Step 1: Create `web/components/VideoPanel.tsx`
- File: `web/components/VideoPanel.tsx`
- Content:
  ```typescript
  import React, { useEffect, useRef, useCallback, useState } from 'react';
  import { Camera, CameraOff, PhoneOff } from 'lucide-react';
  import { cn } from '../utils';

  interface VideoPanelProps {
    /** Called with SDP offer/answer/ICE payload to relay via WebSocket */
    onSignal: (signal: { signal_type: string; payload: Record<string, unknown> }) => void;
    /** Incoming signal from a remote peer (relayed from backend) */
    incomingSignal?: { signal_type: string; payload: Record<string, unknown> };
    peerId: string;
  }

  export const VideoPanel: React.FC<VideoPanelProps> = ({ onSignal, incomingSignal, peerId }) => {
    const localVideoRef = useRef<HTMLVideoElement>(null);
    const remoteVideoRef = useRef<HTMLVideoElement>(null);
    const pcRef = useRef<RTCPeerConnection | null>(null);
    const [camActive, setCamActive] = useState(false);
    const [status, setStatus] = useState<'idle' | 'calling' | 'connected'>('idle');

    const startCamera = useCallback(async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (localVideoRef.current) localVideoRef.current.srcObject = stream;
        setCamActive(true);

        const pc = new RTCPeerConnection({
          iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
        });
        pcRef.current = pc;

        stream.getTracks().forEach((track) => pc.addTrack(track, stream));

        pc.onicecandidate = (event) => {
          if (event.candidate) {
            onSignal({ signal_type: 'ice', payload: { candidate: event.candidate.toJSON() } });
          }
        };

        pc.ontrack = (event) => {
          if (remoteVideoRef.current) {
            remoteVideoRef.current.srcObject = event.streams[0];
            setStatus('connected');
          }
        };

        // Create and send offer
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        onSignal({ signal_type: 'offer', payload: { sdp: offer.sdp, type: offer.type } });
        setStatus('calling');
      } catch (err) {
        console.error('Camera error:', err);
      }
    }, [onSignal]);

    // Handle incoming signals
    useEffect(() => {
      const pc = pcRef.current;
      if (!pc || !incomingSignal) return;
      (async () => {
        const { signal_type, payload } = incomingSignal;
        if (signal_type === 'answer') {
          await pc.setRemoteDescription(new RTCSessionDescription(payload as RTCSessionDescriptionInit));
        } else if (signal_type === 'ice') {
          await pc.addIceCandidate(new RTCIceCandidate(payload['candidate'] as RTCIceCandidateInit));
        }
      })();
    }, [incomingSignal]);

    const hangUp = useCallback(() => {
      pcRef.current?.close();
      pcRef.current = null;
      if (localVideoRef.current?.srcObject) {
        (localVideoRef.current.srcObject as MediaStream).getTracks().forEach((t) => t.stop());
        localVideoRef.current.srcObject = null;
      }
      setCamActive(false);
      setStatus('idle');
    }, []);

    return (
      <div className="flex flex-col gap-2 bg-os-window border border-os-border rounded-xl p-3">
        <div className="flex gap-2">
          <video
            ref={localVideoRef} autoPlay muted playsInline
            className="w-1/2 rounded-lg bg-black aspect-video object-cover"
          />
          <video
            ref={remoteVideoRef} autoPlay playsInline
            className="w-1/2 rounded-lg bg-black aspect-video object-cover"
          />
        </div>
        <div className="flex items-center gap-2 justify-center">
          {!camActive ? (
            <button onClick={startCamera} className="flex items-center gap-2 px-3 py-1.5 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors">
              <Camera size={16} /> Start Camera
            </button>
          ) : (
            <button onClick={hangUp} className="flex items-center gap-2 px-3 py-1.5 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors">
              <PhoneOff size={16} /> Hang Up
            </button>
          )}
          <span className="text-xs text-os-text/60 capitalize">{status}</span>
        </div>
      </div>
    );
  };
  ```

### Step 2: Verify TypeScript
- Command:
  ```powershell
  cd web; npx tsc --noEmit 2>&1
  ```
- Expected: no errors

---

## Task 13 — Wire AI streaming panel into `App.tsx`

### Step 1: Add `AiPanel` component (`web/components/AiPanel.tsx`)
- File: `web/components/AiPanel.tsx`
- Content:
  ```typescript
  import React, { useState, useCallback } from 'react';
  import { Bot, Loader2 } from 'lucide-react';
  import { useWebSocket, WsMessage } from '../hooks/useWebSocket';
  import { VoiceInput } from './VoiceInput';
  import { cn } from '../utils';

  interface AiPanelProps {
    onActionRequest: (action: string, params: Record<string, unknown>) => void;
  }

  export const AiPanel: React.FC<AiPanelProps> = ({ onActionRequest }) => {
    const [output, setOutput] = useState('');
    const [isStreaming, setIsStreaming] = useState(false);
    const [prompt, setPrompt] = useState('');

    const handleMessage = useCallback((msg: WsMessage) => {
      if (msg.type === 'taskDelta') {
        setOutput((prev) => prev + (msg.delta as string));
      } else if (msg.type === 'taskStarted') {
        setIsStreaming(true);
        setOutput('');
      } else if (msg.type === 'taskComplete') {
        setIsStreaming(false);
      } else if (msg.type === 'actionRequest') {
        onActionRequest(msg.action as string, (msg.params ?? {}) as Record<string, unknown>);
      }
    }, [onActionRequest]);

    const { send, connected } = useWebSocket('ws://localhost:5173/ws', { onMessage: handleMessage });

    const submitPrompt = useCallback((text: string) => {
      if (!text.trim()) return;
      send({ type: 'runTask', task_id: crypto.randomUUID(), task: 'generateText', payload: { prompt: text } });
      setPrompt('');
    }, [send]);

    return (
      <div className="flex flex-col h-full bg-os-bg text-os-text p-3 gap-2">
        <div className={cn("text-xs flex items-center gap-1", connected ? "text-green-400" : "text-yellow-400")}>
          <Bot size={14} />
          {connected ? 'AI Connected' : 'Connecting…'}
          {isStreaming && <Loader2 size={12} className="animate-spin ml-1" />}
        </div>

        <div className="flex-1 bg-os-window border border-os-border rounded-lg p-2 font-mono text-xs overflow-y-auto whitespace-pre-wrap min-h-[100px]">
          {output || <span className="text-os-text/40">AI output will appear here…</span>}
        </div>

        <div className="flex gap-2">
          <input
            className="flex-1 bg-os-window border border-os-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-os-accent"
            placeholder="Ask AI…"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && submitPrompt(prompt)}
          />
          <VoiceInput onTranscript={(t, final) => final && submitPrompt(t)} />
        </div>
      </div>
    );
  };
  ```

### Step 2: Verify TypeScript
- Command:
  ```powershell
  cd web; npx tsc --noEmit 2>&1
  ```
- Expected: no errors

---

## Task 14 — Retire `web/backend/` Node.js proxy

### Step 1: Delete `web/backend/`
- Command:
  ```powershell
  Remove-Item -Recurse -Force web\backend\
  ```

### Step 2: Remove `vertex-ai-proxy-interceptor.js` import from `web/index.tsx`
- File: `web/index.tsx`
- Remove: `import './vertex-ai-proxy-interceptor.js';`

### Step 3: Delete `web/vertex-ai-proxy-interceptor.js`
- Command:
  ```powershell
  Remove-Item web\vertex-ai-proxy-interceptor.js
  ```

### Step 4: Verify frontend still compiles
- Command:
  ```powershell
  cd web; npx tsc --noEmit 2>&1
  ```
- Expected: no errors

---

## Task 15 — Run all backend + frontend tests together

### Step 1: Install backend dependencies
- Command:
  ```powershell
  pip install -r backend/requirements.txt 2>&1
  ```
- Expected: successful install with no errors

### Step 2: Run all backend tests
- Command:
  ```powershell
  pytest tests/test_backend_worker.py tests/test_backend_models.py tests/test_backend_session_manager.py tests/test_backend_ws_handler.py -v 2>&1
  ```
- Expected output:
  ```
  PASSED tests/test_backend_worker.py::test_backend_package_importable
  PASSED tests/test_backend_worker.py::test_backend_app_importable
  PASSED tests/test_backend_models.py::test_init_message_valid
  PASSED tests/test_backend_models.py::test_run_task_message_valid
  PASSED tests/test_backend_models.py::test_task_delta_message_valid
  PASSED tests/test_backend_models.py::test_action_request_message_valid
  PASSED tests/test_backend_models.py::test_signal_message_valid
  PASSED tests/test_backend_session_manager.py::test_connect_returns_session_id
  PASSED tests/test_backend_session_manager.py::test_disconnect_removes_session
  PASSED tests/test_backend_session_manager.py::test_disconnect_nonexistent_session_is_safe
  PASSED tests/test_backend_ws_handler.py::test_init_message_sends_ack
  PASSED tests/test_backend_ws_handler.py::test_unknown_message_sends_error
  PASSED tests/test_backend_ws_handler.py::test_run_task_streams_deltas

  13 passed
  ```

### Step 3: Run frontend hook tests
- Command:
  ```powershell
  cd web; npx vitest run 2>&1
  ```
- Expected:
  ```
  PASS hooks/useWebSocket.test.ts
  PASS hooks/actionRegistry.test.ts
  ```

---

## Task 16 — Update `backend/README.md` to reflect final structure

### Step 1: Edit `backend/README.md`
Replace the placeholder content with accurate instructions:
- File: `backend/README.md`
- Replace "Next steps" with:
  ```markdown
  ## Running the backend worker

  ```powershell
  pip install -r backend/requirements.txt
  python -m backend
  ```

  The server starts at `http://127.0.0.1:8000`.
  The WebSocket endpoint is at `ws://127.0.0.1:8000/ws`.
  Vite dev server proxies `/ws` → Python backend automatically.

  ## Architecture

  - `app.py` — FastAPI app, WebSocket + REST endpoints
  - `session_manager.py` — active WebSocket session registry
  - `ws_handler.py` — message dispatch (runTask, signal, speech, control)
  - `models.py` — Pydantic message schemas
  - `__main__.py` — uvicorn entrypoint
  ```

### Step 2: Verify README is up-to-date
- Command:
  ```powershell
  Get-Content backend\README.md | Select-Object -First 30
  ```
- Expected: shows the updated content above.

---

*Plan complete. Hand off to agent/runSubagent.*
