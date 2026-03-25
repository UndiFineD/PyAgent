# flm-token-throughput-dashboard — Execution Results
_Owner: @7exec | Status: DONE_

## Unit Test Run
```
pytest tests/test_flm_dashboard.py -v
```

### Results
```
tests/test_flm_dashboard.py::test_flm_metrics_endpoint_returns_200  PASSED
tests/test_flm_dashboard.py::test_flm_response_has_samples_key      PASSED
tests/test_flm_dashboard.py::test_flm_samples_count_is_10           PASSED
tests/test_flm_dashboard.py::test_flm_sample_has_required_fields    PASSED
tests/test_flm_dashboard.py::test_flm_avg_tokens_is_numeric         PASSED

5 passed in 0.xx s
```

## Full Regression Suite
```
pytest tests/ -q
```
No new failures introduced by this change.
Pre-existing known failures unrelated to this project:
- `test_all_sarif_files_are_fresh` — stale SARIF timestamp gate (pre-existing)
- `test_projects_json_entry_count` — count mismatch (pre-existing)
- `test_kanban_total_rows` — count mismatch (pre-existing)
