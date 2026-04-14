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
"""Red-phase integration and contract tests for immutable audit trail (prj0000084)."""

from __future__ import annotations

import json
import re
from importlib import import_module
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest


def _load_audit_symbol(module_name: str, symbol_name: str) -> Any:
    """Load a symbol from src.core.audit with assertion-style red failures.

    Args:
        module_name: Module name under src.core.audit.
        symbol_name: Symbol to retrieve from that module.

    Returns:
        The loaded symbol object.

    """
    try:
        module = import_module(f"src.core.audit.{module_name}")
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing audit module src.core.audit.{module_name}; implement prj0000084 modules first."
            f" Original error: {exc}",
            pytrace=False,
        )

    if not hasattr(module, symbol_name):
        pytest.fail(
            f"Missing symbol {symbol_name} in src.core.audit.{module_name};"
            " implement contract from design/plan artifacts.",
            pytrace=False,
        )
    return getattr(module, symbol_name)


def _new_event_payload() -> dict[str, Any]:
    """Build a deterministic baseline payload for event construction.

    Returns:
        Payload dictionary for canonicalization tests.

    """
    return {"alpha": 1, "beta": 2, "nested": {"k": "v"}}


def _make_event(payload: dict[str, Any] | None = None) -> Any:
    """Construct an AuditEvent instance using the contract field set.

    Args:
        payload: Optional payload override.

    Returns:
        A constructed AuditEvent.

    """
    audit_event_cls = _load_audit_symbol("AuditEvent", "AuditEvent")
    return audit_event_cls(
        event_id=str(uuid4()),
        event_type="transaction.commit",
        occurred_at_utc="2026-03-27T12:00:00Z",
        actor_id="agent:test",
        action="commit",
        target="memory",
        tx_id="tx-1",
        context_id="ctx-1",
        correlation_id="corr-1",
        payload=payload if payload is not None else _new_event_payload(),
    )


def _make_core(tmp_path: Path, *, fail_closed: bool = True) -> Any:
    """Create an AuditTrailCore bound to a temporary JSONL file.

    Args:
        tmp_path: pytest temporary path fixture.
        fail_closed: Desired fail-closed policy.

    Returns:
        Constructed AuditTrailCore instance.

    """
    audit_trail_core_cls = _load_audit_symbol("AuditTrailCore", "AuditTrailCore")
    audit_file = tmp_path / "audit.jsonl"
    return audit_trail_core_cls(str(audit_file), fail_closed=fail_closed)


def _audit_file_for(core: Any) -> Path:
    """Resolve the audit file path from a core instance.

    Args:
        core: AuditTrailCore instance.

    Returns:
        Path for the audit trail file.

    """
    if hasattr(core, "audit_file_path"):
        return Path(core.audit_file_path)
    if hasattr(core, "_audit_file_path"):
        return Path(core._audit_file_path)
    pytest.fail("AuditTrailCore must expose audit file path via audit_file_path or _audit_file_path.")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read JSONL records into dictionaries.

    Args:
        path: File path to read.

    Returns:
        List of decoded JSON objects.

    """
    if not path.exists():
        return []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [json.loads(line) for line in lines]


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write JSONL records back to file.

    Args:
        path: File path to write.
        records: JSON-serializable record dictionaries.

    """
    text = "\n".join(json.dumps(rec) for rec in records)
    if text:
        text += "\n"
    path.write_text(text, encoding="utf-8")


def _append_three(core: Any) -> list[str]:
    """Append three deterministic events and return event hashes.

    Args:
        core: AuditTrailCore instance.

    Returns:
        List of event hashes from append calls.

    """
    hashes: list[str] = []
    for index in range(1, 4):
        event = _make_event({"index": index, "kind": "baseline"})
        hashes.append(core.append_event(event))
    return hashes


