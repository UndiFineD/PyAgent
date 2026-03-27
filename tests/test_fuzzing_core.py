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

"""Red-phase behavior tests for prj0000088 fuzzing core contracts.

These tests intentionally fail until `src.core.fuzzing` contract modules are
implemented. Failures are explicit behavior failures, not import-time crashes.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest


def _require_symbol(module_name: str, symbol_name: str) -> Any:
    """Import a fuzzing symbol and fail with a behavior-focused message.

    Args:
        module_name: Fuzzing module filename without extension.
        symbol_name: Required exported symbol name.

    Returns:
        Imported symbol object.

    """
    module_path = f"src.core.fuzzing.{module_name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing fuzzing behavior module '{module_path}'. "
            "Implement fuzzing contracts before satisfying red-phase tests.",
            pytrace=False,
        )
        raise AssertionError("Unreachable after pytest.fail") from exc

    if not hasattr(module, symbol_name):
        pytest.fail(
            f"Module '{module_path}' does not expose required symbol '{symbol_name}'.",
            pytrace=False,
        )

    return getattr(module, symbol_name)


def _build_case(
    *,
    case_id: str = "case-001",
    target: str = "http://127.0.0.1:8080",
    payload: bytes = b"AAAA",
    operator: str = "bit_flip",
    seed: int = 7,
    corpus_index: int = 0,
) -> Any:
    """Construct a canonical fuzz case using the contract constructor.

    Args:
        case_id: Deterministic case identifier.
        target: Fuzz target URL.
        payload: Case payload bytes.
        operator: Mutation operator name.
        seed: Mutation seed value.
        corpus_index: Corpus index used to build the case.

    Returns:
        FuzzCase instance.

    """
    fuzz_case_cls = _require_symbol("FuzzCase", "FuzzCase")
    return fuzz_case_cls(
        case_id=case_id,
        target=target,
        payload=payload,
        operator=operator,
        seed=seed,
        corpus_index=corpus_index,
    )


def test_test_01_policy_violation_exception_typing() -> None:
    """TEST-01: Policy violation exception is typed and domain-specific."""
    base_error = _require_symbol("exceptions", "FuzzingError")
    policy_error = _require_symbol("exceptions", "FuzzPolicyViolation")
    assert issubclass(policy_error, base_error)


def test_test_02_execution_and_config_exception_typing() -> None:
    """TEST-02: Config and execution errors inherit from shared fuzz base error."""
    base_error = _require_symbol("exceptions", "FuzzingError")
    config_error = _require_symbol("exceptions", "FuzzConfigurationError")
    execution_error = _require_symbol("exceptions", "FuzzExecutionError")
    assert issubclass(config_error, base_error)
    assert issubclass(execution_error, base_error)


def test_test_03_fuzz_case_immutability_contract() -> None:
    """TEST-03: FuzzCase is immutable after construction."""
    case = _build_case()
    with pytest.raises((AttributeError, TypeError)):
        case.payload = b"BBBB"


def test_test_04_fuzz_case_replay_key_is_deterministic() -> None:
    """TEST-04: FuzzCase replay key is deterministic for identical input."""
    left = _build_case(case_id="case-004")
    right = _build_case(case_id="case-004")
    assert left.replay_key == right.replay_key


def test_test_05_fuzz_result_case_typing_and_state() -> None:
    """TEST-05: Per-case result exposes typed status fields."""
    case_result_cls = _require_symbol("FuzzResult", "FuzzCaseResult")
    case = _build_case(case_id="case-005")
    item = case_result_cls(case=case, status="crash", duration_ms=11, bytes_sent=len(case.payload), error=None)
    assert item.status == "crash"
    assert item.bytes_sent == len(case.payload)


def test_test_06_fuzz_result_campaign_summary_counts() -> None:
    """TEST-06: Campaign summary counts are deterministic and complete."""
    case_result_cls = _require_symbol("FuzzResult", "FuzzCaseResult")
    campaign_cls = _require_symbol("FuzzResult", "FuzzCampaignResult")
    case = _build_case(case_id="case-006")
    results = [
        case_result_cls(case=case, status="success", duration_ms=1, bytes_sent=4, error=None),
        case_result_cls(case=case, status="policy_blocked", duration_ms=1, bytes_sent=0, error="blocked"),
    ]
    campaign = campaign_cls.from_case_results(results)
    assert campaign.summary_counts["success"] == 1
    assert campaign.summary_counts["policy_blocked"] == 1


def test_test_07_safety_policy_rejects_non_local_target() -> None:
    """TEST-07: Safety policy rejects non-local or non-loopback targets."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    policy_error = _require_symbol("exceptions", "FuzzPolicyViolation")
    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip", "byte_insert"},
        max_cases=32,
        max_payload_bytes=256,
        max_total_bytes=4096,
        max_duration_seconds=30,
    )
    with pytest.raises(policy_error):
        policy.validate_target("https://example.com")


