# PyAgent Implementation Plan

**Goal:** Bootstrap the swarm architecture by implementing core services (agent registry, task scheduler, communication protocol, memory stores) with test-driven development, enabling later feature expansion.

**Architecture:** Microservices in Python coordinating via a central registry and message buses. Key components are `AgentRegistry`, `TaskScheduler`, `SwarmMemory`, and a lightweight `Message` protocol. Services expose HTTP/gRPC APIs and emit Prometheus metrics. The design supports extensible agent types, priority queues, and both shared and local memory domains.

**Tech Stack:**
- Python 3.11
- FastAPI for service endpoints
- pytest for tests
- Redis (mocked) for shared memory and queues
- Prometheus client library for metrics
- pydantic for message schemas
- Docker compose used later for integration

---

### Task 1: Define core message schema and validate logic

**Step 1: Write failing test for Message model validation**
- File: `src/swarm/message_model.py`
- Code:
  ```python
  from pydantic import BaseModel, Field, ValidationError

  class Message(BaseModel):
      id: str
      timestamp: str
      type: str
      priority: str
      source: str
      destination: str
      payload: dict
      checksum: str
  
  def validate_message(data: dict) -> bool:
      Message(**data)
      return True
  ```

- Test file: `tests/test_message_model.py`
  ```python
  import pytest
  from swarm.message_model import validate_message

  def test_validate_message_accepts_valid():
      valid = {
          "id": "uuid-1",
          "timestamp": "2026-03-09T00:00Z",
          "type": "task_request",
          "priority": "high",
          "source": "agent-1",
          "destination": "scheduler",
          "payload": {"foo": "bar"},
          "checksum": "abc",
      }
      assert validate_message(valid)

  def test_validate_message_rejects_missing_field():
      invalid = {"id": "uuid-1"}
      with pytest.raises(Exception):
          validate_message(invalid)
  ```

**Step 2: Run test and verify failure**
- Command: `pytest tests/test_message_model.py -q`
- Expected output:
  ```
  F.
  ```

**Step 3: Implement minimal Message model code above**
- Already included in step 1 file content.

**Step 4: Run test and verify success**
- Command: `pytest tests/test_message_model.py -q`
- Expected output:
  ```
  ..
  ```


### Task 2: AgentRegistry class with registration and heartbeat

**Step 1: Write failing tests for registry methods**
- Test file: `tests/test_agent_registry.py`
  ```python
  import time
  from swarm.agent_registry import AgentRegistry

  def test_register_and_query():
      reg = AgentRegistry()
      agent_id = reg.register(type="security", capabilities=["scan"])
      assert reg.get(agent_id)["type"] == "security"

  def test_heartbeat_marks_healthy():
      reg = AgentRegistry()
      aid = reg.register(type="coder", capabilities=[])
      reg.heartbeat(aid)
      assert reg.is_healthy(aid)

  def test_missing_heartbeat_unhealthy(tmp_path, monkeypatch):
      reg = AgentRegistry(heartbeat_interval=1)
      aid = reg.register(type="coder", capabilities=[])
      time.sleep(1.5)
      assert not reg.is_healthy(aid)
  ```

**Step 2: Run test to see failures**
- Command: `pytest tests/test_agent_registry.py -q`
- Expect all fail.

**Step 3: Implement `AgentRegistry` skeleton**
- File: `src/swarm/agent_registry.py`
  ```python
  import time
  from typing import Dict, Any
  
  class AgentRegistry:
      def __init__(self, heartbeat_interval: float = 30.0):
          self.heartbeat_interval = heartbeat_interval
          self._agents: Dict[str, Dict[str, Any]] = {}

      def register(self, type: str, capabilities: list[str]) -> str:
          aid = f"agent-{len(self._agents)+1}"
          self._agents[aid] = {
              "type": type,
              "capabilities": capabilities,
              "last_seen": time.time(),
          }
          return aid

      def heartbeat(self, agent_id: str):
          self._agents[agent_id]["last_seen"] = time.time()

      def get(self, agent_id: str) -> dict[str, Any]:
          return self._agents[agent_id]

      def is_healthy(self, agent_id: str) -> bool:
          last = self._agents[agent_id]["last_seen"]
          return (time.time() - last) < self.heartbeat_interval
  ```