def test_event_canonical_dict_contains_required_keys_and_schema_version() -> None:
    """U01: Canonical event dict includes required keys and schema_version=1."""
    event = _make_event()
    canonical = event.to_canonical_dict()
    required = {
        "event_id",
        "event_type",
        "occurred_at_utc",
        "actor_id",
        "action",
        "target",
        "tx_id",
        "context_id",
        "correlation_id",
        "payload",
        "schema_version",
    }
    assert required.issubset(set(canonical.keys()))
    assert canonical["schema_version"] == 1


def test_event_canonical_dict_stable_across_payload_insertion_order() -> None:
    """U02: Canonical representation is stable for equivalent payload key orderings."""
    payload_a = {"alpha": 1, "beta": 2, "gamma": {"x": 1, "y": 2}}
    payload_b = {"beta": 2, "gamma": {"y": 2, "x": 1}, "alpha": 1}
    event_a = _make_event(payload_a)
    event_b = _make_event(payload_b)
    assert event_a.to_canonical_dict() == event_b.to_canonical_dict()


def test_hasher_canonical_event_bytes_deterministic_for_same_event() -> None:
    """U03: canonical_event_bytes must be deterministic for equivalent events."""
    audit_hasher = _load_audit_symbol("AuditHasher", "AuditHasher")
    payload = {"alpha": 1, "nested": {"b": 2, "a": 1}}
    event_a = _make_event(payload)
    event_b = _make_event({"nested": {"a": 1, "b": 2}, "alpha": 1})
    bytes_a = audit_hasher.canonical_event_bytes(event_a)
    bytes_b = audit_hasher.canonical_event_bytes(event_b)
    assert bytes_a == bytes_b
    assert audit_hasher.canonical_event_bytes(event_a) == bytes_a


def test_compute_event_hash_returns_64_lowercase_hex() -> None:
    """U04: compute_event_hash returns 64-char lowercase hex hash."""
    audit_hasher = _load_audit_symbol("AuditHasher", "AuditHasher")
    event = _make_event()
    payload_bytes = audit_hasher.canonical_event_bytes(event)
    event_hash = audit_hasher.compute_event_hash("0" * 64, payload_bytes)
    assert isinstance(event_hash, str)
    assert re.fullmatch(r"[0-9a-f]{64}", event_hash) is not None


def test_get_last_hash_returns_genesis_for_empty_and_latest_for_non_empty(tmp_path: Path) -> None:
    """U05: get_last_hash returns genesis for empty file and latest hash after appends."""
    core = _make_core(tmp_path)
    genesis = "0" * 64
    assert core.get_last_hash() == genesis

    first = core.append_event(_make_event({"step": 1}))
    second = core.append_event(_make_event({"step": 2}))
    assert first != second
    assert core.get_last_hash() == second


def test_mixin_emit_event_returns_none_when_core_not_configured() -> None:
    """U06: mixin emits None when host returns no configured core."""
    audit_trail_mixin_cls = _load_audit_symbol("AuditTrailMixin", "AuditTrailMixin")

    class _Host(audit_trail_mixin_cls):
        """Simple host that intentionally has no audit core."""

        def _get_audit_trail_core(self) -> Any:
            """Return no audit core to trigger null-path behavior."""
            return None

    host = _Host()
    result = host.audit_emit_event(
        event_type="transaction.commit",
        action="commit",
        payload={"ok": True},
    )
    assert result is None


def test_exception_hierarchy_preserves_specific_types_under_audittrailerror() -> None:
    """U07: audit exceptions inherit from AuditTrailError and retain subtype identity."""
    audit_trail_error = _load_audit_symbol("exceptions", "AuditTrailError")
    audit_serialization_error = _load_audit_symbol("exceptions", "AuditSerializationError")
    audit_chain_link_error = _load_audit_symbol("exceptions", "AuditChainLinkError")
    audit_integrity_error = _load_audit_symbol("exceptions", "AuditIntegrityError")
    audit_persistence_error = _load_audit_symbol("exceptions", "AuditPersistenceError")

    for exc_type in [
        audit_serialization_error,
        audit_chain_link_error,
        audit_integrity_error,
        audit_persistence_error,
    ]:
        try:
            raise exc_type("x")
        except audit_trail_error as caught:
            assert isinstance(caught, exc_type)


