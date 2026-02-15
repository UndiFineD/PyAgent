# Task: Implement Fleet Security & Architecture Enhancements

**Priority**: High  
**Assigned To**: CoderAgent (Python specialist) or MCP-enabled tool  
**Estimated Effort**: 3-4 hours  
**Due**: Within 1 sprint

---

## Objective
Implement 3 critical architectural and security improvements for the PyAgent fleet:

1. **Agent Execution Sandboxing** (Security)
2. **LLM Request Circuit Breaker** (Architecture/Resilience)
3. **Immutable Audit Trail** (Security/Compliance)

---

## Task 1: Agent Execution Sandboxing

**File**: `src/core/base/mixins/sandbox_mixin.py` (NEW)

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

"""Sandbox mixin to restrict agent file/network access."""

from pathlib import Path
from typing import Set


class SandboxMixin:
    """Restrict agent file and network operations to approved paths."""

    def __init__(self, allowed_paths: list[str], network_enabled: bool = False):
        self._allowed_paths: Set[Path] = {Path(p).resolve() for p in allowed_paths}
        self._network_enabled = network_enabled

    def validate_path(self, path: Path) -> None:
        """Validate that a path is within the allowed sandbox."""
        resolved = path.resolve()
        if not any(resolved.is_relative_to(p) for p in self._allowed_paths):
            raise PermissionError(
                f"Sandbox violation: Path {resolved} is outside allowed paths {self._allowed_paths}"
            )

    def validate_network_access(self) -> None:
        """Validate that network operations are permitted."""
        if not self._network_enabled:
            raise PermissionError("Network access not permitted for this agent")
```

**Integration Points**:
- Add `SandboxMixin` to `BaseAgent` class hierarchy
- Modify `StateTransaction` in `src/core/base/agent_state_manager.py` to call `validate_path()` before all file ops
- Update agent initialization to pass workspace-specific allowed paths

---

## Task 2: LLM Request Circuit Breaker

**File**: `src/core/llm/circuit_breaker.py` (NEW)

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

"""Circuit breaker for LLM API resilience."""

import asyncio
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is in OPEN state."""


class CircuitBreaker:
    """Prevents cascade failures when LLM APIs fail or rate-limit."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failures = 0
        self.threshold = failure_threshold
        self.timeout = timeout
        self.opened_at: float | None = None
        self.success_count = 0

    async def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute function with circuit breaker protection."""
        current_time = asyncio.get_event_loop().time()

        # Check if circuit breaker is OPEN
        if self.opened_at and (current_time - self.opened_at) < self.timeout:
            logger.warning("Circuit breaker OPEN - rejecting request")
            raise CircuitBreakerOpenError(
                f"Circuit breaker open for {self.timeout - (current_time - self.opened_at):.1f}s"
            )

        # Half-open: reset on timeout
        if self.opened_at and (current_time - self.opened_at) >= self.timeout:
            logger.info("Circuit breaker entering HALF-OPEN state")
            self.opened_at = None

        try:
            result = await func(*args, **kwargs)
            # Success: reset failure counter
            self.failures = 0
            self.success_count += 1
            return result
        except Exception as e:
            self.failures += 1
            logger.error(f"Circuit breaker failure {self.failures}/{self.threshold}: {e}")
            
            if self.failures >= self.threshold:
                self.opened_at = current_time
                logger.critical(f"Circuit breaker OPEN after {self.failures} failures")
            raise
```

**Integration Points**:
- Wrap all `LLMProvider.generate()` calls in `src/inference/llm_provider.py`
- Add fallback logic to use local/cached models when circuit is OPEN
- Integrate with `src/observability/structured_logger.py` for alerting

---

## Task 3: Immutable Audit Trail

**File**: `src/core/audit/audit_logger.py` (NEW)

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

