# Description: src/observability/reports/report_generator_cli.py

Module overview:
- CLI entrypoint for running `ReportGenerator` and exporting the dashboard.
- Adds project root to `sys.path` for ease of invocation.

Primary functions:
- `main()`: parses arguments and writes `report.html` and `PROGRESS_DASHBOARD.md` to the output directory.

Notes:
- Includes a small helper `_sha256_text` used by legacy tests.