def test_append_event_uses_genesis_previous_hash_for_first_record(tmp_path: Path) -> None:
    """I01: first appended record must use genesis previous hash."""
    core = _make_core(tmp_path)
    core.append_event(_make_event({"order": 1}))
    records = _read_jsonl(_audit_file_for(core))
    assert len(records) == 1
    assert records[0]["previous_hash"] == "0" * 64


def test_append_event_links_previous_hash_to_prior_event_hash(tmp_path: Path) -> None:
    """I02: second record previous_hash equals first record event_hash."""
    core = _make_core(tmp_path)
    core.append_event(_make_event({"order": 1}))
    core.append_event(_make_event({"order": 2}))
    records = _read_jsonl(_audit_file_for(core))
    assert len(records) == 2
    assert records[1]["previous_hash"] == records[0]["event_hash"]


def test_append_event_dict_matches_equivalent_auditevent_hash(tmp_path: Path) -> None:
    """I03: append_event_dict and explicit AuditEvent must hash equivalently."""
    audit_trail_core_cls = _load_audit_symbol("AuditTrailCore", "AuditTrailCore")
    event_kwargs = {
        "event_type": "transaction.commit",
        "action": "commit",
        "payload": {"x": 1, "y": {"a": 1, "b": 2}},
        "actor_id": "agent:test",
        "target": "memory",
        "tx_id": "tx-42",
        "context_id": "ctx-42",
        "correlation_id": "corr-42",
        "occurred_at_utc": "2026-03-27T12:00:00Z",
        "event_id": "evt-42",
    }

    left_file = tmp_path / "left.jsonl"
    right_file = tmp_path / "right.jsonl"
    left_core = audit_trail_core_cls(str(left_file), fail_closed=True)
    right_core = audit_trail_core_cls(str(right_file), fail_closed=True)

    left_hash = left_core.append_event_dict(**event_kwargs)
    right_event = _make_event(event_kwargs["payload"])
    right_event = type(right_event)(
        event_id=event_kwargs["event_id"],
        event_type=event_kwargs["event_type"],
        occurred_at_utc=event_kwargs["occurred_at_utc"],
        actor_id=event_kwargs["actor_id"],
        action=event_kwargs["action"],
        target=event_kwargs["target"],
        tx_id=event_kwargs["tx_id"],
        context_id=event_kwargs["context_id"],
        correlation_id=event_kwargs["correlation_id"],
        payload=event_kwargs["payload"],
    )
    right_hash = right_core.append_event(right_event)

    assert left_hash == right_hash


def test_iter_records_preserves_append_order(tmp_path: Path) -> None:
    """I04: iter_records returns entries in append sequence order."""
    core = _make_core(tmp_path)
    actions = ["one", "two", "three"]
    for action in actions:
        event = _make_event({"action": action})
        rebuilt = type(event)(
            event_id=event.event_id,
            event_type=event.event_type,
            occurred_at_utc=event.occurred_at_utc,
            actor_id=event.actor_id,
            action=action,
            target=event.target,
            tx_id=event.tx_id,
            context_id=event.context_id,
            correlation_id=event.correlation_id,
            payload=event.payload,
        )
        core.append_event(rebuilt)

    records = core.iter_records()
    assert [r["action"] for r in records] == actions


def test_verify_file_valid_chain_with_three_events_returns_valid_result(tmp_path: Path) -> None:
    """I05: verifier accepts an untampered three-event chain."""
    core = _make_core(tmp_path)
    _append_three(core)
    result = core.verify_file()
    assert result.is_valid is True
    assert result.total_events == 3
    assert result.validated_events == 3
    assert result.error_code is None
    assert result.error_message is None