def test_test_08_safety_policy_rejects_disallowed_operator() -> None:
    """TEST-08: Safety policy rejects operators outside allowlist."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    policy_error = _require_symbol("exceptions", "FuzzPolicyViolation")
    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip", "byte_insert"},
        max_cases=16,
        max_payload_bytes=128,
        max_total_bytes=1024,
        max_duration_seconds=10,
    )
    with pytest.raises(policy_error):
        policy.validate_operator("sql_injection")


def test_test_09_safety_policy_enforces_budget_limits() -> None:
    """TEST-09: Safety policy budget checks reject oversized campaigns."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    policy_error = _require_symbol("exceptions", "FuzzPolicyViolation")
    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip"},
        max_cases=8,
        max_payload_bytes=64,
        max_total_bytes=256,
        max_duration_seconds=5,
    )
    with pytest.raises(policy_error):
        policy.enforce_budget(planned_cases=9, planned_total_bytes=180, planned_duration_seconds=3)


def test_test_10_fuzz_corpus_normalizes_inputs_to_bytes() -> None:
    """TEST-10: Corpus normalizes text and bytes inputs into canonical bytes entries."""
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    corpus = corpus_cls(entries=["AA", b"BB"])
    assert corpus.get(0) == b"AA"
    assert corpus.get(1) == b"BB"


def test_test_11_fuzz_corpus_deduplicates_repeated_payloads() -> None:
    """TEST-11: Corpus removes duplicate payload entries deterministically."""
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    corpus = corpus_cls(entries=[b"AA", "AA", b"BB", b"AA"])
    assert corpus.size == 2


def test_test_12_fuzz_corpus_deterministic_indexed_selection() -> None:
    """TEST-12: Corpus indexed retrieval is deterministic and stable."""
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    corpus = corpus_cls(entries=[b"aa", b"bb", b"cc"])
    assert corpus.get(0) == b"aa"
    assert corpus.get(1) == b"bb"
    assert corpus.get(2) == b"cc"


def test_test_13_fuzz_mutator_registry_exposes_allowed_operators() -> None:
    """TEST-13: Mutator exposes a deterministic allowlisted operator registry."""
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    mutator = mutator_cls(seed=11)
    operators = mutator.available_operators()
    assert "bit_flip" in operators


def test_test_14_fuzz_mutator_seeded_deterministic_mutation() -> None:
    """TEST-14: Mutator output is deterministic for identical seed/operator/index."""
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    left = mutator_cls(seed=42)
    right = mutator_cls(seed=42)
    payload = b"A" * 16
    assert left.mutate(payload=payload, operator="bit_flip", corpus_index=0) == right.mutate(
        payload=payload,
        operator="bit_flip",
        corpus_index=0,
    )


def test_test_15_fuzz_mutator_output_bytes_and_bounded() -> None:
    """TEST-15: Mutator output remains bytes and respects bounded expansion."""
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    payload = b"abcde"
    result = mutator_cls(seed=21).mutate(payload=payload, operator="byte_insert", corpus_index=2)
    assert isinstance(result, bytes)
    assert len(result) <= len(payload) * 2 + 16


def test_test_16_engine_schedules_bounded_case_count() -> None:
    """TEST-16: Engine schedules no more than policy-constrained case count."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    engine_cls = _require_symbol("FuzzEngineCore", "FuzzEngineCore")

    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip"},
        max_cases=3,
        max_payload_bytes=128,
        max_total_bytes=1024,
        max_duration_seconds=30,
    )
    corpus = corpus_cls(entries=[b"a", b"b", b"c", b"d"])
    mutator = mutator_cls(seed=123)
    engine = engine_cls(policy=policy, corpus=corpus, mutator=mutator, seed=123)

    campaign = engine.schedule_cases(target="http://127.0.0.1:8080", operator="bit_flip", requested_cases=10)
    assert len(campaign) == 3


def test_test_17_engine_applies_policy_before_execution() -> None:
    """TEST-17: Engine validates policy constraints before running cases."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    engine_cls = _require_symbol("FuzzEngineCore", "FuzzEngineCore")
    policy_error = _require_symbol("exceptions", "FuzzPolicyViolation")

    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip"},
        max_cases=4,
        max_payload_bytes=128,
        max_total_bytes=1024,
        max_duration_seconds=30,
    )
    engine = engine_cls(
        policy=policy,
        corpus=corpus_cls(entries=[b"a"]),
        mutator=mutator_cls(seed=8),
        seed=8,
    )

    with pytest.raises(policy_error):
        engine.schedule_cases(target="https://example.com", operator="bit_flip", requested_cases=1)


