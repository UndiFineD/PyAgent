**External Integration Summary**

- **Extracted files:** 157 files placed under src/external_candidates/auto/
- **Extraction report used:** C:\DEV\PyAgent\.external\refactor_report.json
- **Static-check summary:**
  - bandit: code=1 result=C:\DEV\PyAgent\.venv\Scripts\python.exe: No module named bandit

  - semgrep: code=1 result=C:\DEV\PyAgent\.venv\Scripts\python.exe: Error while finding module specification for 'semgrep.cli' (ModuleNotFoundError: No module named 'semgrep')

  - python_only: code=0 result=0 files flagged

- **Generated tests:** Executed via `src/tools/run_auto_tests.py`

- **Where to review:** `src/external_candidates/auto/`, `.external/static_checks/`