def test_verify_file_empty_chain_is_valid_and_deterministic(tmp_path: Path) -> None:
    """I06: empty audit file verifies as valid with deterministic counters."""
    core = _make_core(tmp_path)
    result = core.verify_file()
    assert result.is_valid is True
    assert result.total_events == 0
    assert result.validated_events == 0
    assert result.first_invalid_sequence is None


def test_verify_file_detects_tampered_payload_in_middle_record(tmp_path: Path) -> None:
    """N01: verifier reports invalid when middle payload is tampered post-write."""
    core = _make_core(tmp_path)
    _append_three(core)
    path = _audit_file_for(core)
    records = _read_jsonl(path)
    records[1]["payload"] = {"index": 2, "kind": "tampered"}
    _write_jsonl(path, records)

    result = core.verify_file()
    assert result.is_valid is False
    assert result.first_invalid_sequence == 2


def test_verify_file_detects_broken_previous_hash_link(tmp_path: Path) -> None:
    """N02: verifier rejects record with mismatched previous_hash linkage."""
    core = _make_core(tmp_path)
    _append_three(core)
    path = _audit_file_for(core)
    records = _read_jsonl(path)
    records[1]["previous_hash"] = "f" * 64
    _write_jsonl(path, records)

    result = core.verify_file()
    assert result.is_valid is False
    assert result.error_code is not None


def test_verify_file_detects_malformed_hash_format(tmp_path: Path) -> None:
    """N03: verifier rejects malformed hash values in audit records."""
    core = _make_core(tmp_path)
    _append_three(core)
    path = _audit_file_for(core)
    records = _read_jsonl(path)
    records[2]["event_hash"] = "not-a-sha256-hash"
    _write_jsonl(path, records)

    result = core.verify_file()
    assert result.is_valid is False
    assert result.error_code is not None


def test_verify_file_detects_malformed_json_line(tmp_path: Path) -> None:
    """N04: verifier rejects malformed JSON lines in audit file."""
    core = _make_core(tmp_path)
    _append_three(core)
    path = _audit_file_for(core)
    with path.open("a", encoding="utf-8") as handle:
        handle.write("{ this is : not valid json }\n")

    result = core.verify_file()
    assert result.is_valid is False
    assert result.error_code is not None


def test_fail_closed_true_raises_auditpersistenceerror_on_unwritable_path(tmp_path: Path) -> None:
    """N05: fail-closed append raises AuditPersistenceError when target path is unwritable."""
    audit_trail_core_cls = _load_audit_symbol("AuditTrailCore", "AuditTrailCore")
    audit_persistence_error = _load_audit_symbol("exceptions", "AuditPersistenceError")
    core = audit_trail_core_cls(str(tmp_path), fail_closed=True)

    with pytest.raises(audit_persistence_error):
        core.append_event(_make_event({"x": 1}))


def test_event_canonical_handles_nested_lists_and_dicts() -> None:
    """Cover canonicalization of nested list payload values."""
    event = _make_event({"items": [{"b": 2, "a": 1}, {"z": [3, {"k": "v"}]}]})
    canonical = event.to_canonical_dict()
    assert canonical["payload"] == {
        "items": [{"a": 1, "b": 2}, {"z": [3, {"k": "v"}]}],
    }


def test_event_to_canonical_rejects_unsupported_schema_version() -> None:
    """Unsupported schema versions raise AuditSerializationError."""
    audit_serialization_error = _load_audit_symbol("exceptions", "AuditSerializationError")
    event = _make_event()
    rebuilt = type(event)(
        event_id=event.event_id,
        event_type=event.event_type,
        occurred_at_utc=event.occurred_at_utc,
        actor_id=event.actor_id,
        action=event.action,
        target=event.target,
        tx_id=event.tx_id,
        context_id=event.context_id,
        correlation_id=event.correlation_id,
        payload=event.payload,
        schema_version=999,
    )
    with pytest.raises(audit_serialization_error):
        rebuilt.to_canonical_dict()