def test_test_18_engine_replay_stable_ordering_and_case_ids() -> None:
    """TEST-18: Same seed and inputs produce stable case ordering and IDs."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    engine_cls = _require_symbol("FuzzEngineCore", "FuzzEngineCore")

    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip"},
        max_cases=4,
        max_payload_bytes=128,
        max_total_bytes=1024,
        max_duration_seconds=30,
    )
    corpus = corpus_cls(entries=[b"a", b"b", b"c"])

    engine_a = engine_cls(policy=policy, corpus=corpus, mutator=mutator_cls(seed=99), seed=99)
    engine_b = engine_cls(policy=policy, corpus=corpus, mutator=mutator_cls(seed=99), seed=99)

    left = engine_a.schedule_cases(target="http://127.0.0.1:8080", operator="bit_flip", requested_cases=3)
    right = engine_b.schedule_cases(target="http://127.0.0.1:8080", operator="bit_flip", requested_cases=3)

    assert [item.case_id for item in left] == [item.case_id for item in right]


@pytest.mark.parametrize(
    ("kwargs", "expected_message"),
    [
        ({"case_id": ""}, "case_id must be non-empty"),
        ({"target": ""}, "target must be non-empty"),
        ({"payload": "not-bytes"}, "payload must be bytes"),
        ({"operator": ""}, "operator must be non-empty"),
        ({"corpus_index": -1}, "corpus_index must be >= 0"),
    ],
)
def test_test_19_fuzz_case_validation_rejects_invalid_fields(
    kwargs: dict[str, object],
    expected_message: str,
) -> None:
    """TEST-19: FuzzCase rejects invalid constructor field values deterministically."""
    config_error = _require_symbol("exceptions", "FuzzConfigurationError")
    base: dict[str, object] = {
        "case_id": "case-019",
        "target": "http://127.0.0.1:8080",
        "payload": b"AA",
        "operator": "bit_flip",
        "seed": 1,
        "corpus_index": 0,
    }
    base.update(kwargs)

    fuzz_case_cls = _require_symbol("FuzzCase", "FuzzCase")
    with pytest.raises(config_error, match=expected_message):
        fuzz_case_cls(**base)


@pytest.mark.parametrize(
    ("kwargs", "expected_message"),
    [
        ({"allowed_hosts": set()}, "allowed_hosts must not be empty"),
        ({"allowed_operators": set()}, "allowed_operators must not be empty"),
        ({"max_cases": 0}, "max_cases must be > 0"),
        ({"max_payload_bytes": 0}, "max_payload_bytes must be > 0"),
        ({"max_total_bytes": 0}, "max_total_bytes must be > 0"),
        ({"max_duration_seconds": 0}, "max_duration_seconds must be > 0"),
    ],
)
def test_test_20_safety_policy_validate_rejects_invalid_config(
    kwargs: dict[str, object],
    expected_message: str,
) -> None:
    """TEST-20: Safety policy validate() rejects all invalid configuration branches."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    config_error = _require_symbol("exceptions", "FuzzConfigurationError")
    base: dict[str, object] = {
        "allowed_hosts": {"127.0.0.1", "localhost"},
        "allowed_operators": {"bit_flip", "byte_insert"},
        "max_cases": 4,
        "max_payload_bytes": 64,
        "max_total_bytes": 256,
        "max_duration_seconds": 5,
    }
    base.update(kwargs)

    with pytest.raises(config_error, match=expected_message):
        policy_cls(**base)


