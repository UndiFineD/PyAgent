import importlib
import subprocess
import sys
from pathlib import Path
import py_compile

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATION_DIR = REPO_ROOT / ".github" / "agents" / "orchestration"
sys.path.insert(0, str(ORCHESTRATION_DIR))
redact = importlib.import_module("context_manager").redact


def test_redact_masks_common_secret_patterns():
    sample = """
Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456
api_key: secret-value-1234567890
email=test@example.com
private_key: \"-----BEGIN PRIVATE KEY-----\nABCDEF\n-----END PRIVATE KEY-----\"
"""
    redacted = redact(sample)
    assert "secret-value-1234567890" not in redacted
    assert "test@example.com" not in redacted
    assert "BEGIN PRIVATE KEY" not in redacted
    assert "Bearer abcdef" not in redacted
    assert "<REDACTED>" in redacted


def test_install_script_has_valid_bash_syntax():
    script_path = REPO_ROOT / "install.sh"
    result = subprocess.run(["bash", "-n", str(script_path)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_install_script_sets_default_openrouter_model():
    script_path = REPO_ROOT / "install.sh"
    content = script_path.read_text(encoding="utf-8")
    assert 'DEFAULT_PROVIDER="openrouter"' in content
    assert 'DEFAULT_OPENROUTER_MODEL="nvidia/nemotron-3-super-120b-a12b:free"' in content


def test_orchestration_entrypoints_compile():
    for relative_path in (
        ".github/agents/orchestration/daemon.py",
        ".github/agents/orchestration/intent_decomposer.py",
    ):
        py_compile.compile(str(REPO_ROOT / relative_path), doraise=True)