def test_event_from_json_dict_rejects_missing_key() -> None:
    """Missing required persisted fields raise AuditSerializationError."""
    audit_event_cls = _load_audit_symbol("AuditEvent", "AuditEvent")
    audit_serialization_error = _load_audit_symbol("exceptions", "AuditSerializationError")
    with pytest.raises(audit_serialization_error):
        audit_event_cls.from_json_dict(
            {
                "event_type": "x",
                "occurred_at_utc": "2026-03-27T12:00:00Z",
                "action": "act",
                "payload": {},
                "schema_version": 1,
            }
        )


def test_event_from_json_dict_rejects_invalid_payload_type() -> None:
    """Non-dictionary payload values are rejected."""
    audit_event_cls = _load_audit_symbol("AuditEvent", "AuditEvent")
    audit_serialization_error = _load_audit_symbol("exceptions", "AuditSerializationError")
    with pytest.raises(audit_serialization_error):
        audit_event_cls.from_json_dict(
            {
                "event_id": "evt-1",
                "event_type": "x",
                "occurred_at_utc": "2026-03-27T12:00:00Z",
                "action": "act",
                "payload": [1, 2, 3],
                "schema_version": 1,
            }
        )


def test_event_from_json_dict_rejects_non_integer_schema_version() -> None:
    """Schema version must be persisted as an integer."""
    audit_event_cls = _load_audit_symbol("AuditEvent", "AuditEvent")
    audit_serialization_error = _load_audit_symbol("exceptions", "AuditSerializationError")
    with pytest.raises(audit_serialization_error):
        audit_event_cls.from_json_dict(
            {
                "event_id": "evt-1",
                "event_type": "x",
                "occurred_at_utc": "2026-03-27T12:00:00Z",
                "action": "act",
                "payload": {},
                "schema_version": "1",
            }
        )


def test_append_event_returns_empty_string_when_fail_open_on_persistence_error(tmp_path: Path) -> None:
    """Fail-open mode returns empty hash when persistence fails."""
    audit_trail_core_cls = _load_audit_symbol("AuditTrailCore", "AuditTrailCore")
    core = audit_trail_core_cls(str(tmp_path), fail_closed=False)
    assert core.append_event(_make_event({"x": 1})) == ""


