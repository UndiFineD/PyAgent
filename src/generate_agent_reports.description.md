# Description: `generate_agent_reports.py`

## Module purpose
Generate per-file agent reports.

For every Python file under `scripts/agent/*.py`, this script writes:
- `<stem>.description.md`
- `<stem>.errors.md`
- `<stem>.improvements.md`

The output is intentionally lightweight and based on static inspection and
basic syntax/compile checks.

## Location
- Path: `scripts/agent/generate_agent_reports.py`

## Public surface
- Classes: CompileResult
- Functions: _read_text, _sha256_text, _try_parse_python, _compile_check, _is_pytest_test_file, _looks_like_pytest_import_problem, _find_top_level_defs, _find_imports, _detect_cli_entry, _detect_argparse, _placeholder_test_note, _write_md, _rel, render_description, render_errors, _find_issues, render_improvements, iter_agent_py_files, _get_existing_sha, main

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Uses `argparse` for CLI parsing.
- Invokes external commands via `subprocess`.
- Mutates `sys.path` to import sibling modules.

## Key dependencies
- Top imports: `__future__`, `ast`, `hashlib`, `re`, `sys`, `dataclasses`, `pathlib`, `typing`

## File fingerprint
- SHA256(source): `c1e014861e009e6c…`
