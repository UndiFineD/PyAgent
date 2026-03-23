# Think: prj0000050 — Install Script

## Status
Complete

## Findings

### Python
- **Required version:** `>=3.12` (from `pyproject.toml` `requires-python`; CI uses `3.13`)
- **Docs/setup.md says** Python 3.11+ — this is **outdated and incorrect**
- **Requirements files:**
  - `requirements.txt` — core runtime deps (cryptography, fastapi, httpx, openai, pydantic, PyYAML, prometheus-client)
  - `backend/requirements.txt` — backend service deps (fastapi, uvicorn, aiortc, pydantic, websockets, httpx, psutil)
  - `requirements-ci.txt` — dev/CI tooling (includes `-r requirements.txt` + ruff, flake8, mypy, pytest, maturin, mkdocs, etc.)
  - `pyproject.toml` — extensive `[project.dependencies]` list (aiofiles, aiohttp, anthropic, chromadb, numpy, pandas, torch, etc.) — canonical full deps
- **Virtual env convention:** `.venv` at repo root (confirmed by CI, CONTRIBUTING.md, existing `.venv`)
- **Install approach:** `pip install -r requirements.txt` + `pip install -r backend/requirements.txt`
  - For full dev setup: also `pip install -r requirements-ci.txt` (which includes maturin)

### Rust
- **Required toolchain:** stable (no `rust-toolchain.toml` or `rust-toolchain` file found)
- **Current installed:** `rustc 1.93.1 / cargo 1.93.1`
- **Rust edition:** 2021 (in both `rust_core/Cargo.toml` and `rust_core/p2p/Cargo.toml`)
- **Crates to build:**
  - `rust_core/` — main PyO3 CDylib extension (`_rust_core`), builds with `maturin develop`
  - `rust_core/p2p/` — standalone `rust_core_p2p` binary (libp2p), builds with `cargo build`
- **Build command (from CI):** `maturin develop --manifest-path rust_core/Cargo.toml`
- **maturin version required:** `>=1.0,<2.0` (build-system in `pyproject.toml`); CI pins `maturin==1.12.5`
- **rust-toolchain file:** NOT FOUND — must rely on system-installed stable Rust

### Node.js
- **Required version:** Not pinned anywhere (no `.nvmrc`, no `engines` field in `web/package.json`)
- **Current installed:** `v24.12.0` / npm `11.6.2`
- **Package manager:** npm
- **Install location:** `web/`
- **Frontend stack:** Vite 8 + React 19 + TypeScript 5.9 + Vitest 4
- **Install command:** `Push-Location web; npm install; Pop-Location`

### Other tools
- **maturin** — required to build the Rust PyO3 extension into the Python venv; included in `requirements-ci.txt`
- **ruff** — linter (`ruff==0.15.6` in CI)
- **mypy** — type checker (`mypy==1.19.1` in CI)
- **flake8** — linter (`flake8==7.3.0` in CI)
- **pytest / pytest-asyncio / pytest-cov** — test stack
- **mkdocs + mkdocstrings** — documentation build
- **Docker** — optional, noted in `docs/setup.md`, used by some integration tests; not required for dev
- **mkcert** — NOT found in any config
- **cargo-audit** — NOT found in CI workflows
- **`scripts/setup_structure.py`** — creates required directory scaffolding; mentioned in `docs/setup.md` step 4

### Existing setup docs
- **`docs/setup.md`**: Outdated. Says Python 3.11+ (should be 3.12+). Only installs `requirements.txt`, skips `backend/requirements.txt`, Rust build, and Node.js. Mentions `scripts/setup_structure.py`.
- **`README.md`**: Shows all three components manually (run core, run backend, run frontend) but no unified install flow.
- **`CONTRIBUTING.md`**: Basic venv activate + `pip install -r requirements.txt` + pytest. No backend or Rust steps.
- **`docs/onboarding.md`**: High-level orientation, references `docs/setup.md` for actual install steps.

