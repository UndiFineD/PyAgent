# prj0000088-ai-fuzzing-security - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-27_

## Selected Option
Option A - Deterministic Local Mutation Engine (Rule-Based, No Model Runtime).

Rationale:
1. It provides the safest and smallest v1 that still creates actionable fuzzing value.
2. It guarantees deterministic replay for triage and regression testing.
3. It enforces strict local-only execution with explicit policy checks.
4. It preserves an extension seam for later optional local-model-assisted mutation without coupling v1 to model runtime.

## Problem Statement And Goals
You need a deterministic local fuzzing core under `src/core/fuzzing/` that can mutate corpus inputs, execute bounded campaigns, and report reproducible results without external network behavior.

Goals:
1. Deterministic mutation and scheduling from an explicit seed.
2. Local-only execution with policy-based safety constraints.
3. Minimal composable module boundaries suitable for future growth.
4. Stable API contracts for downstream planning and implementation.
5. Testable contracts with clear coverage scope.

Out of scope in this project stage:
1. Non-deterministic model-generated mutators.
2. Distributed or remote fuzzing workers.
3. Coverage-guided instrumentation integrations.

## Architecture
### High-Level Architecture
The design uses a pipeline with six core domain modules plus policy and exception boundaries:
1. `FuzzCorpus` stores and normalizes seed entries.
2. `FuzzMutator` deterministically produces candidate payloads from corpus entries.
3. `FuzzCase` captures each executable fuzz input and metadata.
4. `FuzzSafetyPolicy` validates targets, operators, and runtime limits.
5. `FuzzEngineCore` orchestrates case generation, policy checks, and target execution.
6. `FuzzResult` captures campaign-level and case-level outcomes.

Data flow:
1. Load or build corpus.
2. Expand corpus into deterministic `FuzzCase` instances.
3. Apply safety policy gate before execution.
4. Execute cases with bounded budget.
5. Aggregate deterministic `FuzzResult` output for replay and analysis.

### Component Responsibilities
1. `FuzzCase.py`: immutable case contract and replay identity.
2. `FuzzMutator.py`: deterministic mutation operator registry and generation logic.
3. `FuzzCorpus.py`: corpus ingestion, normalization, deduplication, selection.
4. `FuzzEngineCore.py`: campaign orchestration, sequencing, execution lifecycle.
5. `FuzzSafetyPolicy.py`: policy rules, local-only guards, budget checks.
6. `FuzzResult.py`: typed result models and summary aggregation.
7. `exceptions.py`: typed exception hierarchy for policy, config, and execution failures.
8. `__init__.py`: public package export surface.

## Proposed Module Layout
`src/core/fuzzing/`
1. `FuzzCase.py`
2. `FuzzMutator.py`
3. `FuzzCorpus.py`
4. `FuzzEngineCore.py`
5. `FuzzSafetyPolicy.py`
6. `FuzzResult.py`
7. `exceptions.py`
8. `__init__.py`

## Interfaces & Contracts
### `FuzzCase.py`
Primary contract: immutable execution unit.

```python
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class FuzzCase:
	case_id: str
	run_id: str
	seed: int
	cycle_index: int
	corpus_index: int
	operator: str
	payload: bytes
	metadata: Mapping[str, str]

	def replay_key(self) -> str:
		"""Return deterministic identity for replay and dedup."""
```

Invariants:
1. `case_id` must be stable for identical inputs.
2. `payload` is immutable binary content.
3. `operator` must be declared by mutator registry.

### `FuzzMutator.py`
Primary contract: deterministic mutation generation.

```python
from typing import Iterable, Protocol

class MutationOperator(Protocol):
	name: str

	def mutate(self, seed: int, input_bytes: bytes, cycle_index: int) -> bytes:
		...

class FuzzMutator:
	def __init__(self, operators: Iterable[MutationOperator]) -> None:
		...

	def list_operators(self) -> tuple[str, ...]:
		...

	def mutate(self, operator: str, seed: int, input_bytes: bytes, cycle_index: int) -> bytes:
		...
```

Contract rules:
1. Mutation must be pure with respect to `(operator, seed, input_bytes, cycle_index)`.
2. Unknown operator raises `UnknownMutationOperatorError`.
3. Empty output is allowed only when policy explicitly permits it.

### `FuzzCorpus.py`
Primary contract: deterministic corpus source.

```python
from typing import Iterable

class FuzzCorpus:
	def __init__(self, entries: Iterable[bytes]) -> None:
		...

	def size(self) -> int:
		...

	def get(self, index: int) -> bytes:
		...

	def iter_entries(self) -> Iterable[bytes]:
		...

	def add(self, entry: bytes) -> None:
		...
```

Contract rules:
1. Order is stable and indexable.
2. Optional dedup preserves first-seen ordering.
3. Empty corpus raises `CorpusEmptyError` at engine start.

### `FuzzSafetyPolicy.py`
Primary contract: enforce local deterministic safety boundaries.