def test_append_event_returns_empty_string_when_hasher_raises_oserror(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Fail-open mode handles raw OSError from hashing path."""
    audit_hasher = _load_audit_symbol("AuditHasher", "AuditHasher")
    core = _make_core(tmp_path, fail_closed=False)

    def _raise_oserror(_: Any) -> bytes:
        raise OSError("boom")

    monkeypatch.setattr(audit_hasher, "canonical_event_bytes", _raise_oserror)
    assert core.append_event(_make_event()) == ""


def test_iter_records_skips_blank_lines(tmp_path: Path) -> None:
    """iter_records ignores empty/whitespace lines in JSONL files."""
    core = _make_core(tmp_path)
    path = _audit_file_for(core)
    path.write_text('\n{"event_hash":"a"}\n\n', encoding="utf-8")
    records = core.iter_records()
    assert len(records) == 1


def test_iter_records_rejects_non_object_json_line(tmp_path: Path) -> None:
    """iter_records raises AuditSerializationError for non-object JSON entries."""
    core = _make_core(tmp_path)
    path = _audit_file_for(core)
    path.write_text("[]\n", encoding="utf-8")
    audit_serialization_error = _load_audit_symbol("exceptions", "AuditSerializationError")
    with pytest.raises(audit_serialization_error):
        core.iter_records()


def test_iter_records_rejects_malformed_json_line(tmp_path: Path) -> None:
    """iter_records raises AuditSerializationError for malformed JSON."""
    core = _make_core(tmp_path)
    path = _audit_file_for(core)
    path.write_text("{bad json}\n", encoding="utf-8")
    audit_serialization_error = _load_audit_symbol("exceptions", "AuditSerializationError")
    with pytest.raises(audit_serialization_error):
        core.iter_records()


def test_verify_file_skips_blank_lines_between_records(tmp_path: Path) -> None:
    """verify_file ignores blank lines while validating sequence."""
    core = _make_core(tmp_path)
    _append_three(core)
    path = _audit_file_for(core)
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(f"\n{lines[0]}\n\n{lines[1]}\n{lines[2]}\n", encoding="utf-8")
    result = core.verify_file()
    assert result.is_valid is True
    assert result.validated_events == 3


def test_verify_file_detects_malformed_non_object_record(tmp_path: Path) -> None:
    """verify_file reports MALFORMED_RECORD for JSON values that are not objects."""
    core = _make_core(tmp_path)
    path = _audit_file_for(core)
    path.write_text("[]\n", encoding="utf-8")
    result = core.verify_file()
    assert result.is_valid is False
    assert result.error_code == "MALFORMED_RECORD"


def test_verify_file_detects_missing_hash_fields(tmp_path: Path) -> None:
    """verify_file reports HASH_FORMAT when hash fields are absent."""
    core = _make_core(tmp_path)
    _append_three(core)
    path = _audit_file_for(core)
    records = _read_jsonl(path)
    del records[0]["event_hash"]
    _write_jsonl(path, records)
    result = core.verify_file()
    assert result.is_valid is False
    assert result.error_code == "HASH_FORMAT"


def test_verify_file_detects_serialization_error_from_event_shape(tmp_path: Path) -> None:
    """verify_file reports SERIALIZATION when event fields are missing."""
    core = _make_core(tmp_path)
    _append_three(core)
    path = _audit_file_for(core)
    records = _read_jsonl(path)
    del records[1]["action"]
    _write_jsonl(path, records)
    result = core.verify_file()
    assert result.is_valid is False
    assert result.error_code == "SERIALIZATION"


def test_verify_file_reports_persistence_error_when_open_fails(tmp_path: Path) -> None:
    """verify_file reports PERSISTENCE when file open fails."""
    core = _make_core(tmp_path)

    class _BrokenPath:
        """Test double that simulates an unreadable audit file path."""

        def exists(self) -> bool:
            """Report the synthetic path as existing."""
            return True

        def open(self, *_args: Any, **_kwargs: Any) -> Any:
            """Always raise to simulate file open failure."""
            raise OSError("cannot open")

    core._path = _BrokenPath()
    result = core.verify_file()
    assert result.is_valid is False
    assert result.error_code == "PERSISTENCE"


def test_get_last_hash_falls_back_to_genesis_for_invalid_last_hash(tmp_path: Path) -> None:
    """Invalid tail hash values produce genesis fallback."""
    core = _make_core(tmp_path)
    _write_jsonl(_audit_file_for(core), [{"event_hash": "invalid-hash", "sequence": 1}])
    assert core.get_last_hash() == "0" * 64


def test_get_last_sequence_falls_back_to_record_count_when_non_integer(tmp_path: Path) -> None:
    """Non-integer sequence values fall back to len(records)."""
    core = _make_core(tmp_path)
    _write_jsonl(_audit_file_for(core), [{"event_hash": "a" * 64, "sequence": "x"}])
    assert core.get_last_sequence() == 1


def test_append_event_creates_missing_parent_directory(tmp_path: Path) -> None:
    """append_event creates parent directories before writing records."""
    audit_trail_core_cls = _load_audit_symbol("AuditTrailCore", "AuditTrailCore")
    file_path = tmp_path / "nested" / "audit" / "events.jsonl"
    core = audit_trail_core_cls(str(file_path), fail_closed=True)
    core.append_event(_make_event({"x": 1}))
    assert file_path.exists()


def test_append_record_wraps_oserror_as_auditpersistenceerror(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """_append_record converts raw OSError into AuditPersistenceError."""
    core = _make_core(tmp_path)
    audit_persistence_error = _load_audit_symbol("exceptions", "AuditPersistenceError")
    original_open = Path.open

    def _patched_open(path_obj: Path, *args: Any, **kwargs: Any) -> Any:
        if path_obj == core._path:
            raise OSError("forced open failure")
        return original_open(path_obj, *args, **kwargs)

    monkeypatch.setattr(Path, "open", _patched_open)
    with pytest.raises(audit_persistence_error):
        core._append_record({"a": 1})


def test_audittrailmixin_base_get_core_returns_none() -> None:
    """Base AuditTrailMixin hook returns None when not overridden."""
    audit_trail_mixin_cls = _load_audit_symbol("AuditTrailMixin", "AuditTrailMixin")
    assert audit_trail_mixin_cls()._get_audit_trail_core() is None


def test_audittrailmixin_returns_none_on_audittrailerror_from_core() -> None:
    """audit_emit_event handles AuditTrailError and returns None."""
    audit_trail_mixin_cls = _load_audit_symbol("AuditTrailMixin", "AuditTrailMixin")
    audit_persistence_error = _load_audit_symbol("exceptions", "AuditPersistenceError")

    class _FailingCore:
        """Test double that always raises an audit error."""

        def append_event_dict(self, **_kwargs: Any) -> str:
            """Raise a persistence error for mixin error-path coverage."""
            raise audit_persistence_error("nope")

    class _Host(audit_trail_mixin_cls):
        """Host that injects a failing audit core."""

        def _get_audit_trail_core(self) -> Any:
            """Return the failing core instance."""
            return _FailingCore()

    host = _Host()
    assert host.audit_emit_event(event_type="x", action="a", payload={}) is None


def test_audittrailmixin_success_and_failure_helpers_delegate_event_types() -> None:
    """audit_emit_success/failure use expected event_type values."""
    audit_trail_mixin_cls = _load_audit_symbol("AuditTrailMixin", "AuditTrailMixin")

    class _Core:
        """Test double that records append_event_dict payloads."""

        def __init__(self) -> None:
            """Initialize call capture list."""
            self.calls: list[dict[str, Any]] = []

        def append_event_dict(self, **kwargs: Any) -> str:
            """Record kwargs and return deterministic hash token."""
            self.calls.append(kwargs)
            return "a" * 64

    class _Host(audit_trail_mixin_cls):
        """Host that provides a recording core for helper delegation checks."""

        def __init__(self) -> None:
            """Attach a recording core instance."""
            self.core = _Core()

        def _get_audit_trail_core(self) -> Any:
            """Return the configured recording core."""
            return self.core

    host = _Host()
    success_hash = host.audit_emit_success("ok", {"status": "ok"})
    failure_hash = host.audit_emit_failure("bad", {"status": "bad"})
    assert success_hash == "a" * 64
    assert failure_hash == "a" * 64
    assert host.core.calls[0]["event_type"] == "audit.success"
    assert host.core.calls[1]["event_type"] == "audit.failure"


def test_validate_helpers_return_true_for_all_audit_modules() -> None:
    """Module/package validate() helpers all return True."""
    validators = [
        _load_audit_symbol("AuditEvent", "validate"),
        _load_audit_symbol("AuditHasher", "validate"),
        _load_audit_symbol("AuditTrailCore", "validate"),
        _load_audit_symbol("AuditTrailMixin", "validate"),
        _load_audit_symbol("AuditVerificationResult", "validate"),
        _load_audit_symbol("exceptions", "validate"),
    ]
    package_validate = import_module("src.core.audit").validate
    for validator in [*validators, package_validate]:
        assert validator() is True