"""Immutable audit trail with hash-chain verification."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class AuditLogger:
    """Chain-linked audit log with tamper-proof hash verification."""

    def __init__(self, storage_path: Path):
        self.storage = storage_path
        self.storage.mkdir(parents=True, exist_ok=True)
        self.prev_hash = self._load_latest_hash()

    def _load_latest_hash(self) -> str:
        """Load the hash of the most recent audit event."""
        audit_files = sorted(self.storage.glob("*.json"))
        if not audit_files:
            return "0" * 64  # Genesis hash
        
        with open(audit_files[-1], encoding="utf-8") as f:
            return json.load(f).get("hash", "0" * 64)

    def log_event(self, agent_id: str, action: str, data: Dict[str, Any]) -> str:
        """Log an audit event with cryptographic linking."""
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_id": agent_id,
            "action": action,
            "data": data,
            "prev_hash": self.prev_hash,
        }
        
        # Compute deterministic hash
        event_str = json.dumps(event, sort_keys=True)
        event_hash = hashlib.sha256(event_str.encode()).hexdigest()
        event["hash"] = event_hash

        # Write to immutable storage
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}_{event_hash[:8]}.json"
        with open(self.storage / filename, "w", encoding="utf-8") as f:
            json.dump(event, f, indent=2)

        self.prev_hash = event_hash
        return event_hash

    def verify_chain(self) -> bool:
        """Verify the integrity of the entire audit chain."""
        audit_files = sorted(self.storage.glob("*.json"))
        prev_hash = "0" * 64

        for audit_file in audit_files:
            with open(audit_file, encoding="utf-8") as f:
                event = json.load(f)
            
            if event["prev_hash"] != prev_hash:
                return False
            
            # Recompute hash
            event_copy = event.copy()
            stored_hash = event_copy.pop("hash")
            event_str = json.dumps(event_copy, sort_keys=True)
            computed_hash = hashlib.sha256(event_str.encode()).hexdigest()
            
            if stored_hash != computed_hash:
                return False
            
            prev_hash = stored_hash
        
        return True
```

**Integration Points**:
- Integrate into `CascadeContext` (`src/core/base/models/communication_models.py`)
- Log events before/after all `StateTransaction.commit()` calls
- Add audit hooks to agent initialization, tool calls, and file modifications
- Expose `verify_chain()` via CLI command for compliance audits

---

## Acceptance Criteria

- [ ] All new modules pass `pytest tests/` with 95%+ coverage
- [ ] All new code passes `ruff check` and `mypy` validation
- [ ] Sandbox violations raise `PermissionError` with clear messages
- [ ] Circuit breaker prevents >5 consecutive LLM failures
- [ ] Audit chain integrity verified via `verify_chain()`
- [ ] Documentation added to `docs/ARCHITECTURE.md` and `docs/SECURITY.md`
- [ ] Integration tests demonstrate end-to-end functionality

---

## Testing Strategy

1. **Sandbox Tests** (`tests/unit/core/base/mixins/test_sandbox_mixin.py`):
   - Valid path access succeeds
   - Invalid path raises `PermissionError`
   - Network access enforcement

2. **Circuit Breaker Tests** (`tests/unit/core/llm/test_circuit_breaker.py`):
   - Transitions: CLOSED → OPEN → HALF-OPEN → CLOSED
   - Failure threshold enforcement
   - Timeout recovery

3. **Audit Trail Tests** (`tests/unit/core/audit/test_audit_logger.py`):
   - Hash chain integrity
   - Tamper detection
   - Multi-agent event ordering

---

## Dependencies

- No new external dependencies required
- Uses existing: `asyncio`, `hashlib`, `pathlib`, `json`

---

## Rollout Plan

1. **Phase 1**: Implement core modules (sandbox, circuit breaker, audit)
2. **Phase 2**: Integrate into `BaseAgent` and `StateTransaction`
3. **Phase 3**: Add test coverage (unit + integration)
4. **Phase 4**: Update documentation and run full regression suite
5. **Phase 5**: Deploy to staging fleet, monitor for 48h, then prod

---

## Notes

- Follow PyAgent naming conventions: `snake_case` modules, `PascalCase` classes
- All code must include the Apache 2.0 license header
- Use `asyncio` for all I/O operations
- Integrate with existing `StructuredLogger` for observability
- Consider adding Prometheus metrics for circuit breaker state

---

## Delegation Commands

### Option 1: PyAgent CLI (Local Fleet)
```powershell
python src/interface/ui/cli/pyagent_cli.py delegate-task --file temp\agent_task_security_architecture.md --agent CoderAgent
```

### Option 2: MCP Protocol (if configured)
```powershell
# Requires MCP server setup in mcp.json
mcp-client call pyagent/implement --args '{"task_file": "temp/agent_task_security_architecture.md"}'
```

### Option 3: Direct Agent Instantiation
```python
from pathlib import Path
from src.logic.agents.development.coder_agent import CoderAgent
from src.core.base.models.communication_models import CascadeContext

# Initialize agent
workspace = Path.cwd()
agent = CoderAgent(file_path=str(workspace / "temp" / "agent_task_security_architecture.md"))

# Create task context
context = CascadeContext(
    task_id="security-arch-impl-001",
    task="Implement sandbox, circuit breaker, and audit trail as specified",
    priority=8,
    parent_agent_id="FleetManager",
    lineage=["FleetManager", "CoderAgent"]
)

# Execute
await agent.execute_task(context)
```
