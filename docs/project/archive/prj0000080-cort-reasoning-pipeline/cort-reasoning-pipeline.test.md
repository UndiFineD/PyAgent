# cort-reasoning-pipeline — Test Artifacts

_Status: IN_PROGRESS_
_Tester: @5test | Updated: 2026-03-26_

## Test Plan

**Scope:** V1 unit tests for `src/core/reasoning/` — CortCore loop, EvaluationEngine
heuristic scorer, CortAgent orchestration + CortMixin injection.

**Framework:** pytest + pytest-asyncio (`asyncio_mode = strict`)

**Approach:** Red-phase — all three test files are written to import from
`src.core.reasoning` (does not yet exist) and fail at collection time with
`ModuleNotFoundError`. Complete, correct assertions drive the @6code implementation.

## Test Cases

| ID | Description | File | Status |
|---|---|---|---|
| TC-CC-01 | `test_cort_config_defaults` — DEFAULT_CORT_CONFIG has n_rounds=3, m_alternatives=3 | test_CortCore.py | RED |
| TC-CC-02 | `test_cort_config_cap_enforcement` — n_rounds=5, m_alternatives=4 raises CortLimitExceeded | test_CortCore.py | RED |
| TC-CC-03 | `test_cort_config_valid_cap` — n_rounds=3, m_alternatives=5 is valid | test_CortCore.py | RED |
| TC-CC-04 | `test_reasoning_chain_ordering` — higher score chain has larger .score value | test_CortCore.py | RED |
| TC-CC-05 | `test_cort_result_has_best_chain` — CortResult.best_chain is highest-scoring | test_CortCore.py | RED |
| TC-CC-06 | `test_cort_result_round_count` — CortResult.all_rounds len == n_rounds | test_CortCore.py | RED |
| TC-CC-07 | `test_cort_core_run_returns_cort_result` — run() returns CortResult | test_CortCore.py | RED |
| TC-CC-08 | `test_cort_core_calls_llm_n_times_m_alternatives` — 2×2=4 LLM calls | test_CortCore.py | RED |
| TC-CC-09 | `test_cort_core_temperature_schedule` — temperatures are monotonically non-decreasing | test_CortCore.py | RED |
| TC-CC-10 | `test_cort_recursion_guard` — nested CortCore.run raises CortRecursionError | test_CortCore.py | RED |
| TC-CC-11 | `test_cort_limit_exceeded` — n_rounds=4, m_alternatives=4 raises CortLimitExceeded | test_CortCore.py | RED |
| TC-EE-01 | `test_rubric_score_weighted_total` — all axes=1.0 → weighted_total==1.0 | test_EvaluationEngine.py | RED |
| TC-EE-02 | `test_rubric_score_weights` — individual weight verification (0.5/0.3/0.2) | test_EvaluationEngine.py | RED |
| TC-EE-03 | `test_correctness_penalizes_contradictions` — "that's wrong" lowers correctness | test_EvaluationEngine.py | RED |
| TC-EE-04 | `test_completeness_rewards_keyword_recall` — keyword-rich text scores higher | test_EvaluationEngine.py | RED |
| TC-EE-05 | `test_reasoning_depth_rewards_connectives` — "therefore", "because" boost depth | test_EvaluationEngine.py | RED |
| TC-EE-06 | `test_reasoning_depth_rewards_structure` — numbered list boosts depth score | test_EvaluationEngine.py | RED |
| TC-EE-07 | `test_select_best_returns_highest_score` — select_best chooses max-score chain | test_EvaluationEngine.py | RED |
| TC-EE-08 | `test_select_best_tie_breaks_by_depth` — equal total → lowest alternative_idx wins | test_EvaluationEngine.py | RED |
| TC-CA-01 | `test_cort_agent_run_task_returns_cort_result` — run_task returns CortResult | test_CortAgent.py | RED |
| TC-CA-02 | `test_cort_agent_metadata_has_agent_id` — metadata.agent_id matches agent_id | test_CortAgent.py | RED |
| TC-CA-03 | `test_cort_mixin_injects_into_base_agent` — CortMixin adds reason_with_cort | test_CortAgent.py | RED |
| TC-CA-04 | `test_cort_agent_default_config` — no explicit config → DEFAULT_CORT_CONFIG used | test_CortAgent.py | RED |
| TC-CA-05 | `test_cort_agent_reentrant_raises` — nested reason_with_cort raises CortRecursionError | test_CortAgent.py | RED |

## Validation Results

| ID | Result | Output |
|---|---|---|
| All 24 | RED (expected) | `ImportError: No module named 'src.core.reasoning'` — correct red-phase state |

## Unresolved Failures

All 3 test files fail at collection with `ImportError` (not `AssertionError`).
This is the correct red-phase state — `src/core/reasoning/` does not yet exist.
@6code must implement the source modules to turn these green.
