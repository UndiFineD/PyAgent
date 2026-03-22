# Development Tools

This document catalogs the helper utilities bundled in `src/tools`.
Each tool is registered at import time and can be invoked via the shared CLI
entrypoint:

```sh
python -m src.tools <tool> [args...]
```

## Available tools

| Tool name | Module | Description |
|-----------|--------|-------------|
| `agent-plugins` | `agent_plugins.py` | Load and list additional agent plugin modules via an allowlist-validated loader. |
| `boot` | `boot.py` | Bootstrap starter project manifests (`pyproject.toml`, `package.json`, `Cargo.toml`). |
| `code-quality` | `code_quality.py` | Focused lint/typecheck/test runner for changed files (intended for @8ql). |
| `dependency-audit` | `dependency_audit.py` | Audit dependency manifests (`pyproject.toml`, `requirements.txt`). |
| `9git` / `git-utils` | `git_utils.py` | Git workflow helpers: status, log, diff, branch listing, `create_feature_branch()`, `changed_files()`, `update_changelog()`. |
| `knock` | `knock.py` | Port knocking client. |
| `metrics` | `metrics.py` | Full AST-based code metrics: lines, blank lines, comments, functions, classes, cyclomatic complexity estimates. |
| `netcalc` | `netcalc.py` | CIDR and subnet calculation utilities (stdlib `ipaddress`). |
| `nettest` | `nettest.py` | Async TCP connectivity checks (`asyncio.open_connection`). |
| `nginx` | `nginx.py` | Validate an NGINX configuration (`nginx -t`). |
| `plugin-loader` | `plugin_loader.py` | Allowlist-validated plugin loader: `discover_plugins()`, `load_plugin()`. Rejects path traversal and unlisted names. |
| `port-forward` | `port_forward.py` | Simple async TCP port forwarder. |
| `proxy-test` | `proxy_test.py` | Test HTTP proxy connectivity. |
| `remote` | `remote.py` | SSH/SCP operations using explicit subprocess arg lists (no `shell=True`): `run_ssh_command()`, `upload_file()`, `upload_files()`. |
| `self-heal` | `self_heal.py` | Basic syntax scanning across Python files. |
| `ssl-utils` | `ssl_utils.py` | TLS certificate inspection: `check_expiry()` (live TLS), `verify_pem_file()` (local PEM). |
| `ql` | `ql.py` | CodeQL and security analysis runner. |

## PM subpackage (`src/tools/pm/`)

| Module | Description |
|--------|-------------|
| `kpi.py` | KPI computation (throughput, velocity). |
| `risk.py` | Risk matrix helpers. |
| `email.py` | Simple email template rendering. |

## Usage examples

### List available tools

```sh
python -m src.tools
```

### Run a tool

```sh
python -m src.tools netcalc cidr 192.168.0.0/24
python -m src.tools metrics --file src/tools/git_utils.py
python -m src.tools ssl-utils expiry google.com
python -m src.tools 9git branch my-feature-branch
```

### Get help for a tool

```sh
python -m src.tools git-utils --help
```

## Adding a new tool

To add a tool, create a new module under `src/tools/` with a `main(args: list[str] | None) -> int`
function and call `register_tool("<name>", main, "<description>")` at module level.
The tool will automatically be discoverable by the shared CLI.

**Important constraints:**
- Use only `subprocess.run(args_list, ...)` — never `shell=True` with user input.
- Add a copyright header to every new module.
- Register via `tool_registry.register_tool()` — do not bypass the registry.