### Gaps
1. `docs/setup.md` specifies Python 3.11+ but code requires 3.12+
2. No `rust-toolchain.toml` — Rust version is not pinned; script should warn if rustc < 1.80
3. No Node version pinned anywhere — script should warn if node < 18 (LTS minimum reasonable floor)
4. Backend requirements are never mentioned in setup docs (only in README.md)
5. Rust build step missing from all user-facing docs
6. `pyproject.toml` has large dependency list (torch, chromadb, etc.) — `pip install -e .` would install all; CI uses lighter `requirements.txt`
7. `rust_core/p2p/` is a standalone binary — NOT built by `maturin develop` and not required for dev testing

---

## Ordered Setup Steps

1. **Check Python ≥ 3.12** — abort with message if not satisfied
2. **Check Git** — warn if not found
3. **Check Rust/cargo** — warn (not abort) if not found; set `$BuildRust` flag; warn if version < 1.80
4. **Check Node.js/npm** — warn (not abort) if not found; set `$BuildWeb` flag
5. **Create Python virtual environment** — `python -m venv .venv` (skip if already exists)
6. **Activate venv** — `.\.venv\Scripts\Activate.ps1`
7. **Install core Python deps** — `pip install --prefer-binary -r requirements.txt`
8. **Install backend Python deps** — `pip install --prefer-binary -r backend/requirements.txt`
9. **Install maturin** — `pip install "maturin>=1.0,<2.0"` (needed for Rust build)
10. **Build Rust extension** (conditional on `$BuildRust`) — `maturin develop --manifest-path rust_core/Cargo.toml`
11. **Run setup_structure.py** — `python scripts/setup_structure.py` (creates scaffolding dirs)
12. **Install frontend deps** (conditional on `$BuildWeb`) — `Push-Location web; npm install; Pop-Location`
13. **Summary** — print what succeeded/was skipped with next-steps hints

---

## Recommended Script Structure

```
install.ps1
├── Section 0: Header / banner
├── Section 1: Prerequisite checks
│   ├── Check Python version (hard fail if < 3.12)
│   ├── Check Git (warn only)
│   ├── Check Rust/cargo version (warn; set $BuildRust flag)
│   └── Check Node/npm (warn; set $BuildWeb flag)
├── Section 2: Python virtual environment
│   ├── Create .venv if not exists
│   └── Activate .venv
├── Section 3: Python dependencies
│   ├── pip install --prefer-binary -r requirements.txt
│   └── pip install --prefer-binary -r backend/requirements.txt
├── Section 4: Maturin + Rust build (conditional on $BuildRust)
│   ├── pip install "maturin>=1.0,<2.0"
│   └── maturin develop --manifest-path rust_core/Cargo.toml
├── Section 5: Project scaffolding
│   └── python scripts/setup_structure.py
├── Section 6: Frontend (conditional on $BuildWeb)
│   ├── Push-Location web
│   ├── npm install
│   └── Pop-Location
└── Section 7: Summary printout
    ├── What was installed
    ├── What was skipped (and why)
    └── Next steps (how to run core / backend / frontend)
```

**Style decisions:**
- `$ErrorActionPreference = 'Stop'` within each try-block; restore after
- `Write-Host` with colour (`-ForegroundColor Green/Yellow/Red`) for status
- `try/catch` per section; Rust build failure does NOT abort Python setup
- Non-critical sections wrapped in `if ($BuildRust)` / `if ($BuildWeb)` guards
- Idempotent — safe to re-run on an existing setup

---

## Edge Cases / Error Handling

| Scenario | Handling |
|---|---|
| Python < 3.12 found | Hard abort with clear version message |
| Python 3.12+ found but venv already exists | Skip creation, activate existing |
| pip install fails | Abort section, print error; suggest `--prefer-binary` |
| cargo not found | Set `$BuildRust = $false`; warn: "Rust not found — skipping _rust_core build. Install via rustup." |
| maturin develop fails | Print failure + suggestion to check Rust toolchain; continue script |
| npm not found | Set `$BuildWeb = $false`; print warning |
| `scripts/setup_structure.py` fails | Non-fatal warning only |
| Script run as non-admin | No admin rights needed; all installs are user-local |
| Windows Execution Policy blocks `.ps1` | Note at top: run with `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process` |
| Execution on non-Windows | Guard at top: `if ($IsLinux -or $IsMacOS) { Write-Error "..."; exit 1 }` |
