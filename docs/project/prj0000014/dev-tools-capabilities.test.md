# dev-tools-capabilities — Test Strategy

_Status: COMPLETE_
_Tester: @5test | Updated: 2026-03-22_

## Test File
`tests/tools/test_capabilities_modules.py`

## Coverage

### `remote.py`
```python
def test_run_ssh_command_builds_correct_args(monkeypatch):
    """Ensure no shell=True is passed to subprocess."""
    captured = {}
    def fake_run(args, **kwargs):
        captured['args'] = args
        captured['shell'] = kwargs.get('shell', False)
        return SimpleNamespace(returncode=0, stdout='', stderr='')
    monkeypatch.setattr(subprocess, 'run', fake_run)
    run_ssh_command('host', 'uptime', user='user')
    assert isinstance(captured['args'], list)
    assert not captured['shell']
```

### `ssl_utils.py`
```python
def test_check_expiry_returns_expected_keys(monkeypatch): ...
def test_verify_pem_file_nonexistent(): ...
```

### `git_utils.py`
```python
def test_create_feature_branch_invokes_git(monkeypatch): ...
def test_changed_files_returns_list(monkeypatch): ...
def test_update_changelog_prepends_entry(tmp_path): ...
```

## Non-Goals
- No live TLS connections in tests (monkeypatched).
- No actual git repo operations (monkeypatched subprocess).
