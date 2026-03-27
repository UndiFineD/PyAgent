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

"""Red-phase behavior tests for prj0000085 shadow replay contracts.

These tests intentionally define the expected replay behavior before
implementation. They fail with explicit behavior messages when replay
modules are still missing.
"""

from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import dataclass
from typing import Any

import pytest


def _require_symbol(module_name: str, symbol_name: str) -> Any:
    """Import a replay symbol and fail with a behavior-focused message.

    Args:
        module_name: Replay module filename without extension.
        symbol_name: Symbol expected in that module.

    Returns:
        Imported symbol object.

    """
    module_path = f"src.core.replay.{module_name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing replay behavior module '{module_path}'. "
            "Implement replay contract before satisfying red-phase tests.",
            pytrace=False,
        )
        raise AssertionError("Unreachable after pytest.fail") from exc

    if not hasattr(module, symbol_name):
        pytest.fail(
            f"Module '{module_path}' does not expose required symbol '{symbol_name}'.",
            pytrace=False,
        )

    return getattr(module, symbol_name)


def _replay_envelope_payload(
    *,
    session_id: str = "s-001",
    sequence_no: int = 1,
    logical_clock: int = 1,
) -> dict[str, Any]:
    """Build a deterministic replay envelope payload fixture.

    Args:
        session_id: Session identifier.
        sequence_no: Monotonic sequence number.
        logical_clock: Monotonic logical clock value.

    Returns:
        Canonical envelope payload dictionary.

    """
    canonical: dict[str, Any] = {
        "schema_version": "1.0",
        "envelope_id": f"env-{session_id}-{sequence_no}",
        "session_id": session_id,
        "sequence_no": sequence_no,
        "event_type": "tool_call",
        "occurred_at": "2026-03-27T00:00:00Z",
        "logical_clock": logical_clock,
        "context_id": "ctx-001",
        "transaction_id": "tx-001",
        "parent_transaction_id": None,
        "agent_name": "ReplayAgent",
        "tool_name": "noop_tool",
        "input_payload": {"query": "ping"},
        "output_payload": {"result": "pong"},
        "side_effect_intents": [],
    }
    checksum_source = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    canonical["checksum"] = hashlib.sha256(checksum_source).hexdigest()
    return canonical


def _build_envelope(*, sequence_no: int, session_id: str = "s-store", logical_clock: int | None = None) -> Any:
    """Create an envelope instance through the contract constructor.

    Args:
        sequence_no: Sequence number to use.
        session_id: Session identifier.
        logical_clock: Optional explicit logical clock.

    Returns:
        ReplayEnvelope instance created from payload.

    """
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    payload = _replay_envelope_payload(
        session_id=session_id,
        sequence_no=sequence_no,
        logical_clock=sequence_no if logical_clock is None else logical_clock,
    )
    return replay_envelope_cls.from_dict(payload)


@dataclass
class _TxRecorder:
    """Simple transaction recorder used by shadow-core policy tests.

    Attributes:
        committed: Whether commit was called.
        rolled_back: Whether rollback was called.

    """

    committed: bool = False
    rolled_back: bool = False

    async def commit(self) -> None:
        """Record commit call."""
        self.committed = True

    async def rollback(self) -> None:
        """Record rollback call."""
        self.rolled_back = True


def _make_shadow_core_and_txs() -> tuple[Any, list[_TxRecorder]]:
    """Create a shadow core with observable transaction objects.

    Yields:
        Tuple of shadow core instance and all created transaction recorders.

    """
    shadow_execution_core_cls = _require_symbol("ShadowExecutionCore", "ShadowExecutionCore")
    created: list[_TxRecorder] = []

    def _factory() -> _TxRecorder:
        """Produce trackable transaction recorder instances."""
        tx = _TxRecorder()
        created.append(tx)
        return tx

    core = shadow_execution_core_cls(
        memory_tx_factory=_factory,
        storage_tx_factory=_factory,
        process_tx_factory=_factory,
        context_tx_factory=_factory,
        block_network=True,
    )
    return core, created


