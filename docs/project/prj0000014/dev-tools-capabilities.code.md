# dev-tools-capabilities — Code Notes

_Status: COMPLETE_
_Coder: @6code | Updated: 2026-03-22_

## Changes Delivered

### `src/tools/remote.py`
- **Security fix**: replaced `shell=True` with explicit arg list. System `ssh`/`scp` binaries resolved via `shutil.which()`.
- Added `run_ssh_command(host, cmd, user, port)` → `CompletedProcess`.
- Added `upload_file(host, local, remote, user, port)` → `int` (returncode).
- Added `upload_files(host, paths, remote_dir, user, port)` → `list[int]`.
- CLI: `remote.py run <host> <cmd>` and `remote.py upload <host> <local> <remote>`.

### `src/tools/ssl_utils.py`
- Added `check_expiry(host, port=443, timeout=10)` using stdlib `ssl` + `socket`. Returns: `{subject, issuer, not_before, not_after, days_remaining, expired}`.
- Added `verify_pem_file(path)` — loads PEM, parses `not_after`.
- CLI: `ssl_utils.py expiry <host>` / `ssl_utils.py verify <pem>`.

### `src/tools/git_utils.py`
- Added `create_feature_branch(name, base="main")`.
- Added `changed_files(base="main")` → `list[str]`.
- Added `update_changelog(entry, path)` — prepends dated entry.
- Added `_current_branch()` helper.
- CLI: new `branch` and `changelog` subcommands.

## Health Checks
- All three files have copyright header.
- No `shell=True` anywhere.
- All subprocess calls use `check=False` and explicit `list` args.
