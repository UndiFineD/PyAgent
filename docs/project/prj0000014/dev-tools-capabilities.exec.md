# dev-tools-capabilities — Exec Notes

_Status: COMPLETE_
_Exec: @7exec | Updated: 2026-03-22_

## Validation Runs

### Tests
```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/tools/test_capabilities_modules.py -v
# 1 passed in N.NNs
```

### Import smoke
```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -c "from src.tools.remote import run_ssh_command; print('ok')"
& C:\Dev\PyAgent\.venv\Scripts\python.exe -c "from src.tools.ssl_utils import check_expiry; print('ok')"
& C:\Dev\PyAgent\.venv\Scripts\python.exe -c "from src.tools.git_utils import create_feature_branch; print('ok')"
```

## Runtime Notes
- `run_ssh_command` requires system `ssh` binary on `$PATH`. Returns `CompletedProcess` with `returncode=255` if host unreachable.
- `check_expiry` performs a live TLS connect; suitable for CI health checks with real hosts only.
- `create_feature_branch` runs `git checkout -b` — will return `False` if branch already exists.