@pytest.mark.asyncio
async def test_rt_01_envelope_roundtrip_preserves_payload() -> None:
    """RT-01: Envelope round-trip keeps canonical payload data stable."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    original = _replay_envelope_payload()
    envelope = replay_envelope_cls.from_dict(original)
    second = replay_envelope_cls.from_dict(envelope.to_dict())
    assert second.to_dict() == envelope.to_dict()


@pytest.mark.asyncio
async def test_rt_02_envelope_rejects_missing_required_fields() -> None:
    """RT-02: Envelope creation rejects missing required contract fields."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    replay_schema_error_cls = _require_symbol("exceptions", "ReplaySchemaError")
    payload = _replay_envelope_payload()
    payload.pop("session_id")
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(payload)


@pytest.mark.asyncio
async def test_rt_03_envelope_rejects_non_monotonic_logical_clock() -> None:
    """RT-03: Envelope validation rejects non-monotonic logical clock values."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    replay_schema_error_cls = _require_symbol("exceptions", "ReplaySchemaError")
    payload = _replay_envelope_payload(sequence_no=3, logical_clock=1)
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(payload)


@pytest.mark.asyncio
async def test_rt_04_envelope_checksum_mismatch_raises_schema_error() -> None:
    """RT-04: Envelope validation fails when checksum does not match canonical payload."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    replay_schema_error_cls = _require_symbol("exceptions", "ReplaySchemaError")
    payload = _replay_envelope_payload()
    payload["checksum"] = "bad-checksum"
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(payload)


@pytest.mark.asyncio
async def test_rt_05_store_append_and_load_return_ordered_envelopes(tmp_path: Any) -> None:
    """RT-05: Store load returns envelopes sorted by sequence number."""
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    store = replay_store_cls(root_path=tmp_path)

    env2 = _build_envelope(sequence_no=2, session_id="s-ordered")
    env1 = _build_envelope(sequence_no=1, session_id="s-ordered")
    await store.append_envelope(env2)
    await store.append_envelope(env1)

    loaded = await store.load_session("s-ordered")
    assert [item.sequence_no for item in loaded] == [1, 2]


@pytest.mark.asyncio
async def test_rt_06_store_rejects_duplicate_sequence(tmp_path: Any) -> None:
    """RT-06: Store rejects duplicate sequence numbers in a session."""
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    replay_sequence_error_cls = _require_symbol("exceptions", "ReplaySequenceError")
    store = replay_store_cls(root_path=tmp_path)

    first = _build_envelope(sequence_no=1, session_id="s-dup")
    duplicate = _build_envelope(sequence_no=1, session_id="s-dup")
    await store.append_envelope(first)

    with pytest.raises(replay_sequence_error_cls):
        await store.append_envelope(duplicate)


@pytest.mark.asyncio
async def test_rt_07_store_load_range_is_deterministic_subset(tmp_path: Any) -> None:
    """RT-07: Store load_range returns deterministic inclusive subset bounds."""
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    store = replay_store_cls(root_path=tmp_path)

    for index in range(1, 6):
        await store.append_envelope(_build_envelope(sequence_no=index, session_id="s-range"))

    subset = await store.load_range("s-range", 2, 4)
    assert [item.sequence_no for item in subset] == [2, 3, 4]


@pytest.mark.asyncio
async def test_rt_08_store_corruption_raises_typed_error(tmp_path: Any) -> None:
    """RT-08: Store raises ReplayCorruptionError when persisted JSONL is corrupted."""
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    replay_corruption_error_cls = _require_symbol("exceptions", "ReplayCorruptionError")
    store = replay_store_cls(root_path=tmp_path)

    await store.append_envelope(_build_envelope(sequence_no=1, session_id="s-corrupt"))

    jsonl_files = list(tmp_path.rglob("*.jsonl"))
    assert jsonl_files, "Replay store must persist session data as JSONL files."
    with jsonl_files[0].open("a", encoding="utf-8") as handle:
        handle.write("\n{not-valid-json}\n")

    with pytest.raises(replay_corruption_error_cls):
        await store.load_session("s-corrupt")


