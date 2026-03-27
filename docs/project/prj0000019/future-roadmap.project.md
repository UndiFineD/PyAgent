# future-roadmap — Project Overview

## Project Identity
**Project ID:** prj0000019
**Short name:** future-roadmap
**Project folder:** `docs/project/prj0000019/`

## Project Overview
Enhances the `src/roadmap/` package with a real argparse CLI (`main(argv)`), an enriched vision template that reflects PyAgent's actual goals, and 5 tests covering all CLI subcommands.

## Goal & Scope
**Goal:** Make the roadmap generation tools usable from the command line with proper subcommands and a meaningful vision document template.

**In scope:**
- `src/roadmap/cli.py` — argparse CLI with `generate`, `vision`, `milestones` subcommands
- `src/roadmap/vision.py` — enriched vision template
- `tests/test_roadmap_cli.py` — 4 new tests (5 total)
- `docs/project/prj0000019/` — 9 doc artifacts

**Out of scope:**
- `milestones.py` functional changes
- `innovation.py` / `prioritization.py`

## Branch Plan
**Expected branch:** `prj0000019-future-roadmap`
**Scope boundary:** `src/roadmap/cli.py`, `src/roadmap/vision.py`, `tests/test_roadmap_cli.py`, `docs/project/prj0000019/`
**Handoff rule:** merge after 5 roadmap tests pass
**Failure rule:** if branch mismatch, STOP


## Milestones
Legacy milestone details are not specified in this historical document.


## Status
Legacy status details are not specified in this historical document.