def test_test_21_safety_policy_payload_and_budget_guards() -> None:
    """TEST-21: Safety policy rejects invalid payload types/sizes and budget dimensions."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    policy_error = _require_symbol("exceptions", "FuzzPolicyViolation")
    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip", "byte_insert"},
        max_cases=8,
        max_payload_bytes=4,
        max_total_bytes=16,
        max_duration_seconds=3,
    )

    with pytest.raises(policy_error, match="payload must be bytes"):
        policy.validate_payload("nope")
    with pytest.raises(policy_error, match="payload exceeds max_payload_bytes"):
        policy.validate_payload(b"12345")
    with pytest.raises(policy_error, match="planned total bytes exceeds policy max_total_bytes"):
        policy.enforce_budget(planned_cases=2, planned_total_bytes=17, planned_duration_seconds=1)
    with pytest.raises(policy_error, match="planned duration exceeds policy max_duration_seconds"):
        policy.enforce_budget(planned_cases=2, planned_total_bytes=8, planned_duration_seconds=4)


def test_test_22_mutator_validation_and_unknown_operator_paths() -> None:
    """TEST-22: Mutator validates seed type and rejects unknown operator."""
    unknown_operator_error = _require_symbol("exceptions", "UnknownMutationOperatorError")
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")

    invalid = mutator_cls(seed="bad-seed")
    with pytest.raises(TypeError, match="seed must be an int"):
        invalid.validate()

    with pytest.raises(unknown_operator_error, match="Unknown mutation operator"):
        mutator_cls(seed=1).mutate(payload=b"abc", operator="not-real", corpus_index=0)


def test_test_23_mutator_empty_payload_branch_is_deterministic() -> None:
    """TEST-23: Empty payload path mutates deterministically from synthetic zero byte."""
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    left = mutator_cls(seed=55).mutate(payload=b"", operator="bit_flip", corpus_index=3)
    right = mutator_cls(seed=55).mutate(payload=b"", operator="bit_flip", corpus_index=3)

    assert left == right
    assert isinstance(left, bytes)
    assert len(left) == 1


def test_test_24_corpus_validate_and_type_guards() -> None:
    """TEST-24: Corpus validate() and normalize type checks hit negative branches."""
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    config_error = _require_symbol("exceptions", "FuzzConfigurationError")

    empty_corpus = corpus_cls(entries=[])
    with pytest.raises(config_error, match="corpus must contain at least one entry"):
        empty_corpus.validate()
    with pytest.raises(config_error, match="corpus entries must be str or bytes"):
        corpus_cls(entries=[123])


@pytest.mark.parametrize(
    ("kwargs", "expected_message"),
    [
        ({"status": ""}, "status must be non-empty"),
        ({"duration_ms": -1}, "duration_ms must be >= 0"),
        ({"bytes_sent": -1}, "bytes_sent must be >= 0"),
    ],
)
def test_test_25_case_result_validation_branches(
    kwargs: dict[str, object],
    expected_message: str,
) -> None:
    """TEST-25: FuzzCaseResult validation rejects invalid status/duration/bytes."""
    case_result_cls = _require_symbol("FuzzResult", "FuzzCaseResult")
    config_error = _require_symbol("exceptions", "FuzzConfigurationError")
    base: dict[str, object] = {
        "case": _build_case(case_id="case-025"),
        "status": "success",
        "duration_ms": 1,
        "bytes_sent": 1,
        "error": None,
    }
    base.update(kwargs)

    with pytest.raises(config_error, match=expected_message):
        case_result_cls(**base)


def test_test_26_campaign_result_validate_mismatch_branch() -> None:
    """TEST-26: Campaign result validate() rejects summary mismatch."""
    campaign_cls = _require_symbol("FuzzResult", "FuzzCampaignResult")
    case_result_cls = _require_symbol("FuzzResult", "FuzzCaseResult")
    config_error = _require_symbol("exceptions", "FuzzConfigurationError")
    item = case_result_cls(
        case=_build_case(case_id="case-026"),
        status="success",
        duration_ms=1,
        bytes_sent=1,
        error=None,
    )
    bad_campaign = campaign_cls(case_results=(item,), summary_counts={"crash": 1})

    with pytest.raises(config_error, match="summary_counts must match aggregate case statuses"):
        bad_campaign.validate()


def test_test_27_engine_schedule_zero_requested_returns_empty() -> None:
    """TEST-27: Engine returns empty schedule for non-positive requested case count."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    corpus_cls = _require_symbol("FuzzCorpus", "FuzzCorpus")
    mutator_cls = _require_symbol("FuzzMutator", "FuzzMutator")
    engine_cls = _require_symbol("FuzzEngineCore", "FuzzEngineCore")

    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip"},
        max_cases=3,
        max_payload_bytes=128,
        max_total_bytes=1024,
        max_duration_seconds=30,
    )
    engine = engine_cls(policy=policy, corpus=corpus_cls(entries=[b"a"]), mutator=mutator_cls(seed=3), seed=3)

    assert engine.schedule_cases(target="http://127.0.0.1:8080", operator="bit_flip", requested_cases=0) == ()
