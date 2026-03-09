import os
from pathlib import Path
import subprocess


def run_setup_script() -> None:
    """Helper to run the governance setup script in the project root."""
    # run the governance initialization script
    subprocess.check_call(["python", "scripts/setup_governance.py"])


def test_governance_docs_created(tmp_path, monkeypatch) -> None:
    """The governance setup script should create expected docs and directories."""
    # ensure script creates expected files and directories
    # operate in workspace root
    run_setup_script()
    root = Path(os.getcwd()) / "project"
    expected = [
        "governance.md",
        "milestones.md",
        "budget.md",
        "risk.md",
    ]
    for fname in expected:
        path = root / fname
        assert path.exists(), f"{fname} should exist after setup"
        assert path.read_text().startswith("#"), "file should have header"
    dirs = ["metrics", "standups", "incidents", "templates"]
    for d in dirs:
        assert (root / d).is_dir(), f"directory {d} should exist"


def test_status_email_template(tmp_path, monkeypatch) -> None:
    """The status email template should be created with expected content."""
    root = Path(os.getcwd()) / "project" / "templates"
    sample = root / "status_email.md"
    assert sample.exists(), "status_email.md should exist"
    content = sample.read_text()
    assert "{{DATE}}" in content, "template must contain {{DATE}} token"
