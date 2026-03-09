# PyAgent Implementation Plan

**Goal:** Enable integrated chatrooms where humans and agents can communicate, 
  with project-specific and personal assistant rooms and AI-driven assistance 
  via a custom GitHub App/MCP integration.

**Architecture:** A lightweight FastAPI chat service stores rooms and messages. 
  MCP tools allow swarm agents to post and react to chat events. 
  GitHub App webhooks feed updates into the chat (issue/PR summaries, labels). 
  Human clients (Discord/Matrix/web) connect to the chat service 
  for real-time conversations.

**Tech Stack:**
- Python 3.11
- FastAPI for chat API
- pytest for tests
- in-memory storage (later Redis)
- MCP Python SDK to register chat tools
- GitHub App configuration files

---

### Task 1: Define chat room model and persistence

**Step 1: Write failing test for room storage**
- File: `src/chat/models.py`
  ```python
  from typing import List, Dict

  class ChatRoom:
      def __init__(self, name: str, members: List[str]):
          self.name = name
          self.members = members
          self.messages: List[Dict[str, str]] = []

      def post(self, sender: str, text: str) -> None:
          raise NotImplementedError()

      def history(self) -> List[Dict[str, str]]:
          raise NotImplementedError()
  ```

- Test file: `tests/test_chat_models.py`
  ```python
  from chat.models import ChatRoom

  def test_room_post_and_history() -> None:
      room = ChatRoom("project-x", ["alice", "agent-1"])
      assert room.history() == []
      room.post("alice", "hello")
      assert room.history()[0]["sender"] == "alice"
      assert room.history()[0]["text"] == "hello"
  ```

**Step 2: Run `pytest tests/test_chat_models.py -q`** and observe failure.

**Step 3: Implement methods in `ChatRoom`** so the test passes.

**Step 4: Run test again and verify success.

### Task 2: Add chat service API endpoints

**Step 1: Write failing tests for FastAPI handlers**
- Test file: `tests/test_chat_api.py`
  ```python
  from fastapi import FastAPI
  from fastapi.testclient import TestClient
  from chat.models import ChatRoom

  app = FastAPI()
  rooms = {}

  # we'll wire the real endpoints later

  def test_create_and_post() -> None:
      client = TestClient(app)
      resp = client.post("/rooms", json={"name":"proj","members":["u"]})
      assert resp.status_code == 200
      resp = client.post("/rooms/proj/messages", json={"sender":"u","text":"hi"})
      assert resp.status_code == 200
      resp = client.get("/rooms/proj/messages")
      assert resp.json()[0]["text"] == "hi"
  ```

**Step 2: Run `pytest tests/test_chat_api.py -q`** to see failures.

**Step 3: Implement handlers in `src/chat/api.py` using `rooms` dict and ChatRoom.

**Step 4: Run tests again; they should pass.

### Task 3: Register MCP chat tools

**Step 1: Write failing test for MCP tool definitions**
- Test file: `tests/test_chat_mcp.py`
  ```python
  from chat.mcp_tools import send_message_tool

  def test_mcp_tool_signature():
      assert send_message_tool.__name__ == "send_chat_message"
      assert "room" in send_message_tool.__annotations__
  ```

**Step 2:** run test and observe failure (tool not implemented).

**Step 3:** create `src/chat/mcp_tools.py` with a simple function 
  decorated for MCP; the body can be `pass`.

**Step 4:** run tests again to confirm signature.

### Task 4: Integrate GitHub App skeleton and webhook handler

**Step 1: Write failing test for webhook POST**
- Test file: `tests/test_github_app.py`
  ```python
  from fastapi import FastAPI
  from fastapi.testclient import TestClient

  app = FastAPI()

  @app.post("/webhook")
  def webhook(payload: dict):
      # placeholder
      return {"received": True}

  def test_webhook_receives():
      client = TestClient(app)
      resp = client.post("/webhook", json={"action":"opened"})
      assert resp.json()["received"]
  ```

**Step 2:** run and fail.

**Step 3:** implement real handler in `src/github_app.py` 
  and mount in main application later.

**Step 4:** run test to ensure basic reception.

### Task 5: Agent posting integration test

**Step 1: Write failing test verifying MCP tool posts to room**
- Update `tests/test_chat_api.py` to import send_message_tool and call it.

**Step 2:** run test and observe failure (tool not yet wired to API).

**Step 3:** implement `send_message_tool` to call internal API (e.g. via httpx). 
  Use monkeypatch in test to simulate network call.

**Step 4:** run and confirm success.

### Task 6: Personal assistant room linkage

**Step 1:** Write failing test for function `create_personal_room(human)` 
  which creates room with name `personal-{human}` and adds agent.

**Step 2:** Implement utility in `src/chat/utils.py`.

**Step 3:** Run test for creation and membership.

### Task 7: Add chat metrics and logging

**Step 1:** Write failing test that posting a message increments 
  a Prometheus counter.

**Step 2:** Add metric in `chat/api.py` using `prometheus_client.Counter`.

**Step 3:** Run test to validate.

### Task 8: Update CI config and templates

- Add `.github/issue_template/chat.md` and `.github/pull_request_template.md` 
  sections for chat notifications.
- Add GitHub Actions job to run `tests/test_chat_*` on pull requests.
- Tests added above already run in full suite; verify via `pytest -q` earlier.

---

This plan converts the chatroom design into a sequence of TDD steps. 
After you review and approve, I’ll save this file 
and hand off to superpower-execute for implementation.