```python
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class FuzzLimits:
	max_cases: int
	max_cycles: int
	per_case_timeout_ms: int
	campaign_timeout_ms: int
	max_payload_bytes: int

class FuzzSafetyPolicy:
	def __init__(
		self,
		allowed_targets: Iterable[str],
		allowed_operators: Iterable[str],
		limits: FuzzLimits,
	) -> None:
		...

	def validate_target(self, target: str) -> None:
		...

	def validate_operator(self, operator: str) -> None:
		...

	def validate_case_payload(self, payload: bytes) -> None:
		...

	def validate_campaign_budget(self, planned_cases: int, planned_cycles: int) -> None:
		...
```

Policy guarantees:
1. Target must be allowlisted and local.
2. Networked execution paths are rejected by default.
3. Budget limits are enforced before and during execution.

### `FuzzResult.py`
Primary contract: immutable output records.

```python
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class CaseExecutionResult:
	case_id: str
	succeeded: bool
	duration_ms: int
	exit_code: int | None
	error_type: str | None
	error_message: str | None
	observations: Mapping[str, str]

@dataclass(frozen=True)
class FuzzResult:
	run_id: str
	seed: int
	planned_cases: int
	executed_cases: int
	failed_cases: int
	timed_out_cases: int
	total_duration_ms: int
	case_results: tuple[CaseExecutionResult, ...]

	def success_rate(self) -> float:
		...
```

Contract rules:
1. `run_id` ties all cases to one deterministic campaign.
2. `case_results` order matches execution order.
3. Summary counts must equal the aggregate case records.

### `FuzzEngineCore.py`
Primary contract: deterministic campaign orchestrator.

```python
from typing import Iterable

class FuzzEngineCore:
	def __init__(
		self,
		corpus: FuzzCorpus,
		mutator: FuzzMutator,
		policy: FuzzSafetyPolicy,
	) -> None:
		...

	def build_cases(
		self,
		seed: int,
		operators: Iterable[str],
		cycles: int,
	) -> tuple[FuzzCase, ...]:
		...

	def execute(
		self,
		target: str,
		cases: Iterable[FuzzCase],
	) -> FuzzResult:
		...

	def run(
		self,
		target: str,
		seed: int,
		operators: Iterable[str],
		cycles: int,
	) -> FuzzResult:
		...
```

Engine guarantees:
1. `run` is equivalent to `build_cases` then `execute`.
2. Case ordering is deterministic for the same input tuple.
3. Policy checks happen before execution and during runtime boundaries.

### `exceptions.py`
Typed hierarchy:

```python
class FuzzingError(Exception):
	...

class FuzzConfigurationError(FuzzingError):
	...

class FuzzPolicyViolationError(FuzzingError):
	...

class UnknownMutationOperatorError(FuzzConfigurationError):
	...

class CorpusEmptyError(FuzzConfigurationError):
	...

class CampaignBudgetExceededError(FuzzPolicyViolationError):
	...

class TargetNotAllowedError(FuzzPolicyViolationError):
	...
```

### `__init__.py`
Public export contract:

```python
from .FuzzCase import FuzzCase
from .FuzzCorpus import FuzzCorpus
from .FuzzEngineCore import FuzzEngineCore
from .FuzzMutator import FuzzMutator
from .FuzzResult import CaseExecutionResult, FuzzResult
from .FuzzSafetyPolicy import FuzzLimits, FuzzSafetyPolicy
```

## Determinism Contract
For identical input tuple `(target, seed, corpus contents/order, operator list/order, cycles, policy limits)`:
1. The generated case sequence must be identical.
2. Every case replay key must be identical.
3. Aggregate `FuzzResult` summary fields must be reproducible except wall-clock timing drift.

## Non-Functional Requirements
- Performance: Default configuration should support at least 1,000 generated cases per campaign with policy-constrained execution and deterministic ordering.
- Security: Engine must reject non-allowlisted targets and disallow external network access paths by default.
- Testability: All modules must be constructor-injected and deterministic under fixed seeds to enable stable unit/integration tests.

## Test Scope (18)
1. `FuzzCase.replay_key` is stable for identical fields.
2. `FuzzCase.replay_key` changes when seed/operator/payload changes.
3. `FuzzCorpus` preserves insertion order.
4. `FuzzCorpus` dedup mode retains first-seen entry.
5. `FuzzCorpus.get` rejects invalid index bounds.
6. `FuzzMutator.list_operators` returns deterministic operator order.
7. `FuzzMutator.mutate` raises on unknown operator.
8. Each built-in operator is deterministic across repeated calls.
9. `FuzzSafetyPolicy.validate_target` rejects non-allowlisted target.
10. `FuzzSafetyPolicy.validate_operator` rejects blocked operator.
11. `FuzzSafetyPolicy.validate_case_payload` enforces max payload size.
12. `FuzzSafetyPolicy.validate_campaign_budget` enforces `max_cases`.
13. `FuzzEngineCore.build_cases` creates stable ordering for identical seed and corpus.
14. `FuzzEngineCore.build_cases` fails when corpus is empty.
15. `FuzzEngineCore.execute` aggregates counts consistently with case results.
16. `FuzzEngineCore.run` equals `build_cases + execute` functional behavior.
17. Timeout budget violation yields policy/timeout failure records without crashing campaign aggregation.
18. Full replay test: same seed/config produces matching case IDs and summary stats across two runs.

## Open Questions
None blocking for @4plan. Optional follow-up decisions can be made during planning without changing this core module contract.
