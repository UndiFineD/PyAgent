# Development Tools

This document catalogs the helper utilities bundled in `src/tools`.
Each tool is registered at import time and can be invoked via the shared CLI
entrypoint:

```sh
python -m src.tools <tool> [args...]
```

## Available tools

The following tools are currently available and exercised via unit tests:

* `agent_plugins` – load and list additional agent plugin modules.
* `boot` – bootstrap starter project manifests (`pyproject.toml`, `package.json`, `Cargo.toml`).
* `dependency_audit` – audit dependency manifests (`pyproject.toml`, `requirements.txt`).
* `git_utils` / `9git` – common git helper commands (status, log, branch, diff). 
  `9git` is an alias used by the agent workflow.
* `metrics` – gather basic repository metrics (line counts, file counts).
* `netcalc` – CIDR and subnet calculation utilities.
* `nettest` – TCP connectivity checks (async).
* `nginx` – validate an NGINX configuration (`nginx -t`).
* `port_forward` – simple async TCP port forwarder.
* `proxy_test` – test HTTP proxy connectivity.
* `remote` – local command runner (placeholder for SSH/FTP helpers).
* `self_heal` – basic syntax scanning across Python files.
* `code_quality` – focused lint/typecheck/test runner for changed files (intended for @8ql).
* `ssl_utils` – inspect PEM certificates (expiry, subject).
* `knock` – port knocking client.

## Usage examples

### List available tools

```sh
python -m src.tools
```

### Run a tool

```sh
python -m src.tools netcalc cidr 192.168.0.0/24
```

### Get help for a tool

```sh
python -m src.tools git-utils --help
```

## Adding a new tool

To add a tool, create a new module under `src/tools/` with a `main(args)`
function and call `register_tool("<name>", main, "<description>")`.
The tool will automatically be discoverable by the shared CLI.