**Step 4: Run tests and confirm they pass**
- Command: `pytest tests/test_agent_registry.py -q`
- Expected output: `...` (three passing tests)


### Task 3: Basic TaskScheduler with priority queues

**Step 1: Write failing tests for enqueue/dequeue**
- Test file: `tests/test_task_scheduler.py`
  ```python
  from swarm.task_scheduler import TaskScheduler

  def test_enqueue_dequeue_priority():
      sched = TaskScheduler()
      t1 = sched.enqueue({"name": "a"}, priority=2)
      t2 = sched.enqueue({"name": "b"}, priority=1)
      assert sched.dequeue()["name"] == "b"
      assert sched.dequeue()["name"] == "a"

  def test_modify_priority():
      sched = TaskScheduler()
      t = sched.enqueue({"x":1}, priority=3)
      sched.modify(t, priority=1)
      assert sched.dequeue()["id"] == t
  ```

**Step 2: Run tests to see failures**
- Command: `pytest tests/test_task_scheduler.py -q`

**Step 3: Implement minimal scheduler**
- File: `src/swarm/task_scheduler.py`
  ```python
  import heapq
  import uuid
  
  class TaskScheduler:
      def __init__(self):
          self._queues = {1: [], 2: [], 3: [], 4: []}
          self._tasks = {}

      def enqueue(self, payload: dict, priority: int = 3) -> str:
          tid = str(uuid.uuid4())
          self._tasks[tid] = {"id": tid, "payload": payload, "priority": priority}
          heapq.heappush(self._queues[priority], (time.time(), tid))
          return tid

      def dequeue(self) -> dict:
          for pr in sorted(self._queues):
              if self._queues[pr]:
                  _, tid = heapq.heappop(self._queues[pr])
                  return self._tasks.pop(tid)
          raise IndexError("no tasks")

      def modify(self, task_id: str, priority: int):
          if task_id in self._tasks:
              self._tasks[task_id]["priority"] = priority
          # no requeue logic in minimal impl
  ```

**Step 4: Run tests again** and verify they pass.


### Task 4: Shared and local memory modules

**Step 1: Write tests for memory stores**
- File: `tests/test_memory.py`
  ```python
  from swarm.memory import SharedMemory, AgentMemory

  def test_shared_put_get():
      m = SharedMemory()
      m.put("foo", 1)
      assert m.get("foo") == 1

  def test_agent_local():
      a = AgentMemory("agent-1")
      a.set("temp", "x")
      assert a.get("temp") == "x"
  ```

**Step 2: Run tests to confirm failure.**

**Step 3: Implement simple classes**
- File: `src/swarm/memory.py`
  ```python
  class SharedMemory:
      def __init__(self):
          self._store = {}
      def put(self, k, v):
          self._store[k] = v
      def get(self, k):
          return self._store.get(k)

  class AgentMemory:
      def __init__(self, agent_id: str):
          self.agent_id = agent_id
          self._local = {}
      def set(self, k, v):
          self._local[k] = v
      def get(self, k):
          return self._local.get(k)
  ```

**Step 4: Run tests and verify pass.


### Task 5: Metrics export helper

**Step 1: Write failing test that registry exports Prometheus metrics**
- File: `tests/test_metrics.py`
  ```python
  from swarm.agent_registry import AgentRegistry
  
  def test_metrics_contains_agent_count():
      reg = AgentRegistry()
      reg.register(type="x", capabilities=[])
      text = reg.metrics()
      assert "agent_tasks_total" in text
  ```

**Step 2:** run test (should fail)
**Step 3:** add simple `metrics` method using `prometheus_client`.
**Step 4:** run again and pass.


### Task 6: Registry API endpoints with FastAPI

... (continues building an HTTP server) ...


---

Each of the above tasks follows the TDD cycle: write a failing test, implement
minimal code, run tests to pass.  Additional features (communication channels,
security, scheduler persistence) will be added as separate tasks in Phase 2.


**Next steps:** After you review and approve this plan, I'll save it and hand
off to superpower-execute for implementation.