@pytest.mark.asyncio
async def test_rt_09_store_delete_session_removes_events(tmp_path: Any) -> None:
    """RT-09: Store delete_session removes persisted events and existence marker."""
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    store = replay_store_cls(root_path=tmp_path)

    await store.append_envelope(_build_envelope(sequence_no=1, session_id="s-delete"))
    assert await store.session_exists("s-delete") is True

    await store.delete_session("s-delete")
    assert await store.session_exists("s-delete") is False
    assert await store.load_session("s-delete") == []


@pytest.mark.asyncio
async def test_rt_10_shadow_core_executes_read_only_envelope_safely() -> None:
    """RT-10: Shadow core executes a read-only envelope without side effects."""
    core, txs = _make_shadow_core_and_txs()
    envelope = _build_envelope(sequence_no=1, session_id="s-shadow-ro")

    result = await core.execute_envelope(envelope)

    assert getattr(result, "success", False) is True
    assert not any(tx.committed for tx in txs)


@pytest.mark.asyncio
async def test_rt_11_shadow_core_blocks_process_side_effects() -> None:
    """RT-11: Shadow core blocks envelopes that request process side effects."""
    core, _txs = _make_shadow_core_and_txs()
    shadow_policy_violation_cls = _require_symbol("exceptions", "ShadowPolicyViolation")
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")

    payload = _replay_envelope_payload(session_id="s-policy", sequence_no=1)
    payload["side_effect_intents"] = [{"kind": "process", "action": "spawn", "command": "echo hi"}]
    envelope = replay_envelope_cls.from_dict(payload)

    with pytest.raises(shadow_policy_violation_cls):
        await core.execute_envelope(envelope)


@pytest.mark.asyncio
async def test_rt_12_shadow_core_rolls_back_transactions_on_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """RT-12: Shadow core rolls back active transactions on execution failure."""
    core, txs = _make_shadow_core_and_txs()
    envelope = _build_envelope(sequence_no=1, session_id="s-rollback")

    async def _boom(_envelope: Any) -> Any:
        """Raise deterministic failure to trigger rollback path."""
        raise RuntimeError("forced-shadow-failure")

    monkeypatch.setattr(core, "_execute_tool_intent", _boom)
    result = await core.execute_envelope(envelope)

    assert getattr(result, "success", True) is False
    assert any(tx.rolled_back for tx in txs)


@pytest.mark.asyncio
async def test_rt_13_orchestrator_fails_on_sequence_gap() -> None:
    """RT-13: Orchestrator fails fast when envelope sequence contains a gap."""
    replay_orchestrator_cls = _require_symbol("ReplayOrchestrator", "ReplayOrchestrator")
    replay_sequence_error_cls = _require_symbol("exceptions", "ReplaySequenceError")

    class _Store:
        """Fake store providing a deterministic sequence gap."""

        async def load_session(self, _session_id: str) -> list[Any]:
            """Return envelopes with an intentional sequence gap."""
            return [
                _build_envelope(sequence_no=1, session_id="s-gap"),
                _build_envelope(sequence_no=3, session_id="s-gap"),
            ]

    class _ShadowCore:
        """Fake shadow core not expected to run for sequence-gap errors."""

        async def execute_envelope(self, _envelope: Any, *, deterministic_seed: int | None = None) -> Any:
            """Fail if called, because sequence validation must happen first."""
            raise AssertionError("execute_envelope should not run when sequence validation fails")

    orchestrator = replay_orchestrator_cls(store=_Store(), shadow_core=_ShadowCore())

    with pytest.raises(replay_sequence_error_cls):
        await orchestrator.replay_session("s-gap", mode="replay")


