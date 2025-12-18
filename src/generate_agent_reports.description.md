# Description: `generate_agent_reports.py`

## Module purpose

`generate_agent_reports.py` generates simple per-file reports for Python sources in `src/`.

For each `src/*.py`, it writes three markdown files into `src/`:

- `<stem>.description.md`
- `<stem>.errors.md`
- `<stem>.improvements.md`

Reports are based on static inspection (AST parse, top-level def discovery, import listing) plus a lightweight syntax check.

## Location

- Path: `src/generate_agent_reports.py`

## Public surface

- Primary entrypoint: `main(argv: Sequence[str]) -> int`
- File iteration: `iter_agent_py_files() -> Iterable[Path]` (currently `src/*.py`)
- Report renderers: `render_description(...)`, `render_errors(...)`, `render_improvements(...)`

Note: The file also contains many report-system enums/dataclasses that are not currently used by `main()`.

## Behavior summary

- Has a CLI entrypoint (`__main__`).
- Does not currently parse CLI flags; `argv` is accepted but unused.
- Skips unchanged files by comparing the first 16 hex chars of `SHA256(source)` against the value embedded in the existing `<stem>.description.md`.
- Normalizes output newlines to `\n` and enforces a single trailing newline.

## Key dependencies

- Top imports: `__future__`, `ast`, `hashlib`, `re`, `sys`, `dataclasses`, `pathlib`, `typing`

## File fingerprint

- SHA256(source): `C58832E7DC7CF6F71652659FF372A3D266CC1891AD513CE72CAB98C9D9C8C663`
