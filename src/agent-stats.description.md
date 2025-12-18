# Description: `agent-stats.py`

## Module purpose

`src/agent-stats.py` provides a standalone Stats Agent that summarizes “progress”
across a set of files by counting how many have the expected companion docs and
tests present.

## Location

- Path: `src/agent-stats.py`

## Public surface (high level)

- Class: `StatsAgent`
- Function: `main()` (CLI entrypoint)

## Behavior summary

- Input: a list of file paths (passed via `--files ...`).
- Validates input files and filters out missing paths; raises `ValueError` if no
  valid files remain.
- For each input file, checks for adjacent companion files based on `stem`:
  - `{stem}.description.md`
  - `{stem}.changes.md`
  - `{stem}.errors.md`
  - `{stem}.improvements.md`
  - `test_{stem}.py`
- Reports counts for total files and each “has companion” bucket.
- Optional extras:
  - `--coverage`: reads JSON and stores `total_coverage` in the stats.
  - `--export`: writes stats to `stats_output.{json,csv,html,db}`.
  - `--baseline`: loads JSON baseline stats and prints a comparison report.
  - `--format`: outputs the summary as `text`, `json`, or `csv`.
  - If `matplotlib` is installed, it will also display a bar chart.

## CLI usage

- Example:
  - `python src/agent-stats.py --files src/*.py --format text`
- Export multiple formats:
  - `python src/agent-stats.py --files src/*.py --export json csv html sqlite`

## Key dependencies

- Standard library: `argparse`, `csv`, `json`, `logging`, `pathlib`, `sys`
- Optional: `matplotlib` (enables chart visualization)

## File fingerprint

- SHA256(source): `8AAA2393605155970C1B6E58B7FBD29B2DFC7CFE1829CCD4217C18AB30390E96`