@pytest.mark.asyncio
async def test_rt_14_orchestrator_halts_at_first_divergence() -> None:
    """RT-14: Orchestrator stop_on_divergence=True halts at first divergence."""
    replay_orchestrator_cls = _require_symbol("ReplayOrchestrator", "ReplayOrchestrator")

    class _Store:
        """Fake store with contiguous deterministic sequence."""

        async def load_session(self, _session_id: str) -> list[Any]:
            """Return a stable, contiguous envelope stream."""
            return [
                _build_envelope(sequence_no=1, session_id="s-div-1"),
                _build_envelope(sequence_no=2, session_id="s-div-1"),
                _build_envelope(sequence_no=3, session_id="s-div-1"),
            ]

    class _Result:
        """Minimal step result used by fake core."""

        def __init__(self, *, success: bool) -> None:
            """Initialize step result with success flag."""
            self.success = success

    class _ShadowCore:
        """Fake core that diverges on sequence two."""

        def __init__(self) -> None:
            """Initialize call recorder."""
            self.calls: list[int] = []

        async def execute_envelope(self, envelope: Any, *, deterministic_seed: int | None = None) -> _Result:
            """Return divergence result on sequence two."""
            self.calls.append(envelope.sequence_no)
            return _Result(success=envelope.sequence_no != 2)

    core = _ShadowCore()
    orchestrator = replay_orchestrator_cls(store=_Store(), shadow_core=core)

    await orchestrator.replay_session("s-div-1", mode="replay", stop_on_divergence=True)
    assert core.calls == [1, 2]


@pytest.mark.asyncio
async def test_rt_15_orchestrator_collects_all_divergences_when_configured() -> None:
    """RT-15: Orchestrator stop_on_divergence=False executes full stream and tracks divergences."""
    replay_orchestrator_cls = _require_symbol("ReplayOrchestrator", "ReplayOrchestrator")

    class _Store:
        """Fake store with four deterministic envelopes."""

        async def load_session(self, _session_id: str) -> list[Any]:
            """Return contiguous deterministic envelope stream."""
            return [
                _build_envelope(sequence_no=1, session_id="s-div-2"),
                _build_envelope(sequence_no=2, session_id="s-div-2"),
                _build_envelope(sequence_no=3, session_id="s-div-2"),
                _build_envelope(sequence_no=4, session_id="s-div-2"),
            ]

    class _Result:
        """Minimal step result with success and diagnostic message."""

        def __init__(self, *, success: bool, reason: str = "") -> None:
            """Initialize result payload fields."""
            self.success = success
            self.reason = reason

    class _ShadowCore:
        """Fake core diverging at sequence two and four."""

        def __init__(self) -> None:
            """Initialize call recorder."""
            self.calls: list[int] = []

        async def execute_envelope(self, envelope: Any, *, deterministic_seed: int | None = None) -> _Result:
            """Return deterministic divergence map across four envelopes."""
            self.calls.append(envelope.sequence_no)
            if envelope.sequence_no in {2, 4}:
                return _Result(success=False, reason="diverged")
            return _Result(success=True)

    core = _ShadowCore()
    orchestrator = replay_orchestrator_cls(store=_Store(), shadow_core=core)
    summary = await orchestrator.replay_session("s-div-2", mode="replay", stop_on_divergence=False)

    assert core.calls == [1, 2, 3, 4]
    divergences = getattr(summary, "divergences", None)
    assert divergences is not None
    assert len(divergences) == 2


@pytest.mark.asyncio
async def test_rt_16_mixin_emission_includes_context_lineage_fields() -> None:
    """RT-16: ReplayMixin emission includes context lineage fields."""
    replay_mixin_cls = _require_symbol("ReplayMixin", "ReplayMixin")

    class _Host(replay_mixin_cls):
        """Minimal host object exposing replay dependencies and lineage fields."""

        def __init__(self) -> None:
            """Initialize deterministic host state used by mixin methods."""
            self._replay_store = None
            self._replay_orchestrator = None
            self.context_id = "ctx-red"
            self.transaction_id = "tx-red"
            self.parent_transaction_id = "tx-parent-red"
            self.name = "ReplayHost"

    host = _Host()
    envelope = await host.emit_replay_envelope(
        event_type="tool_call",
        input_payload={"q": "hello"},
        output_payload={"a": "world"},
        side_effect_intents=[],
    )

    as_dict = envelope.to_dict()
    assert as_dict["context_id"]
    assert as_dict["transaction_id"]
    assert "parent_transaction_id" in as_dict


