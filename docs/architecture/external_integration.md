**External Integration Summary**

- **Extracted files:** 157 files placed under src/external_candidates/auto/
- **Extraction report used:** C:\DEV\PyAgent\.external\refactor_report.json
- **Static-check summary:**
  - bandit: code=1 result=[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[json]	INFO	JSON output written to file: C:\DEV\PyAgent\.external\static_checks\bandit.json

  - semgrep: code=0 result=C:\DEV\PyAgent\.external\static_checks\semgrep.json
  - python_only: code=0 result=0 files flagged

- **Generated tests:** Executed via `src/tools/run_auto_tests.py`

- **Where to review:** `src/external_candidates/auto/`, `.external/static_checks/`