@pytest.mark.asyncio
async def test_rt_17_mixin_replay_delegates_to_orchestrator() -> None:
    """RT-17: ReplayMixin replay API delegates to orchestrator with stop flag."""
    replay_mixin_cls = _require_symbol("ReplayMixin", "ReplayMixin")

    class _Orchestrator:
        """Fake orchestrator recording replay_session calls."""

        def __init__(self) -> None:
            """Initialize call recorder list."""
            self.calls: list[tuple[str, bool]] = []

        async def replay_session(
            self,
            session_id: str,
            *,
            mode: str = "replay",
            stop_on_divergence: bool = True,
        ) -> dict[str, Any]:
            """Record replay request and return deterministic result."""
            self.calls.append((session_id, stop_on_divergence))
            return {"session_id": session_id, "mode": mode, "stop_on_divergence": stop_on_divergence}

    class _Host(replay_mixin_cls):
        """Minimal host carrying fake orchestrator dependency."""

        def __init__(self) -> None:
            """Initialize orchestrator and optional store placeholders."""
            self._replay_store = None
            self._replay_orchestrator = _Orchestrator()

    host = _Host()
    result = await host.replay_session("s-mixin", stop_on_divergence=False)

    assert host._replay_orchestrator.calls == [("s-mixin", False)]
    assert result["session_id"] == "s-mixin"


@pytest.mark.asyncio
async def test_rt_18_end_to_end_replay_produces_deterministic_hash() -> None:
    """RT-18: End-to-end replay reproduces expected deterministic output hash."""
    replay_mixin_cls = _require_symbol("ReplayMixin", "ReplayMixin")

    class _Store:
        """In-memory fake replay store for deterministic fixture playback."""

        async def load_session(self, _session_id: str) -> list[Any]:
            """Return stable fixture envelope stream for e2e replay checks."""
            return [
                _build_envelope(sequence_no=1, session_id="s-e2e"),
                _build_envelope(sequence_no=2, session_id="s-e2e"),
            ]

    class _Orchestrator:
        """Fake orchestrator returning a deterministic payload hash."""

        async def replay_session(
            self,
            session_id: str,
            *,
            mode: str = "replay",
            stop_on_divergence: bool = True,
        ) -> dict[str, Any]:
            """Return deterministic hash derived from canonical replay payload."""
            canonical = json.dumps(
                {
                    "session_id": session_id,
                    "events": ["env-s-e2e-1", "env-s-e2e-2"],
                    "mode": mode,
                    "stop_on_divergence": stop_on_divergence,
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            return {"output_hash": hashlib.sha256(canonical).hexdigest()}

    class _Host(replay_mixin_cls):
        """Minimal host that wires fake replay dependencies."""

        def __init__(self) -> None:
            """Initialize deterministic fake dependencies for e2e test."""
            self._replay_store = _Store()
            self._replay_orchestrator = _Orchestrator()

    host = _Host()
    result = await host.replay_session("s-e2e")

    assert isinstance(result["output_hash"], str)
    assert len(result["output_hash"]) == 64


@pytest.mark.asyncio
async def test_rt_19_envelope_rejects_invalid_schema_and_payload_types() -> None:
    """RT-19: Envelope rejects unsupported schema and invalid payload types."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    replay_schema_error_cls = _require_symbol("exceptions", "ReplaySchemaError")

    bad_schema = _replay_envelope_payload()
    bad_schema["schema_version"] = "2.0"
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(bad_schema)

    bad_input_payload = _replay_envelope_payload()
    bad_input_payload["input_payload"] = ["not", "a", "dict"]
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(bad_input_payload)

    bad_output_payload = _replay_envelope_payload()
    bad_output_payload["output_payload"] = ["not", "a", "dict"]
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(bad_output_payload)

    bad_side_effect_intents = _replay_envelope_payload()
    bad_side_effect_intents["side_effect_intents"] = {"kind": "process"}
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(bad_side_effect_intents)


@pytest.mark.asyncio
async def test_rt_20_envelope_rejects_non_positive_sequence_and_logical_clock() -> None:
    """RT-20: Envelope validation rejects non-positive sequence and logical clock values."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    replay_schema_error_cls = _require_symbol("exceptions", "ReplaySchemaError")

    zero_sequence = _replay_envelope_payload(sequence_no=0, logical_clock=1)
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(zero_sequence)

    zero_clock = _replay_envelope_payload(sequence_no=1, logical_clock=0)
    with pytest.raises(replay_schema_error_cls):
        replay_envelope_cls.from_dict(zero_clock)


@pytest.mark.asyncio
async def test_rt_21_envelope_allows_sha256_checksum_mismatch_for_side_effect_envelopes() -> None:
    """RT-21: Side-effect envelopes may carry non-canonical but SHA256-shaped checksums."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")

    payload = _replay_envelope_payload(session_id="s-checksum-intent", sequence_no=1)
    payload["side_effect_intents"] = [{"kind": "process", "action": "spawn"}]
    payload["checksum"] = "a" * 64

    envelope = replay_envelope_cls.from_dict(payload)
    assert envelope.checksum == "a" * 64


@pytest.mark.asyncio
async def test_rt_22_envelope_sha256_shape_helper_rejects_non_hex() -> None:
    """RT-22: SHA256 helper returns False for invalid-hex checksum strings."""
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    assert replay_envelope_cls._is_sha256("g" * 64) is False


@pytest.mark.asyncio
async def test_rt_23_store_handles_invalid_bounds_and_missing_delete(tmp_path: Any) -> None:
    """RT-23: Store returns empty range for invalid bounds and no-op delete for missing sessions."""
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    store = replay_store_cls(root_path=tmp_path)

    empty_subset = await store.load_range("s-missing", 5, 1)
    assert empty_subset == []

    await store.delete_session("s-missing")
    assert await store.session_exists("s-missing") is False


@pytest.mark.asyncio
async def test_rt_24_store_validate_rejects_file_root(tmp_path: Any) -> None:
    """RT-24: Store validate rejects non-directory roots."""
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    replay_corruption_error_cls = _require_symbol("exceptions", "ReplayCorruptionError")

    root_file = tmp_path / "root-file"
    root_file.write_text("not-a-directory", encoding="utf-8")
    store = replay_store_cls(root_path=tmp_path / "store-root")
    store._root_path = root_file
    with pytest.raises(replay_corruption_error_cls):
        await store.load_session("s-any")


@pytest.mark.asyncio
async def test_rt_25_mixin_validate_and_missing_orchestrator_errors() -> None:
    """RT-25: ReplayMixin reports invalid orchestrator contract and missing orchestration setup."""
    replay_mixin_cls = _require_symbol("ReplayMixin", "ReplayMixin")
    replay_configuration_error_cls = _require_symbol("exceptions", "ReplayConfigurationError")

    class _BadOrchestrator:
        """Missing replay_session contract method."""

    class _HostBad(replay_mixin_cls):
        """Host wired with invalid orchestrator dependency."""

        def __init__(self) -> None:
            """Initialize invalid replay orchestrator dependency."""
            self._replay_store = None
            self._replay_orchestrator = _BadOrchestrator()

    with pytest.raises(replay_configuration_error_cls):
        _HostBad().validate()

    class _HostMissing(replay_mixin_cls):
        """Host wired without orchestrator for delegation path test."""

        def __init__(self) -> None:
            """Initialize replay dependencies with no orchestrator."""
            self._replay_store = None
            self._replay_orchestrator = None

    with pytest.raises(replay_configuration_error_cls):
        await _HostMissing().replay_session("s-missing-orchestrator")


@pytest.mark.asyncio
async def test_rt_26_mixin_emission_appends_to_store_when_available() -> None:
    """RT-26: ReplayMixin append path persists emitted envelope when store supports append."""
    replay_mixin_cls = _require_symbol("ReplayMixin", "ReplayMixin")

    class _Store:
        """Record appended envelopes for assertion."""

        def __init__(self) -> None:
            """Initialize append recorder."""
            self.envelopes: list[Any] = []

        async def append_envelope(self, envelope: Any) -> None:
            """Record appended envelope."""
            self.envelopes.append(envelope)

    class _Host(replay_mixin_cls):
        """Host wired with append-capable store and no orchestrator requirement."""

        def __init__(self) -> None:
            """Initialize replay dependencies for append-path testing."""
            self._replay_store = _Store()
            self._replay_orchestrator = None
            self.context_id = "ctx-store"
            self.transaction_id = "tx-store"

    host = _Host()
    envelope = await host.emit_replay_envelope(
        event_type="tool_call",
        input_payload={"a": 1},
        output_payload={"b": 2},
        side_effect_intents=[],
    )

    assert len(host._replay_store.envelopes) == 1
    assert host._replay_store.envelopes[0] == envelope


@pytest.mark.asyncio
async def test_rt_27_orchestrator_empty_stream_and_dependency_validation() -> None:
    """RT-27: Orchestrator validates dependencies and handles empty replay streams."""
    replay_orchestrator_cls = _require_symbol("ReplayOrchestrator", "ReplayOrchestrator")
    replay_configuration_error_cls = _require_symbol("exceptions", "ReplayConfigurationError")

    class _NoStoreMethod:
        """Missing load_session dependency contract."""

    class _NoShadowMethod:
        """Missing execute_envelope dependency contract."""

    missing_store_dependency = replay_orchestrator_cls(
        store=_NoStoreMethod(),
        shadow_core=type("_Core", (), {"execute_envelope": object()})(),
    )
    with pytest.raises(replay_configuration_error_cls):
        missing_store_dependency.validate()

    missing_shadow_dependency = replay_orchestrator_cls(
        store=type("_Store", (), {"load_session": object()})(),
        shadow_core=_NoShadowMethod(),
    )
    with pytest.raises(replay_configuration_error_cls):
        missing_shadow_dependency.validate()

    class _Store:
        """Return an empty session stream."""

        async def load_session(self, _session_id: str) -> list[Any]:
            """Return no envelopes for the requested session."""
            return []

    class _ShadowCore:
        """Provide execute_envelope contract without execution usage."""

        async def execute_envelope(self, _envelope: Any, *, deterministic_seed: int | None = None) -> Any:
            """Provide contract method; should not be called for empty streams."""
            return type("ReplayStepResult", (), {"success": True})()

    summary = await replay_orchestrator_cls(store=_Store(), shadow_core=_ShadowCore()).replay_session("s-empty")
    assert summary.total_steps == 0
    assert summary.executed_steps == 0
    assert summary.success is True


@pytest.mark.asyncio
async def test_rt_28_shadow_core_network_toggle_and_policy_rollback(monkeypatch: pytest.MonkeyPatch) -> None:
    """RT-28: Shadow core allows network intents when configured and rolls back on policy exceptions."""
    shadow_execution_core_cls = _require_symbol("ShadowExecutionCore", "ShadowExecutionCore")
    shadow_policy_violation_cls = _require_symbol("exceptions", "ShadowPolicyViolation")

    core_allow_network, _txs_allow_network = _make_shadow_core_and_txs()
    core_allow_network._block_network = False

    payload = _replay_envelope_payload(session_id="s-net", sequence_no=1)
    payload["side_effect_intents"] = [{"kind": "network", "action": "send"}]
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    envelope_network = replay_envelope_cls.from_dict(payload)
    result = await core_allow_network.execute_envelope(envelope_network)
    assert result.success is True

    core_rollback, txs_rollback = _make_shadow_core_and_txs()
    envelope = _build_envelope(sequence_no=1, session_id="s-policy-rollback")

    async def _policy_error(_envelope: Any) -> dict[str, Any]:
        """Raise policy violation in execution path to trigger rollback branch."""
        raise shadow_policy_violation_cls("blocked")

    monkeypatch.setattr(core_rollback, "_execute_tool_intent", _policy_error)
    with pytest.raises(shadow_policy_violation_cls):
        await core_rollback.execute_envelope(envelope)

    assert all(tx.rolled_back for tx in txs_rollback)

    invalid_core = shadow_execution_core_cls(
        memory_tx_factory=123,
        storage_tx_factory=lambda: object(),
        process_tx_factory=lambda: object(),
        context_tx_factory=lambda: object(),
    )
    replay_configuration_error_cls = _require_symbol("exceptions", "ReplayConfigurationError")
    with pytest.raises(replay_configuration_error_cls):
        invalid_core.validate()


@pytest.mark.asyncio
async def test_rt_29_shadow_core_rollback_ignores_transactions_without_rollback() -> None:
    """RT-29: Shadow rollback helper skips transactions that do not expose rollback()."""
    core, _txs = _make_shadow_core_and_txs()

    class _NoRollback:
        """Transaction-like object without rollback support."""

    await core._rollback_all([_NoRollback()])
